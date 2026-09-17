-- =====================================================
-- ESTRUTURA DO BANCO - trabalhonp1
-- Sistema de Gestão e Reserva de Áreas Comuns em Condomínio
-- =====================================================

CREATE DATABASE trabalhonp1
GO

USE trabalhonp1
GO

CREATE TABLE USUARIO (
    id_usuario INT IDENTITY(1,1) PRIMARY KEY,
    email VARCHAR(100) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL,
    tipo_usuario VARCHAR(20) NOT NULL,
    status VARCHAR(20) NOT NULL,

    CONSTRAINT CK_USUARIO_TIPO
        CHECK (tipo_usuario IN ('ADMINISTRADOR', 'MORADOR')),

    CONSTRAINT CK_USUARIO_STATUS
        CHECK (status IN ('ATIVO', 'INATIVO'))
);
GO

CREATE TABLE MORADOR (
    id_morador INT IDENTITY(1,1) PRIMARY KEY,
    id_usuario INT NOT NULL UNIQUE,
    nome VARCHAR(100) NOT NULL,
    cpf CHAR(11) NOT NULL UNIQUE,
    telefone VARCHAR(15) NOT NULL,
    bloco VARCHAR(10) NOT NULL,
    apartamento VARCHAR(10) NOT NULL,

    CONSTRAINT FK_MORADOR_USUARIO
        FOREIGN KEY (id_usuario)
        REFERENCES USUARIO(id_usuario)
);
GO

CREATE TABLE AREA_COMUM (
    id_area INT IDENTITY(1,1) PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE,
    descricao VARCHAR(255),
    capacidade INT NOT NULL,
    status VARCHAR(20) NOT NULL,

    CONSTRAINT CK_AREA_CAPACIDADE
        CHECK (capacidade > 0),

    CONSTRAINT CK_AREA_STATUS
        CHECK (status IN ('ATIVA', 'INATIVA'))
);
GO

CREATE TABLE RESERVA (
    id_reserva INT IDENTITY(1,1) PRIMARY KEY,
    id_morador INT NOT NULL,
    id_area INT NOT NULL,
    data_reserva DATE NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fim TIME NOT NULL,
    status VARCHAR(20) NOT NULL,

    CONSTRAINT FK_RESERVA_MORADOR
        FOREIGN KEY (id_morador)
        REFERENCES MORADOR(id_morador),

    CONSTRAINT FK_RESERVA_AREA
        FOREIGN KEY (id_area)
        REFERENCES AREA_COMUM(id_area),

    CONSTRAINT CK_RESERVA_HORARIO
        CHECK (hora_fim > hora_inicio),

    CONSTRAINT CK_RESERVA_STATUS
        CHECK (status IN ('ATIVA', 'CANCELADA'))
);
GO
