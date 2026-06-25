from flask import Flask
from src.models import Base, engine
from src.models.productos import Productos
from src.models.categorias import Categorias
from src.models.proovedores import Proveedores
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





app = Flask(__name__)

Base.metadata.create_all(engine)

if __name__ == '__main__':
    app.run(debug=True)