# Sistema de Gestão e Reserva de Áreas Comuns em Condomínio

Projeto acadêmico da disciplina de Banco de Dados - UNIP.

## Tecnologias
- Back-end: Python (sem framework), conexão direta com SQL Server via pyodbc
- Front-end: HTML5, CSS3, JavaScript puro (páginas separadas, sem SPA)
- Banco de dados: Microsoft SQL Server (LocalDB)

## Como rodar

1. Instale as dependências:
   ```
   pip install pyodbc
   ```

2. Confirme o nome do seu servidor SQL Server em `Backend/banco.py`
   (por padrão está configurado para LocalDB: `(localdb)\MSSQLLocalDB`)

3. Crie o banco executando o script de estrutura (tabelas USUARIO, MORADOR,
   AREA_COMUM, RESERVA) e depois `banco/dados_teste.sql` (dados de teste) no
   SQL Server Management Studio.

4. Teste a conexão:
   ```
   cd Backend
   python banco.py
   ```

5. Suba o servidor:
   ```
   python servidor.py
   ```

6. Acesse http://localhost:8000 no navegador (abre a tela de login).

## Estrutura do projeto
```
Backend/
├── banco.py      → conexão com o SQL Server + TODAS as consultas SQL
├── usuario.py     → regra de negócio do login
├── morador.py     → regra de negócio do CRUD de moradores
├── area.py        → regra de negócio do CRUD de áreas comuns
├── reserva.py      → regra de negócio das reservas + conflito de horário
├── rotas.py       → mapeia as URLs para as funções corretas
└── servidor.py    → servidor HTTP (módulo nativo http.server, sem framework)

Frontend/
├── HTML/   (index.html = login, opcoes.html = menu, moradores.html, areas.html,
│            cadastro_morador.html, cadastro_area.html, reservas.html, nova_reserva.html)
├── CSS/    (style.css)
├── JS/     (script.js)
└── IMG/    (logo_sunlake.png)
```

Todo o SQL fica concentrado em `banco.py` — nenhum outro arquivo executa
comando SQL diretamente, o que facilita explicar o projeto: "todo acesso ao
banco passa por um único lugar".

## Como o sistema sabe quem está logado
Não usamos sessão de servidor (nem framework pronto pra isso). No login, o
navegador guarda o usuário logado no `localStorage` (id, tipo de usuário e,
se for morador, o id_morador). Cada tela envia esses dados junto com a
requisição, e o back-end confere as permissões antes de responder
(ex.: um morador só consegue ver e cancelar as próprias reservas).

## Usuários de teste
- Administrador: admin@condominio.com / admin123
- Morador: joao.silva@email.com / 123456
- Morador: maria.souza@email.com / 123456
- Morador (inativo): carlos.pereira@email.com / 123456

## Regras de negócio implementadas
- RN01/RN03 — cada morador tem cadastro único (e-mail e CPF únicos)
- RN02/RN04 — um morador pode ter várias reservas; uma área pode ter várias reservas
- RN05 — impede reservas com horário sobreposto na mesma área/data
- RN06 — impede reserva em área INATIVA
- RN07 — impede reserva em data passada
- RN08 — hora final deve ser maior que a inicial
- RN09 — morador só vê/cancela as próprias reservas
- RN10 — administrador vê todas as reservas
- RN11/RN12 — administrador gerencia áreas e moradores
- Cancelamento de reserva e desativação de área nunca apagam o registro,
  apenas mudam o status (histórico preservado)

## Status do desenvolvimento
- [x] Conexão com o banco
- [x] Login com controle de sessão
- [x] CRUD de moradores (cadastrar, consultar, alterar)
- [x] CRUD de áreas comuns (cadastrar, consultar, ativar/desativar)
- [x] Sistema de reservas (criar, consultar, cancelar)
- [x] Verificação de conflito de horários
- [x] Cancelamento de reservas (mantendo histórico)
- [ ] Testes completos documentados (Etapa 18)
- [ ] Documentação final / prints das telas (Etapa 19)
