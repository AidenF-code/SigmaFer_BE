from .productos_routes import productos_bp
from .categorias_routes import categorias_bp
from .roles_routes import roles_bp
from .facturas_routes import facturas_bp
from .detalle_facturas_routes import detalle_facturas_bp
from .clientes_routes import clientes_bp
from .usuarios_routes import usuarios_bp
from .proveedores_routes import proveedores_bp
from .metodo_pago_routes import metodos_pago_bp
from .orden_compra_routes import ordenes_compra_bp
from .documento_inventarios_routes import documentos_inventario_bp
from .auth_routes import auth_bp


all_blueprints = [
    productos_bp,
    categorias_bp,
    roles_bp,
    facturas_bp,
    detalle_facturas_bp,
    clientes_bp,
    usuarios_bp,
    proveedores_bp,
    metodos_pago_bp,
    ordenes_compra_bp,
    documentos_inventario_bp,
    auth_bp
]
