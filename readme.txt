V projketu sem naredil txt. bazo podatkov. 
Datoteke je možno naložiti v bazo podatkov, jih naložiti iz baze podatkov in odstraniti. 

**Setup**

Kloniranje repozitorija:
```bash
git clone https://github.com/stasdolinsek/projekt_NUKS

cd projekt_NUKS

**Setup po naloženem repo:**

sudo docker build -t my_fastapi_app .
sudo docker run -d -p 8000:8000 my_fastapi_app

**Odprtje v brskalniku:**

http://212.101.137.104:8000/static/index.html
