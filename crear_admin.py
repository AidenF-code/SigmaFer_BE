import os
import sys

# Asegurar que reconozca el módulo src tanto si está en la raíz como si está en src/
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)
sys.path.append(os.path.dirname(current_dir))

from src.models import Base, engine, session
from src.models.rol import Roles
from src.models.usuarios import Usuarios

def seed_admin():
    print("[...] Conectando a la base de datos...")
    
    # 1. Crear las tablas si aún no existen en la BD de Aiven
    Base.metadata.create_all(bind=engine)
    print("[OK] Tablas verificadas / creadas.")

    # 2. Verificar o crear el Rol de Administrador
    rol_admin = Roles.get_by_nombre("Administrador")
    if not rol_admin:
        rol_admin = Roles(nombre="Administrador", permisos={})
        session.add(rol_admin)
        session.commit()
        print(f"[OK] Rol Administrador creado con ID: {rol_admin.id}")
    else:
        print(f"[INFO] Rol Administrador ya existia con ID: {rol_admin.id}")

    # 3. Datos del usuario a crear
    correo_admin = "admin@sigmafer.com"
    password_plana = "Password123"

    usuario = Usuarios.get_by_correo(correo_admin)
    if not usuario:
        usuario = Usuarios(
            nombre="Administrador Principal",
            correo=correo_admin,
            telefono="3000000000",
            password="",  # Se establece con set_password abajo
            rol_id=rol_admin.id,
            identificacion="1000000001",
            estado=True,
            primer_ingreso=False  # Para obtener el token directamente en Postman
        )
        usuario.set_password(password_plana)
        session.add(usuario)
        session.commit()
        print("\n[EXITO] Usuario creado exitosamente!")
        print(f"Correo: {correo_admin}")
        print(f"Contrasena: {password_plana}")
    else:
        print(f"\n[INFO] El usuario con correo {correo_admin} ya existe.")

if __name__ == "__main__":
    try:
        seed_admin()
    except Exception as e:
        session.rollback()
        print(f"\n[ERROR] Error al crear usuario: {e}")
