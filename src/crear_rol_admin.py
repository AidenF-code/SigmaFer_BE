from sqlalchemy import text
from src.models import engine

try:
    with engine.begin() as connection:

        connection.execute(
            text("""
                INSERT INTO rol (nombre, permisos)
                VALUES (:nombre, :permisos)
            """),
            {
                "nombre": "Administrador",
                "permisos": "{}"
            }
        )

    print("Rol Administrador creado correctamente")

except Exception as e:
    print("Error:", e)