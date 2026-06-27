from flask import Blueprint, jsonify, request
from src.models.clientes import Clientes

clientes_bp = Blueprint('clientes', __name__)

@clientes_bp.route('/', methods=['GET'])#Todos los clientes
def get_clientes():
    clientes = Clientes.get()
    clientes_list = []
    for cliente in clientes:
        clientes_list.append({
            'id': cliente.id,
            'razonsocial': cliente.razonsocial,
            'nombre': cliente.nombre,
            'identificacion': cliente.identificacion,
            'correo': cliente.correo,
            'telefono': cliente.telefono,
            'direccion': cliente.direccion,
            'nit': cliente.nit,
            'estado': cliente.estado,
            'fecha_creacion': cliente.fecha_creacion.isoformat()
        })
    return jsonify(clientes_list), 200


@clientes_bp.route('/<int:id>', methods=['GET']) #Cliente por ID
def get_cliente(id):
    cliente = Clientes.get_by_id(id)
    if cliente:
        cliente_data = {
            'id': cliente.id,
            'razonsocial': cliente.razonsocial,
            'nombre': cliente.nombre,
            'identificacion': cliente.identificacion,
            'correo': cliente.correo,
            'telefono': cliente.telefono,
            'direccion': cliente.direccion,
            'nit': cliente.nit,
            'estado': cliente.estado,
            'fecha_creacion': cliente.fecha_creacion.isoformat()
        }
        return jsonify(cliente_data), 200
    else:
        return jsonify({'message': 'Cliente no encontrado'}), 404
    

@clientes_bp.route('/', methods=['POST']) #Crear cliente
def create_cliente():
    data = request.get_json()

    if not data:
        return jsonify({'message': 'No se proporcionaron datos'}), 400

    # Validación de datos requeridos
    # Validación del campo "razonsocial"
    razonsocial = data.get('razonsocial', '').strip()
    if not razonsocial:
        return jsonify({'message': 'El campo "razonsocial" es obligatorio'}), 400
    razonsocial_existente = Clientes.get_by_razonsocial(razonsocial)
    if razonsocial_existente:
        return jsonify({'message': 'Ya existe un cliente con esa razón social'}), 400
    
    # Validación del campo "nit"
    nit = data.get('nit', '').strip()
    if not nit:
        return jsonify({'message': 'El campo "nit" es obligatorio'}), 400
    nit_existente = Clientes.get_by_nit(nit)
    if nit_existente:
        return jsonify({'message': 'Ya existe un cliente con ese NIT'}), 400

    # Validación del campo "nombre"
    nombre = data.get('nombre', '').strip()
    if not nombre:
        return jsonify({'message': 'El campo "nombre" es obligatorio'}), 400
    
    # Validacion del campo "identificacion"
    identificacion =data.get('identificacion', '').strip()
    if not identificacion:
        return jsonify({'message': 'El campo "identificacion" es obligatorio'}), 400
    identificacion_existente =Clientes.get_by_identificacion(identificacion)
    if identificacion_existente:
        return jsonify({'message': 'Ya existe un cliente con esa identificacion'}), 400
    
    # Validacion del campo  "correo"
    correo = data.get('correo', '').strip()
    if not correo:
        return jsonify({'message': 'El campo "correo" es obligatorio'}), 400
    correo_existente = Clientes.get_by_correo(correo)
    if correo_existente:
        return jsonify({'message': 'Ya existe un cliente con esa correo'}), 400
    
    # Validacion del campo  "telefono"
    telefono = data.get('telefono', '').strip()
    if not telefono:
        return jsonify({'message': 'El campo "telefono" es obligatorio'}), 400
    telefono_existente = Clientes.get_by_telefono(telefono)
    if telefono_existente:
        return jsonify({'message': 'Ya existe un cliente con ese numero de telefono'}), 400
    
    # Validacion del campo  "direccion"
    direccion = data.get('direccion', '').strip()
    if not direccion:
        return jsonify({'message': 'El campo "direccion" es obligatorio'}), 400
    direccion_existente = Clientes.get_by_direccion(direccion)
    if direccion_existente:
        return jsonify({'message': 'Ya existe un cliente con la direccion suministrada'}), 400

    
    

    # Elementos requeridos para crear un cliente
    cliente = Clientes(
        razonsocial=razonsocial,
        nit=nit,
        nombre=nombre,
        identificacion=identificacion,
        correo=correo,
        telefono=telefono,
        direccion=direccion 
    )
    
    cliente.save()
    return jsonify({'message': 'Cliente creado exitosamente', 'cliente': cliente.to_dict()}), 201



@clientes_bp.route('/<int:id>', methods=['PUT']) #Actualizar cliente
def update_cliente(id):
    cliente = Clientes.get_by_id(id)#Busca el cliente por el ID

    if not cliente:
        return jsonify({'message': 'Cliente no encontrado'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'message': 'Datos inválidos'}), 400
    
    #Validacion de datos
    #Razon social
    razonsocial = data.get('razonsocial', '').strip()

    if not razonsocial:
        return jsonify({'message': 'El campo "razonsocial" es obligatorio'}), 400

    razonsocial_existente = Clientes.get_by_razonsocial(razonsocial)

    if razonsocial_existente and razonsocial_existente.id != id:
        return jsonify({'message': 'Ya existe un cliente con esa razón social'}), 400
    
    # Nit
    nit = data.get('nit', '').strip()

    if not nit:
        return jsonify({'message': 'El campo "nit" es obligatorio'}), 400

    nit_existente = Clientes.get_by_nit(nit)

    if nit_existente and nit_existente.id != id:
        return jsonify({'message': 'Ya existe un cliente con ese NIT'}), 400

    # Nombre
    nombre = data.get('nombre', '').strip()

    if not nombre:
        return jsonify({'message': 'El campo "nombre" es obligatorio'}), 400

    # Identificacion
    identificacion = data.get('identificacion', '').strip()

    if not identificacion:
        return jsonify({'message': 'El campo "identificacion" es obligatorio'}), 400

    identificacion_existente = Clientes.get_by_identificacion(identificacion)

    if identificacion_existente and identificacion_existente.id != id:
        return jsonify({'message': 'Ya existe un cliente con esa identificación'}), 400
    
    # Correo
    correo = data.get('correo', '').strip()

    if not correo:
        return jsonify({'message': 'El campo "correo" es obligatorio'}), 400

    correo_existente = Clientes.get_by_correo(correo)

    if correo_existente and correo_existente.id != id:
        return jsonify({'message': 'Ya existe un cliente con ese correo'}), 400
    
    # Telefono
    telefono = data.get('telefono', '').strip()

    if not telefono:
        return jsonify({'message': 'El campo "telefono" es obligatorio'}), 400

    telefono_existente = Clientes.get_by_telefono(telefono)

    if telefono_existente and telefono_existente.id != id:
        return jsonify({'message': 'Ya existe un cliente con ese número de teléfono'}), 400
    
    # Direccion
    direccion = data.get('direccion', '').strip()

    if not direccion:
        return jsonify({'message': 'El campo "direccion" es obligatorio'}), 400

    direccion_existente = Clientes.get_by_direccion(direccion)

    if direccion_existente and direccion_existente.id != id:
        return jsonify({'message': 'Ya existe un cliente con esa dirección'}), 400
    

    cliente.razonsocial = razonsocial
    cliente.nit = nit
    cliente.nombre = nombre
    cliente.identificacion = identificacion
    cliente.correo = correo
    cliente.telefono = telefono
    cliente.direccion = direccion

    cliente.save()
    return jsonify({'message': 'Cliente actualizado exitosamente', 'cliente': cliente.to_dict()}), 200
