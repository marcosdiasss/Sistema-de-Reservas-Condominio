
-- DADOS DE TESTE - trabalhonp1 

USE trabalhonp1
GO


-- 1) USUÁRIOS

-- Administrador (não terá registro em MORADOR)
INSERT INTO USUARIO (email, senha, tipo_usuario, status)
VALUES ('admin@condominio.com', 'admin123', 'ADMINISTRADOR', 'ATIVO');

-- Morador 1
INSERT INTO USUARIO (email, senha, tipo_usuario, status)
VALUES ('joao.silva@email.com', '123456', 'MORADOR', 'ATIVO');

-- Morador 2
INSERT INTO USUARIO (email, senha, tipo_usuario, status)
VALUES ('maria.souza@email.com', '123456', 'MORADOR', 'ATIVO');

-- Morador 3 (INATIVO, para testar bloqueio de login)
INSERT INTO USUARIO (email, senha, tipo_usuario, status)
VALUES ('carlos.pereira@email.com', '123456', 'MORADOR', 'INATIVO');
GO




INSERT INTO MORADOR (id_usuario, nome, cpf, telefone, bloco, apartamento)
VALUES (2, 'João Silva', '11122233344', '(11) 91111-1111', 'A', '101');

INSERT INTO MORADOR (id_usuario, nome, cpf, telefone, bloco, apartamento)
VALUES (3, 'Maria Souza', '22233344455', '(11) 92222-2222', 'B', '202');

INSERT INTO MORADOR (id_usuario, nome, cpf, telefone, bloco, apartamento)
VALUES (4, 'Carlos Pereira', '33344455566', '(11) 93333-3333', 'C', '303');
GO


-- 3) ÁREAS COMUNS


INSERT INTO AREA_COMUM (nome, descricao, capacidade, status)
VALUES ('Salão de Festas', 'Salão para eventos e comemorações', 50, 'ATIVA');

INSERT INTO AREA_COMUM (nome, descricao, capacidade, status)
VALUES ('Churrasqueira', 'Área de churrasqueira coberta', 20, 'ATIVA');

-- Área INATIVA (para testar RN06 - não pode reservar área inativa)
INSERT INTO AREA_COMUM (nome, descricao, capacidade, status)
VALUES ('Quadra Poliesportiva', 'Quadra em reforma', 30, 'INATIVA');
GO


-- 4) RESERVAS


-- Reserva válida e ativa (João reservou o Salão)
INSERT INTO RESERVA (id_morador, id_area, data_reserva, hora_inicio, hora_fim, status)
VALUES (1, 1, '2026-09-20', '18:00', '22:00', 'ATIVA');

-- Reserva válida e ativa, encostando exatamente no horário final da anterior
-- (Maria reserva o mesmo Salão das 22:00 às 23:00 -> permitido pela RN05)
INSERT INTO RESERVA (id_morador, id_area, data_reserva, hora_inicio, hora_fim, status)
VALUES (2, 1, '2026-09-20', '22:00', '23:00', 'ATIVA');

-- Reserva ativa da Churrasqueira (Maria)
INSERT INTO RESERVA (id_morador, id_area, data_reserva, hora_inicio, hora_fim, status)
VALUES (2, 2, '2026-09-21', '12:00', '16:00', 'ATIVA');

-- Reserva CANCELADA (para demonstrar que o registro não é apagado, só muda status)
INSERT INTO RESERVA (id_morador, id_area, data_reserva, hora_inicio, hora_fim, status)
VALUES (1, 2, '2026-09-22', '10:00', '14:00', 'CANCELADA');
GO
