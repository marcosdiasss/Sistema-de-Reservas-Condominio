import pyodbc

SERVIDOR = "(localdb)\\MSSQLLocalDB"
BANCO = "trabalhonp1"


def conectar():
    
    try:
        conexao = pyodbc.connect(
            "DRIVER={ODBC Driver 18 for SQL Server};"
            f"SERVER={SERVIDOR};"
            f"DATABASE={BANCO};"
            "Trusted_Connection=yes;"
            "TrustServerCertificate=yes;"
        )
        return conexao

    except pyodbc.Error as erro:
        print("Erro ao conectar no banco de dados:", erro)
        return None


def testar_conexao():
 
    conexao = conectar()

    if conexao is None:
        print("Não foi possível conectar ao banco.")
        return

    try:
        cursor = conexao.cursor()
        cursor.execute("SELECT COUNT(*) AS total_usuarios FROM USUARIO")
        resultado = cursor.fetchone()
        print("Conexão realizada com sucesso!")
        print("Total de usuários cadastrados:", resultado.total_usuarios)

    except pyodbc.Error as erro:
        print("Erro ao executar consulta de teste:", erro)

    finally:
        cursor.close()
        conexao.close()



# CONSULTAS - USUARIO

def buscar_usuario_login(email, senha):
    """
    Busca um usuário no banco pelo email e senha informados.
    Retorna um dicionário com os dados do usuário (incluindo o
    id_morador, se ele for MORADOR), ou None se não encontrar.
    """
    conexao = conectar()
    if conexao is None:
        return None

    try:
        cursor = conexao.cursor()
        cursor.execute(
            "SELECT U.id_usuario, U.email, U.tipo_usuario, U.status, M.id_morador "
            "FROM USUARIO U "
            "LEFT JOIN MORADOR M ON M.id_usuario = U.id_usuario "
            "WHERE U.email = ? AND U.senha = ?",
            email, senha
        )
        linha = cursor.fetchone()

        if linha is None:
            return None

        usuario = {
            "id_usuario": linha.id_usuario,
            "email": linha.email,
            "tipo_usuario": linha.tipo_usuario,
            "status": linha.status,
            "id_morador": linha.id_morador
        }
        return usuario

    except pyodbc.Error as erro:
        print("Erro ao buscar usuário:", erro)
        return None

    finally:
        cursor.close()
        conexao.close()

# CONSULTAS - MORADOR


def cadastrar_morador(email, senha, nome, cpf, telefone, bloco, apartamento):
    """
    Cadastra um novo morador: cria o USUARIO (login) e o MORADOR
    (dados pessoais), ligados pelo id_usuario.
    Retorna (True, "") em caso de sucesso, ou (False, "mensagem de erro").
    """
    conexao = conectar()
    if conexao is None:
        return False, "Não foi possível conectar ao banco."

    try:
        cursor = conexao.cursor()

        cursor.execute(
            "INSERT INTO USUARIO (email, senha, tipo_usuario, status) "
            "OUTPUT INSERTED.id_usuario "
            "VALUES (?, ?, 'MORADOR', 'ATIVO')",
            email, senha
        )
        id_usuario = cursor.fetchone().id_usuario

        
        cursor.execute(
            "INSERT INTO MORADOR (id_usuario, nome, cpf, telefone, bloco, apartamento) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            id_usuario, nome, cpf, telefone, bloco, apartamento
        )

        conexao.commit()
        return True, ""

    except pyodbc.IntegrityError:
        
        conexao.rollback()
        return False, "Já existe um morador cadastrado com esse e-mail ou CPF."

    except pyodbc.Error as erro:
        conexao.rollback()
        print("Erro ao cadastrar morador:", erro)
        return False, "Erro ao cadastrar morador."

    finally:
        cursor.close()
        conexao.close()


def consultar_moradores():
    """
    Retorna a lista de todos os moradores cadastrados, já com o
    status do login (ATIVO/INATIVO) trazido da tabela USUARIO.
    """
    conexao = conectar()
    if conexao is None:
        return []

    try:
        cursor = conexao.cursor()
        cursor.execute(
            "SELECT M.id_morador, M.nome, M.cpf, M.telefone, M.bloco, "
            "M.apartamento, U.email, U.status "
            "FROM MORADOR M "
            "JOIN USUARIO U ON U.id_usuario = M.id_usuario "
            "ORDER BY M.nome"
        )

        moradores = []
        for linha in cursor.fetchall():
            moradores.append({
                "id_morador": linha.id_morador,
                "nome": linha.nome,
                "cpf": linha.cpf,
                "telefone": linha.telefone,
                "bloco": linha.bloco,
                "apartamento": linha.apartamento,
                "email": linha.email,
                "status": linha.status
            })
        return moradores

    except pyodbc.Error as erro:
        print("Erro ao consultar moradores:", erro)
        return []

    finally:
        cursor.close()
        conexao.close()


def alterar_morador(id_morador, nome, cpf, telefone, bloco, apartamento):
    """
    Atualiza os dados pessoais de um morador já cadastrado.
    Retorna (True, "") em caso de sucesso, ou (False, "mensagem de erro").
    """
    conexao = conectar()
    if conexao is None:
        return False, "Não foi possível conectar ao banco."

    try:
        cursor = conexao.cursor()
        cursor.execute(
            "UPDATE MORADOR SET nome = ?, cpf = ?, telefone = ?, "
            "bloco = ?, apartamento = ? WHERE id_morador = ?",
            nome, cpf, telefone, bloco, apartamento, id_morador
        )
        conexao.commit()
        return True, ""

    except pyodbc.IntegrityError:
        conexao.rollback()
        return False, "Já existe outro morador com esse CPF."

    except pyodbc.Error as erro:
        conexao.rollback()
        print("Erro ao alterar morador:", erro)
        return False, "Erro ao alterar morador."

    finally:
        cursor.close()
        conexao.close()


# CONSULTAS - AREA_COMUM

def cadastrar_area(nome, descricao, capacidade):
    """
    Cadastra uma nova área comum, sempre começando com status ATIVA.
    """
    conexao = conectar()
    if conexao is None:
        return False, "Não foi possível conectar ao banco."

    try:
        cursor = conexao.cursor()
        cursor.execute(
            "INSERT INTO AREA_COMUM (nome, descricao, capacidade, status) "
            "VALUES (?, ?, ?, 'ATIVA')",
            nome, descricao, capacidade
        )
        conexao.commit()
        return True, ""

    except pyodbc.IntegrityError:
        conexao.rollback()
        return False, "Já existe uma área com esse nome."

    except pyodbc.Error as erro:
        conexao.rollback()
        print("Erro ao cadastrar área:", erro)
        return False, "Erro ao cadastrar área."

    finally:
        cursor.close()
        conexao.close()


def consultar_areas():
    """Retorna a lista de todas as áreas comuns cadastradas."""
    conexao = conectar()
    if conexao is None:
        return []

    try:
        cursor = conexao.cursor()
        cursor.execute(
            "SELECT id_area, nome, descricao, capacidade, status "
            "FROM AREA_COMUM ORDER BY nome"
        )

        areas = []
        for linha in cursor.fetchall():
            areas.append({
                "id_area": linha.id_area,
                "nome": linha.nome,
                "descricao": linha.descricao,
                "capacidade": linha.capacidade,
                "status": linha.status
            })
        return areas

    except pyodbc.Error as erro:
        print("Erro ao consultar áreas:", erro)
        return []

    finally:
        cursor.close()
        conexao.close()


def buscar_area_por_id(id_area):
    """Busca uma única área comum pelo id. Retorna None se não achar."""
    conexao = conectar()
    if conexao is None:
        return None

    try:
        cursor = conexao.cursor()
        cursor.execute(
            "SELECT id_area, nome, status FROM AREA_COMUM WHERE id_area = ?",
            id_area
        )
        linha = cursor.fetchone()

        if linha is None:
            return None

        return {"id_area": linha.id_area, "nome": linha.nome, "status": linha.status}

    except pyodbc.Error as erro:
        print("Erro ao buscar área:", erro)
        return None

    finally:
        cursor.close()
        conexao.close()


def alternar_status_area(id_area):
    """
    Alterna o status de uma área comum: ATIVA vira INATIVA e
    vice-versa (nunca apaga o registro, conforme regra do projeto).
    """
    area = buscar_area_por_id(id_area)
    if area is None:
        return False, "Área não encontrada."

    novo_status = "INATIVA" if area["status"] == "ATIVA" else "ATIVA"

    conexao = conectar()
    if conexao is None:
        return False, "Não foi possível conectar ao banco."

    try:
        cursor = conexao.cursor()
        cursor.execute(
            "UPDATE AREA_COMUM SET status = ? WHERE id_area = ?",
            novo_status, id_area
        )
        conexao.commit()
        return True, ""

    except pyodbc.Error as erro:
        conexao.rollback()
        print("Erro ao alterar status da área:", erro)
        return False, "Erro ao alterar status da área."

    finally:
        cursor.close()
        conexao.close()



# CONSULTAS - RESERVA


def existe_conflito_horario(id_area, data_reserva, hora_inicio, hora_fim):
    """
    Verifica se já existe uma reserva ATIVA para a mesma área e mesma
    data, com horário que se sobrepõe ao informado.
    Essa é a regra principal do sistema (RN05).
    """
    conexao = conectar()
    if conexao is None:
        return True  

    try:
        cursor = conexao.cursor()
        cursor.execute(
            "SELECT COUNT(*) AS total FROM RESERVA "
            "WHERE id_area = ? AND data_reserva = ? AND status = 'ATIVA' "
            "AND hora_inicio < ? AND hora_fim > ?",
            id_area, data_reserva, hora_fim, hora_inicio
        )
        resultado = cursor.fetchone()
        return resultado.total > 0

    except pyodbc.Error as erro:
        print("Erro ao verificar conflito de horário:", erro)
        return True

    finally:
        cursor.close()
        conexao.close()


def inserir_reserva(id_morador, id_area, data_reserva, hora_inicio, hora_fim):
    """Insere uma nova reserva com status ATIVA."""
    conexao = conectar()
    if conexao is None:
        return False

    try:
        cursor = conexao.cursor()
        cursor.execute(
            "INSERT INTO RESERVA (id_morador, id_area, data_reserva, "
            "hora_inicio, hora_fim, status) VALUES (?, ?, ?, ?, ?, 'ATIVA')",
            id_morador, id_area, data_reserva, hora_inicio, hora_fim
        )
        conexao.commit()
        return True

    except pyodbc.Error as erro:
        conexao.rollback()
        print("Erro ao inserir reserva:", erro)
        return False

    finally:
        cursor.close()
        conexao.close()


def consultar_reservas(id_morador=None):
   
    conexao = conectar()
    if conexao is None:
        return []

    try:
        cursor = conexao.cursor()

        sql = (
            "SELECT R.id_reserva, R.data_reserva, R.hora_inicio, R.hora_fim, "
            "R.status, M.nome AS nome_morador, A.nome AS nome_area, R.id_morador "
            "FROM RESERVA R "
            "JOIN MORADOR M ON M.id_morador = R.id_morador "
            "JOIN AREA_COMUM A ON A.id_area = R.id_area "
        )

        if id_morador is not None:
            sql += "WHERE R.id_morador = ? ORDER BY R.data_reserva DESC"
            cursor.execute(sql, id_morador)
        else:
            sql += "ORDER BY R.data_reserva DESC"
            cursor.execute(sql)

        reservas = []
        for linha in cursor.fetchall():
            reservas.append({
                "id_reserva": linha.id_reserva,
                "data_reserva": str(linha.data_reserva),
                "hora_inicio": str(linha.hora_inicio),
                "hora_fim": str(linha.hora_fim),
                "status": linha.status,
                "nome_morador": linha.nome_morador,
                "nome_area": linha.nome_area,
                "id_morador": linha.id_morador
            })
        return reservas

    except pyodbc.Error as erro:
        print("Erro ao consultar reservas:", erro)
        return []

    finally:
        cursor.close()
        conexao.close()


def cancelar_reserva(id_reserva, id_morador_solicitante, eh_administrador):
  
    conexao = conectar()
    if conexao is None:
        return False, "Não foi possível conectar ao banco."

    try:
        cursor = conexao.cursor()

        if eh_administrador:
            cursor.execute(
                "UPDATE RESERVA SET status = 'CANCELADA' WHERE id_reserva = ?",
                id_reserva
            )
        else:
          
            cursor.execute(
                "UPDATE RESERVA SET status = 'CANCELADA' "
                "WHERE id_reserva = ? AND id_morador = ?",
                id_reserva, id_morador_solicitante
            )

        linhas_afetadas = cursor.rowcount
        conexao.commit()

        if linhas_afetadas == 0:
            return False, "Reserva não encontrada ou você não tem permissão para cancelá-la."

        return True, ""

    except pyodbc.Error as erro:
        conexao.rollback()
        print("Erro ao cancelar reserva:", erro)
        return False, "Erro ao cancelar reserva."

    finally:
        cursor.close()
        conexao.close()



if __name__ == "__main__":
    testar_conexao()
