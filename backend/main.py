from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Optional
from fastapi import HTTPException
from pydantic import BaseModel

class Sensor(BaseModel):
    id: int
    nombre: str
    ubicacion: str
    descripcion: str
class lecturaInsert(BaseModel):
    id_sensor: int
    valor: int


# Variables de conexión a base de datos
DB_HOST = "192.168.56.1"
DB_NAME = "BD_plant_sense"
DB_USER = "plat"
DB_PASWD = "plant123"

# Conectar a la base de datos
cc = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASWD, host=DB_HOST, port=5432)
# Cursor para ejecutar SQL
cursor_obj = cc.cursor(cursor_factory=RealDictCursor)

# Creación de objeto API
app = FastAPI()

# Agregar el middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas las direcciones. Puedes restringirlo con una lista de URLs específicas.
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos HTTP
    allow_headers=["*"],  # Permite todos los encabezados
)
# Rutas CRUD para la tabla `dispositivo`




# Crear sensores
@app.post("/insert/sensores", tags=["Sensor"])
async def insert_sensor(nombre: str, ubicacion: str, descripcion: str):
    try:
        sql = f"INSERT INTO sensores (nombre, ubicacion, descripcion) VALUES ('{nombre}', '{ubicacion}', '{descripcion}')"
        cursor_obj.execute(sql)
        cc.commit()
        return {"message": "Sensor insertado exitosamente"}
    except Exception as e:
        cc.rollback()
        return {"error": f"Es:{str(e)}"}

# Leer sensores
@app.get("/select/sensores", tags=["Sensor"])
async def select_sensor():
    try:
        sql = "SELECT * FROM sensores ORDER BY id"
        cursor_obj.execute(sql)
        rows = cursor_obj.fetchall()
        return rows
    except Exception as e:
        cc.rollback()
        return {"error": f"Es:{str(e)}"}

# Por id

@app.get("/select/sensores/{id}", tags=["Sensor"])
async def get_sensor(id: int):
    try:
        sql = f"SELECT * FROM sensores WHERE id = {id}"
        cursor_obj.execute(sql)
        sensores = cursor_obj.fetchone()
        
        if sensores is None:
            raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
        
        return sensores  # Devolver el sensores encontrado
    except Exception as e:
        cc.rollback()
        return {"error": f"Error al obtener el sensores: {str(e)}"}

# Actualizar sensores
@app.put("/update/sensores/{id}", tags=["Sensor"])
async def update_sensor(id: int, nombre: Optional[str] = None, ubicacion: Optional[str] = None, descripcion: Optional[str] = None):
    try:
        set_clause = []
        if nombre:
            set_clause.append(f"nombre = '{nombre}'")
        if ubicacion:
            set_clause.append(f"ubicacion = '{ubicacion}'")
        if descripcion:
            set_clause.append(f"descripcion = '{descripcion}'")
        
        set_clause_str = ", ".join(set_clause)
        sql = f"UPDATE sensores SET {set_clause_str} WHERE id = {id}"
        cursor_obj.execute(sql)
        cc.commit()
        return {"message": "Sensor actualizado exitosamente"}
    except Exception as e:
        cc.rollback()
        return {"error": f"Es:{str(e)}"}

# Eliminar sensores
@app.delete("/delete/sensores/{id}", tags=["Sensor"])
async def delete_sensor(id: int):
    try:
        sql = f"DELETE FROM sensores WHERE id = {id}"
        cursor_obj.execute(sql)
        cc.commit()
        return {"message": "Sensor eliminado exitosamente"}
    except Exception as e:
        cc.rollback()
        return {"error": f"Es:{str(e)}"}

# Rutas CRUD para la tabla `lecturas`
# Crear lecturas
@app.post("/insert/lecturas", tags=["Lectura"])
async def insert_lectura(lectura: lecturaInsert):
    try:
        print(lectura)  # Verificar que llega correctamente
        sql = f"INSERT INTO lecturas (id_sensor, valor) VALUES ({lectura.id_sensor}, {lectura.valor})"
        print(sql)  # Verificar la consulta que se ejecuta
        cursor_obj.execute(sql)
        cc.commit()
        return {"message": "Lectura insertada exitosamente"}
    except Exception as e:
        cc.rollback()
        return {"error": f"Es:{str(e)}"}


# Leer lecturas
@app.get("/select/lecturas", tags=["Lectura"])
async def select_lectura():
    try:
        sql = "SELECT * FROM lecturas ORDER BY id"
        cursor_obj.execute(sql)
        rows = cursor_obj.fetchall()
        return rows
    except Exception as e:
        cc.rollback()
        return {"error": f"Es:{str(e)}"}
# Obtener lecturas por ID
@app.get("/lecturas/{id}", tags=["Lectura"])
async def get_lectura(id: int):
    try:
        sql = f"SELECT * FROM lecturas WHERE id = {id}"
        cursor_obj.execute(sql)
        lecturas = cursor_obj.fetchone()
        
        if lecturas is None:
            raise HTTPException(status_code=404, detail="Lectura no encontrada")
        
        return lecturas  # Devolver la lecturas encontrada
    except Exception as e:
        cc.rollback()
        return {"error": f"Error al obtener la lecturas: {str(e)}"}

# Actualizar lecturas
@app.put("/update/lecturas/{id}", tags=["Lectura"])
async def update_lectura(id: int, id_sensor: Optional[int] = None, valor: Optional[int] = None):
    try:
        set_clause = []
        if id_sensor:
            set_clause.append(f"id_sensor = {id_sensor}")
        if valor:
            set_clause.append(f"valor = {valor}")
        
        set_clause_str = ", ".join(set_clause)
        sql = f"UPDATE lecturas SET {set_clause_str} WHERE id = {id}"
        cursor_obj.execute(sql)
        cc.commit()
        return {"message": "Lectura actualizada exitosamente"}
    except Exception as e:
        cc.rollback()
        return {"error": f"Es:{str(e)}"}

# Eliminar lecturas
@app.delete("/delete/lecturas/{id}", tags=["Lectura"])
async def delete_lectura(id: int):
    try:
        sql = f"DELETE FROM lecturas WHERE id = {id}"
        cursor_obj.execute(sql)
        cc.commit()
        return {"message": "Lectura eliminada exitosamente"}
    except Exception as e:
        cc.rollback()
        return {"error": f"Es:{str(e)}"}
