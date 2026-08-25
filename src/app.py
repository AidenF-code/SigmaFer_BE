import os
from dotenv import load_dotenv

from flask import Flask
from src.models import Base, engine, session
from src.models.productos import Productos
from src.models.categorias import Categorias
from src.models.proveedores import Proveedores
from src.models.detalle_doc_inventario import DetalleDocInventario
from src.models.documento_inventarios import DocumentoInventarios
from src.models.usuarios import Usuarios
from src.models.rol import Roles
from src.models.clientes import Clientes
from src.models.orden_compra import OrdenCompra
from src.models.detalle_oc import DetalleOC
from src.models.metodo_pago import MetodoPago
from src.models.facturas import Facturas
from src.models.detalle_facturas import DetalleFacturas
from src.routes import all_blueprints



load_dotenv()

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

try:
    Base.metadata.create_all(engine)
except Exception as e:
    print(f"Aviso: Base.metadata.create_all omitido o no conectó: {e}")

@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()

prefix = '/api/v1'
for bp in all_blueprints:
    url_prefix = f"{prefix}/{bp.name}"
    app.register_blueprint(bp, url_prefix=url_prefix)

if __name__ == '__main__':
    app.run(debug=True)
