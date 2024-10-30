import mysql.connector
from tkinter import messagebox
import os
from dotenv import load_dotenv

load_dotenv()

# Variable de control para rastrear si ya se ha mostrado un mensaje de error
error_mostrado = False

def obtener_conexion():
    global error_mostrado
    try:
        conexion = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            port=os.getenv("DB_PORT")
        )
        print("Conexión a la base de datos establecida.")
        error_mostrado = False  # Reiniciar la variable de control si la conexión es exitosa
        return conexion
    except mysql.connector.Error as err:
        if not error_mostrado:
            messagebox.showerror("Error", f"Error al conectar a la base de datos: {err}")
            error_mostrado = True
        print(f"Error al conectar a la base de datos: {err}")
        return None

def insertar_datos(datos):
    global error_mostrado
    conexion = obtener_conexion()
    if conexion is None:
        return
    try:
        cursor = conexion.cursor()
        for fila in datos:
            print(f"Insertando fila: {fila}")
            cursor.execute("""
                INSERT INTO Actividades (numero_actividad, dia, actividad, parroquia, direccion, mes)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, fila)
        conexion.commit()
        print("Datos insertados correctamente.")
        error_mostrado = False  # Reiniciar la variable de control si la inserción es exitosa
    except mysql.connector.Error as err:
        if not error_mostrado:
            messagebox.showerror("Error", f"Error al insertar datos: {err}")
            error_mostrado = True
        print(f"Error al insertar datos: {err}")
    finally:
        conexion.close()

def buscar_archivos(columna, filtro):
    conexion = obtener_conexion()
    if conexion is None:
        return []
    try:
        cursor = conexion.cursor()
        query = f"SELECT numero_actividad, dia, actividad, parroquia, direccion, mes FROM Actividades WHERE {columna} LIKE %s"
        cursor.execute(query, (f"%{filtro}%",))
        resultados = cursor.fetchall()
        return resultados
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al buscar datos: {err}")
        return []
    finally:
        conexion.close()

def actualizar_datos(datos):
    conexion = obtener_conexion()
    if conexion is None:
        return
    try:
        cursor = conexion.cursor()
        query = """
            UPDATE Actividades
            SET dia = %s, actividad = %s, parroquia = %s, direccion = %s, mes = %s
            WHERE numero_actividad = %s
        """
        cursor.execute(query, (datos[1], datos[2], datos[3], datos[4], datos[5], datos[0]))
        conexion.commit()
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al actualizar datos: {err}")
    finally:
        conexion.close()