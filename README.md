# 🎬 Catálogo de Filmes

Atividade Prática UC32 — Sistema CRUD com Flask e SQLite, publicado no Render.

## Funcionalidades
- Cadastrar filme (título, gênero, ano e nota de 1 a 10)
- Listar todos os filmes
- Editar um filme
- Excluir um filme

## Tecnologias
- Python 3
- Flask
- SQLite
- HTML + Jinja2
- Gunicorn (para o deploy)

## Como rodar localmente

```bash
# 1. (opcional) criar ambiente virtual
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Linux/Mac

# 2. instalar as dependências
pip install -r requirements.txt

# 3. rodar o app
python app.py
```

Depois é só abrir http://127.0.0.1:5000 no navegador.
O banco de dados (`filmes.db`) é criado sozinho na primeira vez que o app inicia.

## Deploy no Render
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn app:app`

> Obs: o SQLite no Render é temporário, então os dados somem quando o serviço reinicia.

## Link do projeto no Render
(colocar aqui o link depois do deploy)
