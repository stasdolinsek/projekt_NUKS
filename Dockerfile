# Uporabimo osnovni image z Pythonom
FROM python:3.11.2-slim

# Nastavimo delovni direktorij znotraj kontejnerja
WORKDIR /app

# Kopiramo requirements.txt v delovni direktorij
COPY requirements.txt .

# Namestimo odvisnosti
RUN pip install --no-cache-dir -r requirements.txt

# Kopiramo celotno aplikacijo v delovni direktorij
COPY . .

# Expose porta, ki ga uporablja FastAPI
EXPOSE 8000

# Zaženemo aplikacijo
CMD ["uvicorn", "routes:app", "--host", "0.0.0.0", "--port", "8000"]
