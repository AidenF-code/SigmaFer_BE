-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 26-08-2026 a las 05:20:40
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `sigmafer`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `categorias`
--

CREATE TABLE `categorias` (
  `id` int(11) NOT NULL,
  `nombre` varchar(150) NOT NULL,
  `estado` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

--
-- Volcado de datos para la tabla `categorias`
--

INSERT INTO `categorias` (`id`, `nombre`, `estado`) VALUES
(1, 'Productos Abrasivos', 'Activo'),
(2, 'Herramienta Eléctrica', 'Activo'),
(3, 'Herramienta Manual', 'Activo'),
(4, 'Elementos De Protección Personal', NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `clientes`
--

CREATE TABLE `clientes` (
  `id` int(11) NOT NULL,
  `razon_social` varchar(150) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `tipo_documento` varchar(10) NOT NULL,
  `numero_identificacion` varchar(20) NOT NULL,
  `correo` varchar(100) NOT NULL,
  `telefono` varchar(20) NOT NULL,
  `direccion` varchar(200) NOT NULL,
  `estado` tinyint(1) NOT NULL,
  `fecha_creacion` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

--
-- Volcado de datos para la tabla `clientes`
--

INSERT INTO `clientes` (`id`, `razon_social`, `nombre`, `tipo_documento`, `numero_identificacion`, `correo`, `telefono`, `direccion`, `estado`, `fecha_creacion`) VALUES
(1, 'Ferre-Electricos AAA', 'Alduin Garcia', 'NIT', '927384566-0', 'ferrecontacto@gmail.com', '0614898999', 'Av Siempre Viva 123', 1, '2026-08-25'),
(2, 'Ferreteria El Constructor', 'Juan Carlos Perez', 'CC', '1029384756', 'contacto.constructor@gmail.com', '6017348291', 'Calle 18 # 12 - 45', 0, '2026-08-25'),
(3, 'Distribuciones La 80', 'Laura Martinez', 'CC', '52938471', 'laura.martinez@gmail.com', '6018457326', 'Carrera 80 # 24 - 18', 1, '2026-08-25'),
(4, 'Insumos Industriales Colombia', 'Andres Rodriguez', 'NIT', '901283746-5', 'contacto@insumosindustriales.com', '6019283746', 'Calle 72 # 16 - 32', 1, '2026-08-25'),
(5, 'Comercializadora El Progreso', 'Maria Fernanda Torres', 'CC', '1018273645', 'maria.torres@gmail.com', '6016372918', 'Carrera 15 # 35 - 21', 1, '2026-08-25'),
(6, 'Soluciones Electricas del Norte', 'Carlos Alberto Gomez', 'CC', '79836251', 'carlos.gomez@gmail.com', '6017293845', 'Calle 45 # 8 - 67', 1, '2026-08-25'),
(7, 'Importaciones Andinas S.A.S.', 'Sofia Ramirez', 'NIT', '900738291-4', 'contacto@importacionesandinas.com', '6018364927', 'Carrera 30 # 68 - 14', 1, '2026-08-25'),
(8, 'Tecnologia y Suministros S.A.S.', 'Diego Hernandez', 'CE', 'E12345678', 'diego.hernandez@gmail.com', '6019182736', 'Calle 26 # 42 - 19', 1, '2026-08-25'),
(9, 'Materiales La Sabana', 'Natalia Castillo', 'CC', '1037482916', 'natalia.castillo@gmail.com', '6015827364', 'Carrera 9 # 17 - 53', 1, '2026-08-25'),
(10, 'Grupo Comercial del Centro', 'Felipe Moreno', 'CC', '80192736', 'felipe.moreno@gmail.com', '6017463829', 'Calle 13 # 6 - 28', 1, '2026-08-25'),
(11, 'Servicios Industriales Globales', 'Emily Johnson', 'CE', 'E98765432', 'emily.johnson@gmail.com', '6018293647', 'Carrera 68 # 25 - 41', 1, '2026-08-25');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalle_doc_inventario`
--

CREATE TABLE `detalle_doc_inventario` (
  `id` int(11) NOT NULL,
  `cantidad` int(11) NOT NULL,
  `valor_unitario` decimal(12,2) NOT NULL,
  `valor_total` decimal(12,2) NOT NULL,
  `documento_id` int(11) NOT NULL,
  `producto_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

--
-- Volcado de datos para la tabla `detalle_doc_inventario`
--

INSERT INTO `detalle_doc_inventario` (`id`, `cantidad`, `valor_unitario`, `valor_total`, `documento_id`, `producto_id`) VALUES
(1, 10, 27000.00, 270000.00, 1, 8),
(2, 1000, 1200.00, 1200000.00, 1, 1),
(3, 1000, 1100.00, 1100000.00, 1, 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalle_facturas`
--

CREATE TABLE `detalle_facturas` (
  `id` int(11) NOT NULL,
  `cantidad` int(11) NOT NULL,
  `valor_unitario` decimal(12,2) NOT NULL,
  `subtotal` decimal(12,2) NOT NULL,
  `iva` decimal(12,2) NOT NULL,
  `iva_porcentaje` decimal(5,2) NOT NULL,
  `valor_total` decimal(12,2) NOT NULL,
  `factura_id` int(11) NOT NULL,
  `producto_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

--
-- Volcado de datos para la tabla `detalle_facturas`
--

INSERT INTO `detalle_facturas` (`id`, `cantidad`, `valor_unitario`, `subtotal`, `iva`, `iva_porcentaje`, `valor_total`, `factura_id`, `producto_id`) VALUES
(1, 100, 5800.00, 580000.00, 110200.00, 19.00, 690200.00, 1, 4),
(2, 1500, 1200.00, 1800000.00, 342000.00, 19.00, 2142000.00, 1, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalle_oc`
--

CREATE TABLE `detalle_oc` (
  `id` int(11) NOT NULL,
  `cantidad` int(11) NOT NULL,
  `valor_unitario` decimal(12,2) NOT NULL,
  `valor_total` decimal(12,2) NOT NULL,
  `orden_compra_id` int(11) NOT NULL,
  `producto_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

--
-- Volcado de datos para la tabla `detalle_oc`
--

INSERT INTO `detalle_oc` (`id`, `cantidad`, `valor_unitario`, `valor_total`, `orden_compra_id`, `producto_id`) VALUES
(1, 10, 27000.00, 270000.00, 1, 8),
(2, 1000, 1200.00, 1200000.00, 1, 1),
(3, 15, 210000.00, 3150000.00, 1, 6);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `documento_inventario`
--

CREATE TABLE `documento_inventario` (
  `id` int(11) NOT NULL,
  `numero_documento` varchar(50) NOT NULL,
  `tipo_documento` enum('ENTRADA','SALIDA','DEVOLUCION','AJUSTE') NOT NULL,
  `fecha_creacion` date NOT NULL,
  `observaciones` varchar(200) DEFAULT NULL,
  `estado` tinyint(1) NOT NULL,
  `cliente_id` int(11) DEFAULT NULL,
  `proveedor_id` int(11) DEFAULT NULL,
  `usuario_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

--
-- Volcado de datos para la tabla `documento_inventario`
--

INSERT INTO `documento_inventario` (`id`, `numero_documento`, `tipo_documento`, `fecha_creacion`, `observaciones`, `estado`, `cliente_id`, `proveedor_id`, `usuario_id`) VALUES
(1, 'CO-00001', 'ENTRADA', '2026-08-25', 'Factura Proveedor: 236512 | Orden Compra: OC-00001', 1, NULL, 1, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `facturas`
--

CREATE TABLE `facturas` (
  `id` int(11) NOT NULL,
  `numero_factura` varchar(50) NOT NULL,
  `fecha_emision` date NOT NULL,
  `subtotal` decimal(10,2) NOT NULL,
  `iva` decimal(10,2) NOT NULL,
  `total` decimal(10,2) NOT NULL,
  `observaciones` varchar(200) DEFAULT NULL,
  `estado_pago` tinyint(1) NOT NULL,
  `cliente_id` int(11) NOT NULL,
  `usuario_id` int(11) NOT NULL,
  `metodo_pago_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

--
-- Volcado de datos para la tabla `facturas`
--

INSERT INTO `facturas` (`id`, `numero_factura`, `fecha_emision`, `subtotal`, `iva`, `total`, `observaciones`, `estado_pago`, `cliente_id`, `usuario_id`, `metodo_pago_id`) VALUES
(1, 'FV-000001', '2026-08-25', 2380000.00, 452200.00, 2832200.00, '', 0, 1, 4, 3);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `metodo_pago`
--

CREATE TABLE `metodo_pago` (
  `id` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `estado` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

--
-- Volcado de datos para la tabla `metodo_pago`
--

INSERT INTO `metodo_pago` (`id`, `nombre`, `estado`) VALUES
(1, 'Efectivo', 1),
(2, 'Cheque', 1),
(3, 'Crédito - 30 días', 1),
(4, 'Crédito - 60 días', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `orden_compra`
--

CREATE TABLE `orden_compra` (
  `id` int(11) NOT NULL,
  `numero_orden` varchar(50) NOT NULL,
  `fecha_creacion` date NOT NULL,
  `observaciones` varchar(200) DEFAULT NULL,
  `estado` tinyint(1) NOT NULL,
  `subtotal` decimal(12,2) NOT NULL,
  `total` decimal(12,2) NOT NULL,
  `proveedor_id` int(11) NOT NULL,
  `usuario_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

--
-- Volcado de datos para la tabla `orden_compra`
--

INSERT INTO `orden_compra` (`id`, `numero_orden`, `fecha_creacion`, `observaciones`, `estado`, `subtotal`, `total`, `proveedor_id`, `usuario_id`) VALUES
(1, 'OC-00001', '2026-08-25', '', 1, 4620000.00, 4620000.00, 1, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `productos`
--

CREATE TABLE `productos` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `codigo` varchar(50) NOT NULL,
  `stock` decimal(12,2) NOT NULL,
  `stock_minimo` decimal(12,2) NOT NULL,
  `stock_maximo` decimal(12,2) DEFAULT NULL,
  `precio` decimal(12,2) NOT NULL,
  `estado` tinyint(1) NOT NULL,
  `fecha_creacion` date NOT NULL,
  `categoria_id` int(11) NOT NULL,
  `proveedor_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

--
-- Volcado de datos para la tabla `productos`
--

INSERT INTO `productos` (`id`, `nombre`, `codigo`, `stock`, `stock_minimo`, `stock_maximo`, `precio`, `estado`, `fecha_creacion`, `categoria_id`, `proveedor_id`) VALUES
(1, 'Lija Premier Red # 80', 'C1LS0001', 2480.00, 2500.00, 10000.00, 1200.00, 1, '2026-08-25', 1, 1),
(2, 'Lija Premier Red # 120', 'C1LS0002', 4200.00, 2500.00, 10000.00, 1100.00, 1, '2026-08-25', 1, 1),
(3, 'Disco de Corte Metal 4 1/2\"', 'C1DC0003', 850.00, 500.00, 3000.00, 4500.00, 1, '2026-08-25', 1, 2),
(4, 'Disco Flap Grano 60', 'C1DF0004', 520.00, 400.00, 2500.00, 5800.00, 1, '2026-08-25', 1, 3),
(5, 'Taladro Percutor 1/2\" 650W', 'C2TP0001', 45.00, 20.00, 100.00, 185000.00, 1, '2026-08-25', 2, 2),
(6, 'Pulidora Angular 4 1/2\" 900W', 'C2PA0002', 32.00, 15.00, 80.00, 210000.00, 1, '2026-08-25', 2, 4),
(7, 'Juego de Destornilladores 6 Piezas', 'C3DD0001', 75.00, 30.00, 150.00, 38500.00, 1, '2026-08-25', 3, 1),
(8, 'Alicate Universal 8\"', 'C3AU0002', 100.00, 35.00, 180.00, 27000.00, 1, '2026-08-25', 3, 3),
(9, 'Martillo de Uña 16 Oz', 'C3MU0003', 55.00, 25.00, 120.00, 32000.00, 1, '2026-08-25', 3, 4),
(10, 'Guantes de Seguridad Antideslizantes', 'C4GS0001', 180.00, 80.00, 400.00, 12500.00, 1, '2026-08-25', 4, 2),
(11, 'Gafas de Seguridad Transparentes', 'C4GS0002', 210.00, 100.00, 500.00, 8500.00, 1, '2026-08-25', 4, 3),
(12, 'Lija Premier Red # 180', 'C1LS0005', 2750.00, 2000.00, 9000.00, 1250.00, 1, '2026-08-25', 1, 1),
(13, 'Disco de Corte Acero Inoxidable 4 1/2\"', 'C1DC0006', 740.00, 400.00, 2500.00, 5200.00, 1, '2026-08-25', 1, 3),
(14, 'Piedra de Esmeril Grano 80', 'C1PE0007', 380.00, 200.00, 1000.00, 9800.00, 1, '2026-08-25', 1, 4),
(15, 'Esmeril Angular 7\" 2200W', 'C2EA0003', 28.00, 10.00, 60.00, 385000.00, 1, '2026-08-25', 2, 2),
(16, 'Atornillador Inalámbrico 12V', 'C2AI0004', 38.00, 15.00, 80.00, 165000.00, 1, '2026-08-25', 2, 4),
(17, 'Llave Inglesa Ajustable 10\"', 'C3LI0004', 65.00, 25.00, 130.00, 29500.00, 1, '2026-08-25', 3, 1),
(18, 'Juego de Llaves Combinadas 8 Piezas', 'C3LC0005', 42.00, 15.00, 90.00, 72000.00, 1, '2026-08-25', 3, 3),
(19, 'Cinta Métrica 5 Metros', 'C3CM0006', 110.00, 40.00, 220.00, 18000.00, 1, '2026-08-25', 3, 4),
(20, 'Casco de Seguridad Industrial', 'C4CS0003', 95.00, 40.00, 200.00, 28500.00, 1, '2026-08-25', 4, 2),
(21, 'Protector Auditivo Tipo Copa', 'C4PA0004', 70.00, 30.00, 150.00, 36000.00, 1, '2026-08-25', 4, 3),
(22, 'Lija de Agua Grano # 220', 'C1LA0008', 2400.00, 1800.00, 8000.00, 1350.00, 1, '2026-08-25', 1, 2),
(23, 'Disco Diamantado para Concreto 4 1/2\"', 'C1DD0009', 420.00, 200.00, 1200.00, 18500.00, 1, '2026-08-25', 1, 4),
(24, 'Rueda de Lija Abrasiva 6\"', 'C1RL0010', 310.00, 150.00, 800.00, 14500.00, 1, '2026-08-25', 1, 1),
(25, 'Sierra Circular 7 1/4\" 1400W', 'C2SC0005', 24.00, 10.00, 60.00, 425000.00, 1, '2026-08-25', 2, 3),
(26, 'Lijadora Orbital 240W', 'C2LO0006', 35.00, 15.00, 75.00, 195000.00, 1, '2026-08-25', 2, 1),
(27, 'Juego de Llaves Allen 10 Piezas', 'C3LL0007', 85.00, 30.00, 180.00, 26000.00, 1, '2026-08-25', 3, 2),
(28, 'Tenaza para Electricista 9\"', 'C3TE0008', 58.00, 25.00, 120.00, 34000.00, 1, '2026-08-25', 3, 4),
(29, 'Nivel de Burbuja 24\"', 'C3NB0009', 48.00, 20.00, 100.00, 42000.00, 1, '2026-08-25', 3, 3),
(30, 'Chaleco Reflectivo Industrial', 'C4CR0005', 130.00, 50.00, 300.00, 17500.00, 1, '2026-08-25', 4, 1),
(31, 'Tapabocas Industrial N95', 'C4TN0006', 450.00, 200.00, 1000.00, 4500.00, 1, '2026-08-25', 4, 4);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `proveedores`
--

CREATE TABLE `proveedores` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `direccion` varchar(200) NOT NULL,
  `telefono` varchar(20) NOT NULL,
  `correo` varchar(100) NOT NULL,
  `nit` varchar(25) NOT NULL,
  `estado` tinyint(1) NOT NULL,
  `fecha_creacion` date NOT NULL,
  `nombre_contacto` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

--
-- Volcado de datos para la tabla `proveedores`
--

INSERT INTO `proveedores` (`id`, `nombre`, `direccion`, `telefono`, `correo`, `nit`, `estado`, `fecha_creacion`, `nombre_contacto`) VALUES
(1, 'Carborundum', 'Calle 23 # 20 - 56', '0618569317', 'contacto.carborundum@gmail.com', '9561925-9', 1, '2026-08-25', 'Lizeth Galindo'),
(2, 'Ferremax', 'Carrera 15 # 18 - 42', '6017421836', 'contacto.ferremax@gmail.com', '901284736-1', 1, '2026-08-25', 'Carlos Méndez'),
(3, 'Distribuciones Andinas', 'Calle 12 # 34 - 18', '6018352749', 'ventas.distribucionesandinas@gmail.com', '900738291-6', 1, '2026-08-25', 'Mariana Rodríguez'),
(4, 'Suministros El Dorado', 'Carrera 7 # 45 - 23', '6016249185', 'contacto.suministroeldorado@gmail.com', '901563827-4', 1, '2026-08-25', 'Andrés Castillo'),
(5, 'Proveedora Industrial Bogotá', 'Calle 80 # 25 - 67', '6019183652', 'ventas.proindustrial@gmail.com', '900482615-8', 1, '2026-08-25', 'Natalia Torres');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `rol`
--

CREATE TABLE `rol` (
  `id` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `permisos` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`permisos`))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

--
-- Volcado de datos para la tabla `rol`
--

INSERT INTO `rol` (`id`, `nombre`, `permisos`) VALUES
(1, 'Facturacion', '{\"facturacion\": {\"facturas\": {\"ver\": true, \"crear\": true}, \"clientes\": {\"ver\": true, \"crear\": true, \"editar\": true}}, \"inventarios\": {\"productos\": {\"ver\": true}}}'),
(2, 'Administrador', '{\"administracion\": {\"usuarios\": {\"ver\": true, \"crear\": true, \"editar\": true}, \"roles\": {\"ver\": true, \"crear\": true, \"editar\": true}}, \"facturacion\": {\"facturas\": {\"ver\": true, \"crear\": true, \"editar\": true}, \"clientes\": {\"ver\": true, \"crear\": true, \"editar\": true}, \"metodos\": {\"pago_ver\": true, \"pago_crear\": true, \"pago_editar\": true}}, \"inventarios\": {\"productos\": {\"ver\": true, \"crear\": true, \"editar\": true}, \"proveedores\": {\"ver\": true, \"crear\": true, \"editar\": true}, \"entradas\": {\"ver\": true, \"crear\": true}, \"salidas\": {\"ver\": true, \"crear\": true}, \"devoluciones\": {\"ver\": true, \"crear\": true}, \"ordenes\": {\"compra_ver\": true, \"compra_crear\": true}}}'),
(3, 'Almacenista', '{\"facturacion\": {\"facturas\": {\"ver\": true}, \"clientes\": {\"ver\": true}}, \"inventarios\": {\"productos\": {\"ver\": true, \"crear\": true, \"editar\": true}, \"proveedores\": {\"ver\": true, \"crear\": true, \"editar\": true}, \"entradas\": {\"ver\": true, \"crear\": true}, \"salidas\": {\"ver\": true, \"crear\": true}, \"devoluciones\": {\"ver\": true, \"crear\": true}, \"ordenes\": {\"compra_ver\": true, \"compra_crear\": true}}}'),
(4, 'Vendedor', '{\"facturacion\": {\"facturas\": {\"ver\": true}, \"clientes\": {\"ver\": true}}, \"inventarios\": {\"productos\": {\"ver\": true}}}');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `identificacion` varchar(20) NOT NULL,
  `correo` varchar(100) NOT NULL,
  `telefono` varchar(20) NOT NULL,
  `password` varchar(255) NOT NULL,
  `estado` tinyint(1) NOT NULL,
  `primer_ingreso` tinyint(1) NOT NULL,
  `fecha_creacion` date NOT NULL,
  `rol_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id`, `nombre`, `identificacion`, `correo`, `telefono`, `password`, `estado`, `primer_ingreso`, `fecha_creacion`, `rol_id`) VALUES
(1, 'Andres Fernandez', '1022397751', 'andresfernandez@gmail.com', '3103421090', 'scrypt:32768:8:1$JyMJarkuObCgGiUc$3fcf0cfe22dad29f23f040f5d6c7e06300e99820f7139d02060039d6f27d7491e34e41ac3bcd7f077f62fdf3fc29407e71d407b19a208c2929f0e2e0d0dedf80', 1, 0, '2026-08-25', 2),
(2, 'Edison Arias', '9587416', 'ediAri@gmail.com', '3265987415', 'scrypt:32768:8:1$qIj3Oer6x0kdlwvt$0dac9646df58605b761dc7d5d9cbaf61cc19d9318ab502a1a9e31743dff5890d894dd2eaec4fbf1650b7eff4aedef4d5aeee03c8e0a5097acc6822a4f233c13f', 1, 1, '2026-08-25', 1),
(3, 'Lina Hernández', '7856412', 'linahernandez@gmail.com', '3208754695', 'scrypt:32768:8:1$I3MCmdqPaJ69Bogj$f4bb108915447fa9e8d0779c6516b086f0d203fd697dc246656cacc82ff1a773013df8cd87c49e2d5e545165cedadd633b07422f03fdce292cbca9c150554b91', 1, 1, '2026-08-25', 3),
(4, 'Hernan Pineda', '92642746', 'hernan.pineda@gmail.com', '3215896741', 'scrypt:32768:8:1$kXBempBiszWfn25J$e60259c8de9a85d12f2aec050638577a0806f770696e10616f38e8cf9f0d9ad1f47dbc51b0b3fe85d5a9b64bdad9537fab330cba883db9d682d4e438839372cc', 1, 1, '2026-08-25', 4),
(5, 'Diana Calderon', '1003688485', 'dian.calderon@gmail.com', '3235896741', '000000000', 1, 0, '2026-08-25', 4);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `categorias`
--
ALTER TABLE `categorias`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `clientes`
--
ALTER TABLE `clientes`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `numero_identificacion` (`numero_identificacion`),
  ADD UNIQUE KEY `correo` (`correo`);

--
-- Indices de la tabla `detalle_doc_inventario`
--
ALTER TABLE `detalle_doc_inventario`
  ADD PRIMARY KEY (`id`),
  ADD KEY `documento_id` (`documento_id`),
  ADD KEY `producto_id` (`producto_id`);

--
-- Indices de la tabla `detalle_facturas`
--
ALTER TABLE `detalle_facturas`
  ADD PRIMARY KEY (`id`),
  ADD KEY `factura_id` (`factura_id`),
  ADD KEY `producto_id` (`producto_id`);

--
-- Indices de la tabla `detalle_oc`
--
ALTER TABLE `detalle_oc`
  ADD PRIMARY KEY (`id`),
  ADD KEY `orden_compra_id` (`orden_compra_id`),
  ADD KEY `producto_id` (`producto_id`);

--
-- Indices de la tabla `documento_inventario`
--
ALTER TABLE `documento_inventario`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `numero_documento` (`numero_documento`),
  ADD KEY `cliente_id` (`cliente_id`),
  ADD KEY `proveedor_id` (`proveedor_id`),
  ADD KEY `usuario_id` (`usuario_id`);

--
-- Indices de la tabla `facturas`
--
ALTER TABLE `facturas`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `numero_factura` (`numero_factura`),
  ADD KEY `cliente_id` (`cliente_id`),
  ADD KEY `usuario_id` (`usuario_id`),
  ADD KEY `metodo_pago_id` (`metodo_pago_id`);

--
-- Indices de la tabla `metodo_pago`
--
ALTER TABLE `metodo_pago`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `nombre` (`nombre`);

--
-- Indices de la tabla `orden_compra`
--
ALTER TABLE `orden_compra`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `numero_orden` (`numero_orden`),
  ADD KEY `proveedor_id` (`proveedor_id`),
  ADD KEY `usuario_id` (`usuario_id`);

--
-- Indices de la tabla `productos`
--
ALTER TABLE `productos`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `codigo` (`codigo`),
  ADD KEY `categoria_id` (`categoria_id`),
  ADD KEY `proveedor_id` (`proveedor_id`);

--
-- Indices de la tabla `proveedores`
--
ALTER TABLE `proveedores`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `correo` (`correo`),
  ADD UNIQUE KEY `nit` (`nit`);

--
-- Indices de la tabla `rol`
--
ALTER TABLE `rol`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `identificacion` (`identificacion`),
  ADD UNIQUE KEY `correo` (`correo`),
  ADD UNIQUE KEY `telefono` (`telefono`),
  ADD KEY `rol_id` (`rol_id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `categorias`
--
ALTER TABLE `categorias`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `clientes`
--
ALTER TABLE `clientes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT de la tabla `detalle_doc_inventario`
--
ALTER TABLE `detalle_doc_inventario`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `detalle_facturas`
--
ALTER TABLE `detalle_facturas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `detalle_oc`
--
ALTER TABLE `detalle_oc`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `documento_inventario`
--
ALTER TABLE `documento_inventario`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `facturas`
--
ALTER TABLE `facturas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `metodo_pago`
--
ALTER TABLE `metodo_pago`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `orden_compra`
--
ALTER TABLE `orden_compra`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `productos`
--
ALTER TABLE `productos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=32;

--
-- AUTO_INCREMENT de la tabla `proveedores`
--
ALTER TABLE `proveedores`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `rol`
--
ALTER TABLE `rol`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `detalle_doc_inventario`
--
ALTER TABLE `detalle_doc_inventario`
  ADD CONSTRAINT `detalle_doc_inventario_ibfk_1` FOREIGN KEY (`documento_id`) REFERENCES `documento_inventario` (`id`),
  ADD CONSTRAINT `detalle_doc_inventario_ibfk_2` FOREIGN KEY (`producto_id`) REFERENCES `productos` (`id`);

--
-- Filtros para la tabla `detalle_facturas`
--
ALTER TABLE `detalle_facturas`
  ADD CONSTRAINT `detalle_facturas_ibfk_1` FOREIGN KEY (`factura_id`) REFERENCES `facturas` (`id`),
  ADD CONSTRAINT `detalle_facturas_ibfk_2` FOREIGN KEY (`producto_id`) REFERENCES `productos` (`id`);

--
-- Filtros para la tabla `detalle_oc`
--
ALTER TABLE `detalle_oc`
  ADD CONSTRAINT `detalle_oc_ibfk_1` FOREIGN KEY (`orden_compra_id`) REFERENCES `orden_compra` (`id`),
  ADD CONSTRAINT `detalle_oc_ibfk_2` FOREIGN KEY (`producto_id`) REFERENCES `productos` (`id`);

--
-- Filtros para la tabla `documento_inventario`
--
ALTER TABLE `documento_inventario`
  ADD CONSTRAINT `documento_inventario_ibfk_1` FOREIGN KEY (`cliente_id`) REFERENCES `clientes` (`id`),
  ADD CONSTRAINT `documento_inventario_ibfk_2` FOREIGN KEY (`proveedor_id`) REFERENCES `proveedores` (`id`),
  ADD CONSTRAINT `documento_inventario_ibfk_3` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`);

--
-- Filtros para la tabla `facturas`
--
ALTER TABLE `facturas`
  ADD CONSTRAINT `facturas_ibfk_1` FOREIGN KEY (`cliente_id`) REFERENCES `clientes` (`id`),
  ADD CONSTRAINT `facturas_ibfk_2` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`),
  ADD CONSTRAINT `facturas_ibfk_3` FOREIGN KEY (`metodo_pago_id`) REFERENCES `metodo_pago` (`id`);

--
-- Filtros para la tabla `orden_compra`
--
ALTER TABLE `orden_compra`
  ADD CONSTRAINT `orden_compra_ibfk_1` FOREIGN KEY (`proveedor_id`) REFERENCES `proveedores` (`id`),
  ADD CONSTRAINT `orden_compra_ibfk_2` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`);

--
-- Filtros para la tabla `productos`
--
ALTER TABLE `productos`
  ADD CONSTRAINT `productos_ibfk_1` FOREIGN KEY (`categoria_id`) REFERENCES `categorias` (`id`),
  ADD CONSTRAINT `productos_ibfk_2` FOREIGN KEY (`proveedor_id`) REFERENCES `proveedores` (`id`);

--
-- Filtros para la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD CONSTRAINT `usuarios_ibfk_1` FOREIGN KEY (`rol_id`) REFERENCES `rol` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
