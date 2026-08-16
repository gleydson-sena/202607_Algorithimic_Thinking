# model/cliente.py
class Cliente:
    def __init__(self, nome, email, tem_criancas=False):
        self._nome = nome
        self._email = email
        self._tem_criancas = tem_criancas

    @property
    def nome(self): return self._nome
    @property
    def email(self): return self._email
    @property
    def tem_criancas(self): return self._tem_criancas