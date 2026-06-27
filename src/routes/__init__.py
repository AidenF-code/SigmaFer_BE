from .productos_routes import productos_bp
from .categorias_routes import categorias_bp
from .roles_routes import roles_bp
from .facturas_routes import facturas_bp
from .detalle_facturas_routes import detalle_facturas_bp
from .clientes_routes import clientes_bp
from .usuarios_routes import usuarios_bp


all_blueprints = [
    productos_bp,
    categorias_bp,
    roles_bp,
    facturas_bp,
    detalle_facturas_bp,
    clientes_bp,
    usuarios_bp
]