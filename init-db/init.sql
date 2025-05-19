\connect BD_plant_sense;

CREATE TABLE sensores (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    ubicacion TEXT,
    descripcion TEXT
    creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
);

CREATE TABLE lecturas (
    id SERIAL PRIMARY KEY,
    id_sensor INTEGER REFERENCES sensores(id),
    valor INTEGER NOT NULL CHECK (valor >= 0 AND valor <= 1024),
    porcentaje_humedad NUMERIC(5,2) GENERATED ALWAYS AS ((1 - (CAST(valor AS NUMERIC)/1023)) * 100) STORED,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
