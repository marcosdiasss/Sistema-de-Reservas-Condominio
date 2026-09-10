import banco


def fazer_login(email, senha):
   
    # Validação de campos obrigatórios
    if not email or not senha:
        return {
            "sucesso": False,
            "mensagem": "Preencha e-mail e senha.",
            "usuario": None
        }

    usuario_encontrado = banco.buscar_usuario_login(email, senha)

    if usuario_encontrado is None:
        return {
            "sucesso": False,
            "mensagem": "E-mail ou senha inválidos.",
            "usuario": None
        }

    if usuario_encontrado["status"] != "ATIVO":
        return {
            "sucesso": False,
            "mensagem": "Usuário inativo. Procure o administrador.",
            "usuario": None
        }

    return {
        "sucesso": True,
        "mensagem": "Login realizado com sucesso.",
        "usuario": usuario_encontrado
    }
