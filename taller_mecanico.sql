CREATE DATABASE IF NOT EXISTS taller_mecanico;
USE taller_mecanico;

CREATE TABLE IF NOT EXISTS clientes (
    dni VARCHAR(255) PRIMARY KEY,
    nombre VARCHAR(255),
    apellido VARCHAR(255),
    direccion VARCHAR(255),
    telefono VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS vehiculos (
    patente VARCHAR(255) PRIMARY KEY,
    dni VARCHAR(255),
    marca VARCHAR(255),
    modelo VARCHAR(255),
    color VARCHAR(255),
    FOREIGN KEY (dni) REFERENCES clientes(dni)
);

CREATE TABLE IF NOT EXISTS mecanicos (
    legajo VARCHAR(255) PRIMARY KEY,
    nombre VARCHAR(255),
    apellido VARCHAR(255),
    rol VARCHAR(255),
    estado VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS productos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(255),
    precio INT,
    fabricante VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS reparaciones (
    id_reparacion INT PRIMARY KEY AUTO_INCREMENT,
    fecha_entrada DATE,
    hora_entrada TIME,
    patente VARCHAR(255),
    legajo VARCHAR(255),
    dni VARCHAR(255), 
    FOREIGN KEY (patente) REFERENCES vehiculos(patente),
    FOREIGN KEY (legajo) REFERENCES mecanicos(legajo),
    FOREIGN KEY (dni) REFERENCES clientes(dni)
);

CREATE TABLE IF NOT EXISTS mecanico_reparaciones (
    legajo VARCHAR(255),
    id_reparacion INT,
    PRIMARY KEY (legajo, id_reparacion),
    FOREIGN KEY (legajo) REFERENCES mecanicos(legajo),
    FOREIGN KEY (id_reparacion) REFERENCES reparaciones(id_reparacion)
);

CREATE TABLE IF NOT EXISTS ficha_tecnica (
    id_ficha  VARCHAR(255) PRIMARY KEY,
    dni_cliente VARCHAR(255),
    marca VARCHAR(255) NOT NULL,
    modelo VARCHAR(255) NOT NULL,
    patente VARCHAR(255) NOT NULL,
    motivo_ingreso VARCHAR(255),
    fecha_ingreso DATE
);

CREATE TABLE IF NOT EXISTS facturacion (
    id_factura INT PRIMARY KEY AUTO_INCREMENT,
    dni_cliente VARCHAR(255),
    fecha_factura DATE,
    monto DECIMAL(10, 2),
    estado ENUM('Emitida', 'Anulada'),
    FOREIGN KEY (dni_cliente) REFERENCES clientes(dni)
);

CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(255),
    apellido VARCHAR(255),
    usuario VARCHAR(255) UNIQUE,
    contrasena VARCHAR(255),
    rol VARCHAR(255)
);