CREATE DATABASE IF NOT EXISTS techespinoza_db;
USE techespinoza_db;

CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(100) NOT NULL UNIQUE,
    contrasena VARCHAR(255) NOT NULL,
    rol VARCHAR(30) NOT NULL DEFAULT 'usuario'
);

CREATE TABLE IF NOT EXISTS equipos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(50) NOT NULL UNIQUE,
    nombre VARCHAR(150) NOT NULL,
    marca VARCHAR(100),
    modelo VARCHAR(100),
    serie VARCHAR(100),
    estado VARCHAR(50) DEFAULT 'Disponible',
    ubicacion VARCHAR(150),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
