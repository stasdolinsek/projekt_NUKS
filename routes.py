from fastapi import FastAPI, HTTPException, Response, status, UploadFile, File as FastAPIFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse
from database import create_connection, create_table, get_all_txt_files, add_txt_file, delete_txt_file
from typing import List, Optional
from pydantic import BaseModel
import io

class File(BaseModel):
    id: Optional[int]
    filename: str
    content: Optional[str]

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
db_file = 'project_database.db'

@app.on_event("startup")
async def startup():
    conn = create_connection(db_file)
    create_table(conn)
    conn.close()

@app.get("/files/", response_model=List[File])
async def read_files():
    conn = create_connection(db_file)
    files = get_all_txt_files(conn)
    conn.close()
    return files

@app.post("/files/", response_model=File, status_code=status.HTTP_201_CREATED)
async def create_file(file: UploadFile = FastAPIFile(...)):
    contents = await file.read()  # Preberi vsebino datoteke
    filename = file.filename
    conn = create_connection(db_file)
    add_txt_file(conn, filename, contents.decode('utf-8'))  # Shranite surove podatke kot string
    conn.close()
    return {"filename": filename, "content": "File uploaded successfully"}

@app.delete("/files/{file_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_file(file_id: int):
    rows_deleted = delete_txt_file(file_id, db_file)
    if rows_deleted == 0:
        raise HTTPException(status_code=404, detail="File not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.get("/files/{file_id}/download")
async def download_file(file_id: int):
    conn = create_connection(db_file)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT filename, content FROM txt_files WHERE id = ?", (file_id,))
        file_row = cursor.fetchone()
        if file_row:
            filename, content = file_row
            response = StreamingResponse(io.BytesIO(content.encode('utf-8')), media_type='application/octet-stream')
            response.headers['Content-Disposition'] = f'attachment; filename={filename}'
            return response
        else:
            raise HTTPException(status_code=404, detail="File not found")
    finally:
        cursor.close()
        conn.close()
