# rocketseat-flask-auth

API simples de autenticação com Flask e Banco de dados

## How to run

```sh
# install dependencies
pip3 install -r requirements.txt --upgrade

# enter flask shell
flask shell

# create tables
>>> db.create_all()
# create user
>>> user = User(username="lfarias", password="test")
>>> db.session.add(user)
# commit your commands
>>> db.session.commit()
>>> exit()
```
