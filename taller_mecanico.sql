CREATE DATABASE IF NOT EXISTS `Taller_Mecanico`;

USE `Taller_Mecanico`;

CREATE TABLE IF NOT EXISTS `Clientes` (
    `DNI` VARCHAR(255) PRIMARY KEY,
    `Nombre` VARCHAR(255),
    `Apellido` VARCHAR(255),
    `Direccion` VARCHAR(255),
    `Telefono` VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS `Vehiculos` (
    `Patente` VARCHAR(255) PRIMARY KEY,
    `DNI` VARCHAR(255),
    `Marca` VARCHAR(255),
    `Modelo` VARCHAR(255),
    `Color` VARCHAR(255),
    FOREIGN KEY (`DNI`) REFERENCES `Clientes`(`DNI`)
);

CREATE TABLE IF NOT EXISTS `Mecanicos` (
    `Legajo` VARCHAR(255) PRIMARY KEY,
    `Nombre` VARCHAR(255),
    `Apellido` VARCHAR(255),
    `Rol` VARCHAR(255),
    `Estado` VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS `Repuestos` (
    `Id` INT PRIMARY KEY,
    `Nombre` VARCHAR(255),
    `Precio` INT,
    `Fabricante` VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS `Reparaciones` (
    `id_reparacion` INT PRIMARY KEY,
    `Fecha_entrada` DATE,
    `Hora_entrada` TIME,
    `Patente` VARCHAR(255),
    `Legajo` VARCHAR(255),
    `DNI` VARCHAR(255), 
    FOREIGN KEY (`Patente`) REFERENCES `Vehiculos`(`Patente`),
    FOREIGN KEY (`Legajo`) REFERENCES `Mecanicos`(`Legajo`),
    FOREIGN KEY (`DNI`) REFERENCES `Clientes`(`DNI`)
);

CREATE TABLE IF NOT EXISTS `Mecanico_Reparaciones` (
    `Legajo` VARCHAR(255),
    `id_reparacion` INT,
    PRIMARY KEY (`Legajo`, `id_reparacion`),
    FOREIGN KEY (`Legajo`) REFERENCES `Mecanicos`(`Legajo`),
    FOREIGN KEY (`id_reparacion`) REFERENCES `Reparaciones`(`id_reparacion`)
);

CREATE TABLE Ficha_tecnica (
    id_ficha  VARCHAR(255) PRIMARY KEY,
    dni_cliente VARCHAR(255),
    marca VARCHAR(255) NOT NULL,
    modelo VARCHAR(255) NOT NULL,
    patente VARCHAR(255) NOT NULL,
    motivo_ingreso VARCHAR(255),
    fecha_ingreso DATE
);


CREATE TABLE IF NOT EXISTS `Facturacion` (
    `id_factura` INT PRIMARY KEY AUTO_INCREMENT,
    `DNI_Cliente` VARCHAR(255),
    `Fecha_Factura` DATE,
    `Monto` DECIMAL(10, 2),
    `Estado` ENUM('Emitida', 'Anulada'),
    FOREIGN KEY (`DNI_Cliente`) REFERENCES `Clientes`(`DNI`)
);