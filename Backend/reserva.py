# =====================================================
# reserva.py
# Regras de negócio relacionadas às reservas: criação,
# consulta, cancelamento e verificação de conflito de horário
# =====================================================

from datetime import date, timedelta
import re
import banco


def criar_reserva(dados):
    """Valida e cria uma nova reserva."""
    id_morador = dados.get("id_morador")
    id_area = dados.get("id_area")
    data_reserva = dados.get("data_reserva")
    hora_inicio = dados.get("hora_inicio")
    hora_fim = dados.get("hora_fim")

    if not all([id_morador, id_area, data_reserva, hora_inicio, hora_fim]):
        return {"sucesso": False, "mensagem": "Preencha todos os campos da reserva."}

    # Garante que a data está no formato AAAA-MM-DD com ano de 4 dígitos.
    # Sem isso, um ano digitado errado (ex: 275760) quebra a consulta no
    # SQL Server mais adiante de um jeito confuso de entender.
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", data_reserva):
        return {"sucesso": False, "mensagem": "Data inválida. Selecione uma data pelo calendário."}

    # O <input type="time"> do navegador manda "HH:MM" (sem segundos).
    # Completa com ":00" para bater com o tipo TIME do SQL Server.
    if len(hora_inicio) == 5:
        hora_inicio += ":00"
    if len(hora_fim) == 5:
        hora_fim += ":00"

    # RN08 - horário final deve ser maior que o inicial
    if hora_fim <= hora_inicio:
        return {"sucesso": False, "mensagem": "O horário final deve ser maior que o inicial."}

    # Horário de funcionamento do condomínio: 08:00 às 22:00
    if hora_inicio < "08:00:00" or hora_fim > "22:00:00":
        return {"sucesso": False, "mensagem": "Reservas só podem ser feitas entre 08:00 e 22:00."}

    # RN07 - não permite reserva em data passada
    if data_reserva < date.today().isoformat():
        return {"sucesso": False, "mensagem": "Não é possível reservar em uma data passada."}

    # Não permite reserva com mais de 1 ano de antecedência (evita ano digitado errado)
    data_limite = (date.today() + timedelta(days=365)).isoformat()
    if data_reserva > data_limite:
        return {"sucesso": False, "mensagem": "Não é possível reservar com mais de 1 ano de antecedência."}

    # RN06 - não permite reservar área inativa
    area = banco.buscar_area_por_id(id_area)
    if area is None:
        return {"sucesso": False, "mensagem": "Área não encontrada."}
    if area["status"] != "ATIVA":
        return {"sucesso": False, "mensagem": "Esta área está inativa e não pode ser reservada."}

    # RN05 - não permite reservas com horário sobreposto
    if banco.existe_conflito_horario(id_area, data_reserva, hora_inicio, hora_fim):
        return {"sucesso": False, "mensagem": "Já existe uma reserva para esta área nesse horário."}

    sucesso = banco.inserir_reserva(id_morador, id_area, data_reserva, hora_inicio, hora_fim)
    if not sucesso:
        return {"sucesso": False, "mensagem": "Erro ao criar reserva."}

    return {"sucesso": True, "mensagem": "Reserva realizada com sucesso."}


def consultar_reservas(dados):
    """
    Retorna as reservas. Se eh_administrador=True, retorna todas
    (RN10). Caso contrário, retorna só as do id_morador informado
    (RN09 - morador só vê as próprias reservas).
    """
    eh_administrador = dados.get("eh_administrador", False)
    id_morador = dados.get("id_morador")

    if eh_administrador:
        reservas = banco.consultar_reservas(id_morador=None)
    else:
        if not id_morador:
            return {"sucesso": False, "mensagem": "Morador não identificado.", "reservas": []}
        reservas = banco.consultar_reservas(id_morador=id_morador)

    return {"sucesso": True, "reservas": reservas}


def cancelar_reserva(dados):
    """Cancela uma reserva (RN09: morador só cancela as próprias)."""
    id_reserva = dados.get("id_reserva")
    id_morador = dados.get("id_morador")
    eh_administrador = dados.get("eh_administrador", False)

    if not id_reserva:
        return {"sucesso": False, "mensagem": "Reserva não informada."}

    sucesso, mensagem_erro = banco.cancelar_reserva(id_reserva, id_morador, eh_administrador)

    if not sucesso:
        return {"sucesso": False, "mensagem": mensagem_erro}

    return {"sucesso": True, "mensagem": "Reserva cancelada com sucesso."}
