# Descrição do Projeto
Este projeto é uma aplicação web construída em Python, utilizando o framework Flask. Ele inclui funcionalidades de autenticação de usuário e interação com um banco de dados.

## Estrutura do Projeto
```
__pycache__/
.gitignore
.vscode/
    settings.json
app.py
database.py
instance/
models/
    __pycache__/
    user.py
```
## Funções

app.py:

`load_user(user_id):` Esta função é usada para carregar um usuário com base em seu ID. Ela é uma parte essencial do gerenciamento de sessão de usuário.

`login():` Esta função é responsável por autenticar o usuário. Ela recebe um nome de usuário e uma senha, verifica se eles estão corretos e, em caso afirmativo, inicia uma sessão para o usuário.

`logout():` Esta função é responsável por encerrar a sessão do usuário atualmente autenticado.

`create_user():` Esta função é responsável por criar um novo usuário. Ela recebe um nome de usuário e uma senha, cria um novo usuário com essas credenciais e o adiciona ao banco de dados.

`read_user(id_user):` Esta função é responsável por ler as informações de um usuário específico. Ela recebe o ID de um usuário e retorna suas informações.

`update_user(id_user):` Esta função é responsável por atualizar as informações de um usuário específico. Ela recebe o ID de um usuário e as novas informações, e atualiza o usuário no banco de dados.

`delete_user(id_user):` Esta função é responsável por deletar um usuário específico. Ela recebe o ID de um usuário e o remove do banco de dados.

## Como executar o projeto
Para executar este projeto, você precisa ter Python e Flask instalados em seu ambiente. Em seguida, você pode executar o arquivo app.py para iniciar o servidor Flask.
