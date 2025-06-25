🌱 PlantSense - Sistema IoT de Monitoreo de Humedad de Tierra

Este proyecto integra hardware (ESP8266 + sensor YL-69), backend (FastAPI + PostgreSQL) y frontend (Vue.js + Chart.js) para monitorear en tiempo real la humedad del suelo de una planta.

📦 Estructura del Proyecto
/PlantSense
-  esp8266/              → Código para la placa ESP8266
   -   yl-69-.ino

- init-db/              → Script SQL para crear base de datos y tablas
   -  init.sql

-  main.py               → Backend FastAPI
- docker-compose.yml    → Infraestructura completa con Docker (opcional)
- frontend/             → Frontend Vue + Chart.js
   -   src/
   -  App.vue           → Dashboard con gráfica y tabla


🔌 Hardware Utilizado

ESP8266 NodeMCU
Sensor de humedad de tierra YL-69
Alimentación por microUSB
Comunicación por WiFi


🔧 Backend (FastAPI + PostgreSQL)

Ruta para registrar lecturas:

POST /insert/lecturas
Body JSON: { "id_sensor": 1, "valor": 657 }


Ruta para obtener lecturas:

GET /select/lecturas


Calcula automáticamente el porcentaje de humedad en base al valor leído (0–1023).


🌐 Frontend (Vue 3 + Chart.js)

Dashboard responsivo accesible en navegador web
Muestra:
Tabla de las últimas 20 lecturas
Gráfica en tiempo real de humedad (%)


Actualización automática cada 10 segundos

Para ejecutarlo:
cd frontend
npm install
npm run dev

Luego visita: http://localhost:5173

🐳 (Opcional) Despliegue con Docker
docker-compose up --build

Esto levanta:

Base de datos PostgreSQL
API con FastAPI
Frontend (requiere build adicional)


👨‍💻 Autor

Bryan Gómez
Universidad: Universidad Piloto de Colombia
Proyecto académico para la asignatura: Infraestructura


📸 Vista previa
(Puedes añadir capturas de pantalla del dashboard aquí si lo deseas)

✅ Estado del Proyecto
✅ Recolección de datos✅ API REST funcional✅ Dashboard completo✅ Actualización en tiempo real⬜ Despliegue externo (opcional)



Para correr este proyecto esnecesario instalar Python:
https://www.python.org/ftp/python/3.12.0/python-3.12.0 amd64.exe

2. pip install virtualenv => Esto permitirá crear un entorno ailado para el proyecto 
3. virtualenv <nombre de proyecto> o python -m virtualenv <nombre de proyecto>
4. cd proyecto 
5. Scripts\activate.bat
6.  pip install fastapi uvicorn psycopg2
7.  scripts\activate.bat
8.  uvicorn main:app --reload --port=3000
9.  uvicorn main:app --host 0.0.0.0 --port 3000 --reload
//PowerSell  Abre firewall
1. New-NetFirewallRule -DisplayName "FastAPI 3000" -Direction Inbound -Protocol TCP -LocalPort 3000 -Action Allow
2. http://192.168.80.15:3000/docs#/

npm create vite@latest frontend -- --template vue
cd frontend
npm install
npm install axios chart.js

Para correr el proyecto:
docker-compose up -d  // Tenga presente que debe tener docker abierto


uvicorn main:app --host 0.0.0.0 --port 3000 --reload
npm run dev
