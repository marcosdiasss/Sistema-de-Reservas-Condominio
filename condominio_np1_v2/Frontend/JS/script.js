// =====================================================
// script.js
// Interface do sistema (telas do Fernando) conectada de
// verdade ao back-end Python via fetch(). Nada de dados
// falsos: tudo que aparece na tela vem do SQL Server.
// =====================================================

// ---------- SESSÃO / CONTROLE DE ACESSO ----------

const tipoUsuarioLogado = localStorage.getItem("tipoUsuarioLogado");
const idUsuarioLogado = localStorage.getItem("idUsuarioLogado");
const idMoradorLogado = localStorage.getItem("idMoradorLogado");
const ehAdministrador = tipoUsuarioLogado === "ADMINISTRADOR";

const paginasAdministrativas = ["moradores.html", "cadastro_morador.html", "cadastro_area.html"];
const paginaAtual = window.location.pathname.split("/").pop();

// Se a página exige login e ninguém está logado, manda pro login
const paginasQueExigemLogin = [
    "opcoes.html", "moradores.html", "cadastro_morador.html",
    "areas.html", "cadastro_area.html", "reservas.html", "nova_reserva.html"
];

if (paginasQueExigemLogin.includes(paginaAtual) && !tipoUsuarioLogado) {
    window.location.href = "index.html";
}

if (tipoUsuarioLogado === "MORADOR") {
    if (paginasAdministrativas.includes(paginaAtual)) {
        window.location.href = "opcoes.html";
    } else {
        document.querySelectorAll('.sidebar a[href="moradores.html"], a[href="cadastro_area.html"]').forEach(function(link) {
            link.style.display = "none";
        });

        document.querySelectorAll(".usuario").forEach(function(elemento) {
            elemento.childNodes.forEach(function(no) {
                if (no.nodeType === Node.TEXT_NODE && no.nodeValue.includes("Administrador")) {
                    no.nodeValue = no.nodeValue.replace("Administrador", "Morador");
                }
            });
        });
    }
}

// ---------- LOGIN ----------

const loginForm = document.getElementById("form-login");

if (loginForm) {
    loginForm.addEventListener("submit", async function(event) {
        event.preventDefault();

        const email = document.getElementById("email").value.trim().toLowerCase();
        const senha = document.getElementById("senha").value;
        const mensagem = document.getElementById("erro-login");

        if (!email || !senha) {
            mensagem.textContent = "Preencha todos os campos.";
            return;
        }

        try {
            const resposta = await fetch("/login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email: email, senha: senha })
            });

            const dados = await resposta.json();

            if (!dados.sucesso) {
                mensagem.textContent = dados.mensagem;
                return;
            }

            localStorage.setItem("usuarioLogado", dados.usuario.email);
            localStorage.setItem("idUsuarioLogado", dados.usuario.id_usuario);
            localStorage.setItem("tipoUsuarioLogado", dados.usuario.tipo_usuario);
            localStorage.setItem("idMoradorLogado", dados.usuario.id_morador || "");

            window.location.href = "opcoes.html";

        } catch (erro) {
            mensagem.textContent = "Erro ao conectar com o servidor.";
            console.error(erro);
        }
    });
}

// ---------- MENU HAMBÚRGUER (mobile) ----------

document.querySelectorAll(".topbar").forEach(function(topbar) {
    const layout = topbar.nextElementSibling;
    const sidebar = layout ? layout.querySelector(".sidebar") : null;
    if (!sidebar) return;

    const idSidebar = "menuNavegacao";
    sidebar.id = idSidebar;

    const menu = document.createElement("button");
    menu.type = "button";
    menu.className = "menu-hamburguer";
    menu.setAttribute("aria-label", "Abrir menu de navegação");
    menu.setAttribute("aria-controls", idSidebar);
    menu.setAttribute("aria-expanded", "false");
    menu.innerHTML = "<span></span><span></span><span></span>";

    topbar.insertBefore(menu, topbar.firstElementChild);

    function fecharMenu() {
        sidebar.classList.remove("is-open");
        menu.classList.remove("is-open");
        menu.setAttribute("aria-expanded", "false");
        menu.setAttribute("aria-label", "Abrir menu de navegação");
    }

    menu.addEventListener("click", function(event) {
        event.stopPropagation();
        const aberto = sidebar.classList.toggle("is-open");
        menu.classList.toggle("is-open", aberto);
        menu.setAttribute("aria-expanded", String(aberto));
        menu.setAttribute("aria-label", aberto ? "Fechar menu de navegação" : "Abrir menu de navegação");
    });

    sidebar.addEventListener("click", function(event) {
        event.stopPropagation();
    });

    document.addEventListener("click", fecharMenu);
    document.addEventListener("keydown", function(event) {
        if (event.key === "Escape") fecharMenu();
    });
});

// ---------- LOGOUT ----------

function logout() {
    abrirModal("modalConfirmarSaida", "confirmarSaida");
}

function confirmarSaida() {
    localStorage.removeItem("usuarioLogado");
    localStorage.removeItem("idUsuarioLogado");
    localStorage.removeItem("tipoUsuarioLogado");
    localStorage.removeItem("idMoradorLogado");
    window.location.href = "index.html";
}

// ---------- MOSTRAR/OCULTAR SENHA ----------

const botaoAlternarSenha = document.querySelector('[data-action="toggle-senha"]');

if (botaoAlternarSenha) {
    botaoAlternarSenha.addEventListener("click", function() {
        const campoSenha = document.getElementById(botaoAlternarSenha.dataset.target);
        const icone = botaoAlternarSenha.querySelector("i");
        const senhaVisivel = campoSenha.type === "text";

        campoSenha.type = senhaVisivel ? "password" : "text";
        botaoAlternarSenha.setAttribute("aria-label", senhaVisivel ? "Mostrar senha" : "Ocultar senha");
        icone.className = senhaVisivel ? "bi bi-eye-slash" : "bi bi-eye";
    });
}

// ---------- FILTRO: ALGUNS CAMPOS ACEITAM SÓ NÚMEROS ----------
// Aplica em CPF (11 dígitos) e Apartamento (3 dígitos), tanto no
// cadastro quanto na edição.

function permitirSomenteNumeros(idCampo, tamanhoMaximo) {
    const campo = document.getElementById(idCampo);
    if (!campo) return;

    campo.addEventListener("input", function() {
        let valor = campo.value.replace(/\D/g, ""); // remove tudo que não é dígito
        if (tamanhoMaximo) {
            valor = valor.slice(0, tamanhoMaximo);
        }
        campo.value = valor;
    });
}

function permitirTelefone(idCampo) {
    const campo = document.getElementById(idCampo);
    if (!campo) return;

    campo.addEventListener("input", function() {
        // Permite números, espaço, parênteses e hífen; bloqueia letras/símbolos
        campo.value = campo.value.replace(/[^\d()\-\s]/g, "");
    });
}

function permitirSomenteLetras(idCampo) {
    const campo = document.getElementById(idCampo);
    if (!campo) return;

    campo.addEventListener("input", function() {
        // Permite letras (com acento) e espaço; bloqueia números e símbolos
        campo.value = campo.value.replace(/[^A-Za-zÀ-ÖØ-öø-ÿ\s]/g, "");
    });
}

permitirSomenteNumeros("cpfMorador", 11);
permitirSomenteNumeros("apartamentoMorador", 3);
permitirSomenteNumeros("editarCpfMorador", 11);
permitirSomenteNumeros("editarApartamentoMorador", 3);
permitirTelefone("telefoneMorador");
permitirTelefone("editarTelefoneMorador");
permitirSomenteLetras("nomeMorador");
permitirSomenteLetras("editarNomeMorador");

// =====================================================
// MORADORES
// =====================================================

// Guarda a última lista de moradores carregada (usada para abrir o modal de edição)
let moradoresCache = [];

async function carregarMoradores() {
    const tabela = document.getElementById("moradoresTabela");
    if (!tabela) return;

    const resposta = await fetch("/moradores/consultar", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({})
    });
    const dados = await resposta.json();
    moradoresCache = dados.moradores || [];

    tabela.innerHTML = "";

    moradoresCache.forEach(function(morador) {
        const linha = document.createElement("tr");
        linha.innerHTML = `
            <td>${morador.nome}</td>
            <td>${morador.cpf}</td>
            <td>${morador.telefone}</td>
            <td>${morador.bloco}</td>
            <td>${morador.apartamento}</td>
            <td>
                <button class="btn btn-edit" onclick="editarMorador(${morador.id_morador})">
                    Editar
                </button>
            </td>
        `;
        tabela.appendChild(linha);
    });
}

carregarMoradores();

function editarMorador(id_morador) {
    const morador = moradoresCache.find(function(item) {
        return item.id_morador === id_morador;
    });
    if (!morador) return;

    document.getElementById("editarMoradorId").value = morador.id_morador;
    document.getElementById("editarNomeMorador").value = morador.nome;
    document.getElementById("editarCpfMorador").value = morador.cpf;
    document.getElementById("editarTelefoneMorador").value = morador.telefone;
    document.getElementById("editarBlocoMorador").value = morador.bloco;
    document.getElementById("editarApartamentoMorador").value = morador.apartamento;

    abrirModal("modalEditarMorador", "editarNomeMorador");
}

const moradorForm = document.getElementById("moradorForm");

if (moradorForm) {
    moradorForm.addEventListener("submit", async function(event) {
        event.preventDefault();

        const corpo = {
            email: document.getElementById("emailMorador").value,
            senha: document.getElementById("senhaMorador").value,
            nome: document.getElementById("nomeMorador").value,
            cpf: document.getElementById("cpfMorador").value,
            telefone: document.getElementById("telefoneMorador").value,
            bloco: document.getElementById("blocoMorador").value,
            apartamento: document.getElementById("apartamentoMorador").value
        };

        const resposta = await fetch("/moradores/cadastrar", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(corpo)
        });
        const dados = await resposta.json();

        alert(dados.mensagem);

        if (dados.sucesso) {
            window.location.href = "moradores.html";
        }
    });
}

const formEditarMorador = document.getElementById("formEditarMorador");

if (formEditarMorador) {
    formEditarMorador.addEventListener("submit", async function(event) {
        event.preventDefault();

        const corpo = {
            id_morador: Number(document.getElementById("editarMoradorId").value),
            nome: document.getElementById("editarNomeMorador").value,
            cpf: document.getElementById("editarCpfMorador").value,
            telefone: document.getElementById("editarTelefoneMorador").value,
            bloco: document.getElementById("editarBlocoMorador").value,
            apartamento: document.getElementById("editarApartamentoMorador").value
        };

        const resposta = await fetch("/moradores/alterar", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(corpo)
        });
        const dados = await resposta.json();

        if (!dados.sucesso) {
            alert(dados.mensagem);
            return;
        }

        fecharModal(document.getElementById("modalEditarMorador"));
        carregarMoradores();
    });
}

// =====================================================
// ÁREAS COMUNS
// =====================================================

let areasCache = [];

async function carregarAreas() {
    const container = document.getElementById("areasContainer");
    if (!container) return;

    const resposta = await fetch("/areas/consultar", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({})
    });
    const dados = await resposta.json();
    areasCache = dados.areas || [];

    container.innerHTML = "";

    areasCache.forEach(function(area) {
        const card = document.createElement("div");
        card.classList.add("area-card");

        // O botão de ativar/desativar só aparece para o Administrador (RN11)
        const botaoStatus = ehAdministrador ? `
            <button type="button"
                class="area-status-btn ${area.status === "ATIVA" ? "area-status-btn--active" : ""}"
                aria-label="${area.status === "ATIVA" ? "Desativar" : "Ativar"} ${area.nome}"
                aria-pressed="${area.status === "ATIVA"}"
                onclick="alternarStatusArea(${area.id_area})">
                <span></span>
            </button>
        ` : "";

        card.innerHTML = `
            <h2>${area.nome}</h2>
            <p>${area.descricao || ""}</p>
            <div class="area-capacidade">Capacidade: ${area.capacidade} pessoas</div>
            <br>
            <span class="status status-${area.status === "ATIVA" ? "ativo" : "inativo"}">
                ${area.status}
            </span>
            ${botaoStatus}
        `;

        container.appendChild(card);
    });
}

carregarAreas();

async function alternarStatusArea(id_area) {
    const resposta = await fetch("/areas/alternar_status", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id_area: id_area })
    });
    const dados = await resposta.json();

    if (!dados.sucesso) {
        alert(dados.mensagem);
        return;
    }

    carregarAreas();
}

const areaForm = document.getElementById("areaForm");

if (areaForm) {
    areaForm.addEventListener("submit", async function(event) {
        event.preventDefault();

        const corpo = {
            nome: document.getElementById("nomeArea").value,
            descricao: document.getElementById("descricaoArea").value,
            capacidade: document.getElementById("capacidadeArea").value
        };

        const resposta = await fetch("/areas/cadastrar", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(corpo)
        });
        const dados = await resposta.json();

        alert(dados.mensagem);

        if (dados.sucesso) {
            window.location.href = "areas.html";
        }
    });
}

// =====================================================
// RESERVAS
// =====================================================

// Carrega os <select> da tela de Nova Reserva
async function carregarOpcoesReserva() {
    const seletorMorador = document.getElementById("moradorReserva");
    const seletorArea = document.getElementById("areaReserva");

    if (!seletorMorador && !seletorArea) return;

    if (seletorMorador) {
        const resposta = await fetch("/moradores/consultar", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({})
        });
        const dados = await resposta.json();
        const moradores = dados.moradores || [];

        if (!ehAdministrador) {
            // Um morador só pode reservar para si mesmo (RN02/RN09)
            const proprioMorador = moradores.find(function(m) {
                return m.id_morador === Number(idMoradorLogado);
            });
            if (proprioMorador) {
                seletorMorador.add(new Option(proprioMorador.nome, proprioMorador.id_morador));
                seletorMorador.value = proprioMorador.id_morador;
                seletorMorador.disabled = true;
            }
        } else {
            moradores.forEach(function(morador) {
                seletorMorador.add(new Option(morador.nome, morador.id_morador));
            });
        }
    }

    if (seletorArea) {
        const resposta = await fetch("/areas/consultar", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({})
        });
        const dados = await resposta.json();
        const areas = dados.areas || [];

        areas.filter(function(area) { return area.status === "ATIVA"; })
             .forEach(function(area) {
                 seletorArea.add(new Option(area.nome, area.id_area));
             });
    }
}

// Impede escolher uma data passada (ou um ano absurdo no futuro) no campo de reserva
const campoDataReserva = document.getElementById("dataReserva");

if (campoDataReserva) {
    const hoje = new Date();
    const formatarData = function(data) {
        return data.getFullYear() + "-" +
            String(data.getMonth() + 1).padStart(2, "0") + "-" +
            String(data.getDate()).padStart(2, "0");
    };

    const daquiUmAno = new Date(hoje);
    daquiUmAno.setFullYear(hoje.getFullYear() + 1);

    campoDataReserva.setAttribute("min", formatarData(hoje));
    campoDataReserva.setAttribute("max", formatarData(daquiUmAno));

    // Filtro: se o ano digitado/rolado passar de 4 dígitos (ou a data
    // ficar fora do intervalo permitido, tipo no passado), o campo limpa
    // sozinho assim que a data ficar "completa" (10 caracteres).
    campoDataReserva.addEventListener("input", function() {
        const valor = campoDataReserva.value;
        if (valor.length === 10 && !campoDataReserva.checkValidity()) {
            campoDataReserva.value = "";
        }
    });
}

carregarOpcoesReserva();

async function carregarReservas() {
    const tabela = document.getElementById("reservasTabela");
    if (!tabela) return;

    const corpo = {
        eh_administrador: ehAdministrador,
        id_morador: idMoradorLogado ? Number(idMoradorLogado) : null
    };

    const resposta = await fetch("/reservas/consultar", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(corpo)
    });
    const dados = await resposta.json();
    const reservas = dados.reservas || [];

    tabela.innerHTML = "";

    // A tabela resumida (dashboard) tem 5 colunas; a completa (reservas.html) tem 7
    const exibicaoResumida = tabela.closest("table").querySelectorAll("th").length === 5;
    const itensParaExibir = exibicaoResumida ? reservas.slice(0, 5) : reservas;

    itensParaExibir.forEach(function(reserva) {
        const linha = document.createElement("tr");
        const dataFormatada = reserva.data_reserva.split("-").reverse().join("/");
        const statusClasse = reserva.status === "ATIVA" ? "status-ativo" : "status-inativo";

        linha.innerHTML = exibicaoResumida ? `
            <td>${reserva.nome_morador}</td>
            <td>${reserva.nome_area}</td>
            <td>${dataFormatada}</td>
            <td>${reserva.hora_inicio} - ${reserva.hora_fim}</td>
            <td><span class="status ${statusClasse}">${reserva.status}</span></td>
        ` : `
            <td>${reserva.nome_morador}</td>
            <td>${reserva.nome_area}</td>
            <td>${dataFormatada}</td>
            <td>${reserva.hora_inicio}</td>
            <td>${reserva.hora_fim}</td>
            <td><span class="status ${statusClasse}">${reserva.status}</span></td>
            <td>
                ${reserva.status === "ATIVA" ? `
                    <button class="btn btn-cancel" onclick="cancelarReserva(${reserva.id_reserva})">
                        Cancelar
                    </button>
                ` : ""}
            </td>
        `;

        tabela.appendChild(linha);
    });
}

carregarReservas();

function cancelarReserva(id_reserva) {
    document.getElementById("mensagemCancelarReserva").textContent =
        "Deseja realmente cancelar esta reserva?";
    document.getElementById("confirmarCancelamentoReserva").dataset.reservaId = id_reserva;
    abrirModal("modalCancelarReserva", "confirmarCancelamentoReserva");
}

const confirmarCancelamentoReserva = document.getElementById("confirmarCancelamentoReserva");

if (confirmarCancelamentoReserva) {
    confirmarCancelamentoReserva.addEventListener("click", async function() {
        const id_reserva = Number(confirmarCancelamentoReserva.dataset.reservaId);

        const corpo = {
            id_reserva: id_reserva,
            id_morador: idMoradorLogado ? Number(idMoradorLogado) : null,
            eh_administrador: ehAdministrador
        };

        const resposta = await fetch("/reservas/cancelar", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(corpo)
        });
        const dados = await resposta.json();

        if (!dados.sucesso) {
            alert(dados.mensagem);
        }

        carregarReservas();
        atualizarResumo();
        fecharModal(document.getElementById("modalCancelarReserva"));
    });
}

const reservaForm = document.getElementById("reservaForm");

if (reservaForm) {
    reservaForm.addEventListener("submit", async function(event) {
        event.preventDefault();

        const inicio = document.getElementById("horaInicio").value;
        const fim = document.getElementById("horaFim").value;
        const dataDigitada = document.getElementById("dataReserva").value;

        // Confere se a data está mesmo no formato AAAA-MM-DD com ano de 4 dígitos
        // (evita anos absurdos que o campo de calendário às vezes deixa passar)
        if (!/^\d{4}-\d{2}-\d{2}$/.test(dataDigitada)) {
            alert("Data inválida. Selecione uma data pelo calendário.");
            return;
        }

        const corpo = {
            id_morador: Number(document.getElementById("moradorReserva").value),
            id_area: Number(document.getElementById("areaReserva").value),
            data_reserva: dataDigitada,
            hora_inicio: inicio,
            hora_fim: fim
        };

        const resposta = await fetch("/reservas/criar", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(corpo)
        });
        const dados = await resposta.json();

        alert(dados.mensagem);

        if (dados.sucesso) {
            window.location.href = "reservas.html";
        }
    });
}

// =====================================================
// RESUMO (Visão geral / opcoes.html)
// =====================================================

async function atualizarResumo() {
    const totalMoradoresEl = document.getElementById("totalMoradores");
    if (!totalMoradoresEl) return;

    const [respMoradores, respAreas, respReservas] = await Promise.all([
        fetch("/moradores/consultar", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }),
        fetch("/areas/consultar", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) }),
        fetch("/reservas/consultar", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ eh_administrador: ehAdministrador, id_morador: idMoradorLogado ? Number(idMoradorLogado) : null })
        })
    ]);

    const moradores = (await respMoradores.json()).moradores || [];
    const areas = (await respAreas.json()).areas || [];
    const reservas = (await respReservas.json()).reservas || [];

    totalMoradoresEl.textContent = moradores.length;
    document.getElementById("totalAreas").textContent = areas.length;
    document.getElementById("totalReservas").textContent =
        reservas.filter(function(r) { return r.status === "ATIVA"; }).length;
    document.getElementById("areasAtivas").textContent =
        areas.filter(function(a) { return a.status === "ATIVA"; }).length;
}

atualizarResumo();

// =====================================================
// MODAIS (genérico - já era do Fernando)
// =====================================================

let ultimoElementoFocado = null;

function abrirModal(idModal, idFoco) {
    const modal = document.getElementById(idModal);
    if (!modal) return;

    ultimoElementoFocado = document.activeElement;
    modal.classList.add("is-open");
    modal.setAttribute("aria-hidden", "false");
    document.body.classList.add("modal-aberto");

    const elementoFoco = document.getElementById(idFoco);
    if (elementoFoco) elementoFoco.focus();
}

function fecharModal(modal) {
    if (!modal) return;

    modal.classList.remove("is-open");
    modal.setAttribute("aria-hidden", "true");
    document.body.classList.remove("modal-aberto");

    if (ultimoElementoFocado) ultimoElementoFocado.focus();
}

document.body.insertAdjacentHTML("beforeend", `
    <div class="modal" id="modalConfirmarSaida" aria-hidden="true">
        <div class="modal-backdrop" data-fechar-modal></div>
        <section class="modal-dialog modal-dialog--small" role="dialog" aria-modal="true" aria-labelledby="tituloModalConfirmarSaida">
            <div class="modal-header">
                <h2 id="tituloModalConfirmarSaida">Sair do sistema</h2>
                <button type="button" class="modal-close" aria-label="Fechar" data-fechar-modal>&times;</button>
            </div>
            <p>Deseja realmente sair do sistema?</p>
            <div class="modal-actions">
                <button type="button" class="btn btn-secondary" data-fechar-modal>Cancelar</button>
                <button type="button" class="btn btn-cancel" id="confirmarSaida">Sair</button>
            </div>
        </section>
    </div>
`);

document.querySelectorAll("[data-fechar-modal]").forEach(function(botao) {
    botao.addEventListener("click", function() {
        fecharModal(botao.closest(".modal"));
    });
});

document.addEventListener("keydown", function(event) {
    if (event.key === "Escape") {
        fecharModal(document.querySelector(".modal.is-open"));
    }
});

const botaoConfirmarSaida = document.getElementById("confirmarSaida");

if (botaoConfirmarSaida) {
    botaoConfirmarSaida.addEventListener("click", confirmarSaida);
}
