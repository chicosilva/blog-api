import datetime
import random
import re
import string

from django.template.defaultfilters import slugify


def get_client_ip(request):

    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def diff_dias(d1, d2):
    c = d1 - d2
    return c.days


def validar_cnpj(cnpj):
    """
    Valida CNPJs, retornando apenas a string de números válida.

    # CNPJs errados
    >>> validar_cnpj('abcdefghijklmn')
    False
    >>> validar_cnpj('123')
    False
    >>> validar_cnpj('')
    False
    >>> validar_cnpj(None)
    False
    >>> validar_cnpj('12345678901234')
    False
    >>> validar_cnpj('11222333000100')
    False

    # CNPJs corretos
    >>> validar_cnpj('11222333000181')
    '11222333000181'
    >>> validar_cnpj('11.222.333/0001-81')
    '11222333000181'
    >>> validar_cnpj('  11 222 333 0001 81  ')
    '11222333000181'
    """
    cnpj = "".join(re.findall("\d", str(cnpj)))

    if (not cnpj) or (len(cnpj) < 14):
        return False

    # Pega apenas os 12 primeiros dígitos do CNPJ e gera os 2 dígitos que faltam
    inteiros = map(int, cnpj)
    novo = inteiros[:12]

    prod = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    while len(novo) < 14:
        r = sum([x * y for (x, y) in zip(novo, prod)]) % 11
        if r > 1:
            f = 11 - r
        else:
            f = 0
        novo.append(f)
        prod.insert(0, 6)

    # Se o número gerado coincidir com o número original, é válido
    if novo == inteiros:
        return cnpj
    return False


def contact_data(form):

    dia = form.cleaned_data["data"]
    hora = form.cleaned_data["hora_inicio"]
    return datetime.datetime.combine(dia, hora)


def random_key(size=5):
    chars = string.ascii_uppercase + string.digits
    return "".join(random.choice(chars) for x in range(size))


def date_to_python(date):

    if not date:
        return None

    return datetime.datetime.strptime(date, "%d/%m/%Y").date()


# traduz 123.456.789-10 para 12345678910
_translate = lambda cpf: "".join(re.findall("\d", cpf))


def _exceptions(cpf):
    """Se o número de CPF estiver dentro das exceções é inválido"""
    if len(cpf) != 11:
        return True
    else:
        s = "".join(str(x) for x in cpf)
        if (
            s == "00000000000"
            or s == "11111111111"
            or s == "22222222222"
            or s == "33333333333"
            or s == "44444444444"
            or s == "55555555555"
            or s == "66666666666"
            or s == "77777777777"
            or s == "88888888888"
            or s == "99999999999"
        ):
            return True
    return False


def _gen(cpf):
    """Gera o próximo dígito do número de CPF"""
    res = []
    for i, a in enumerate(cpf):
        b = len(cpf) + 1 - i
        res.append(b * a)

    res = sum(res) % 11

    if res > 1:
        return 11 - res
    else:
        return 0


class CNPJ(object):
    def __init__(self, cnpj):
        """Classe representando um número de CNPJ"""

        from six import string_types

        if isinstance(cnpj, string_types):
            if not cnpj.isdigit():
                cnpj = cnpj.replace(".", "")
                cnpj = cnpj.replace("-", "")
                cnpj = cnpj.replace("/", "")

            if not cnpj.isdigit:
                return None

        if len(cnpj) < 14:
            return None

        self.cnpj = map(int, cnpj)

    def __getitem__(self, index):
        """Retorna o dígito em index como string

        # >>> a = CNPJ('11222333000181')
        # >>> a[9] == '0'
        True
        # >>> a[10] == '0'
        True
        # >>> a[9] == 0
        False
        # >>> a[10] == 0
        False

        """
        return str(self.cnpj[index])

    def __repr__(self):
        """Retorna uma representação 'real', ou seja:

        eval(repr(cnpj)) == cnpj

        # >>> a = CNPJ('11222333000181')
        # >>> print repr(a)
        CNPJ('11222333000181')
        # >>> eval(repr(a)) == a
        True

        """
        return "CNPJ('%s')" % "".join([str(x) for x in self.cnpj])

    def __eq__(self, other):
        """Provê teste de igualdade para números de CNPJ

        # >>> a = CNPJ('11222333000181')
        # >>> b = CNPJ('11.222.333/0001-81')
        >>> c = CNPJ([1, 1, 2, 2, 2, 3, 3, 3, 0, 0, 0, 1, 8, 2])
        # >>> a == b
        True
        # >>> a != c
        True
        # >>> b != c
        True

        """
        if isinstance(other, CNPJ):
            return self.cnpj == other.cnpj
        return False

    def __str__(self):
        """Retorna uma string do CNPJ na forma com pontos e traço

        # >>> a = CNPJ('11222333000181')
        # >>> str(a)
        '11.222.333/0001-81'

        """
        d = ((2, "."), (6, "."), (10, "/"), (15, "-"))
        s = map(str, self.cnpj)
        for i, v in d:
            s.insert(i, v)
        r = "".join(s)
        return r

    def isValid(self):
        """Valida o número de cnpj

        # >>> a = CNPJ('11.222.333/0001-81')
        # >>> a.valido()
        True
        # >>> b = CNPJ('11222333000182')
        # >>> b.valido()
        False

        """
        cnpj = self.cnpj[:12]
        prod = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        # pegamos apenas os 9 primeiros dígitos do CNPJ e geramos os
        # dois dígitos que faltam
        while len(cnpj) < 14:

            r = sum([x * y for (x, y) in zip(cnpj, prod)]) % 11

            if r > 1:
                f = 11 - r
            else:
                f = 0
            cnpj.append(f)
            prod.insert(0, 6)

        # se o número com os digítos faltantes coincidir com o número
        # original, então ele é válido
        return bool(cnpj == self.cnpj)


class CPF(object):
    _gen = staticmethod(_gen)
    _translate = staticmethod(_translate)

    def __init__(self, cpf):
        """O argumento cpf pode ser uma string nas formas:

        12345678910
        123.456.789-10

        ou uma lista ou tuple
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 0]
        (1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 0)

        """
        from six import string_types

        if isinstance(cpf, string_types):
            if not cpf.isdigit():
                cpf = self._translate(cpf)

        self.cpf = [int(x) for x in cpf]

    def __getitem__(self, index):
        """Retorna o dígito em index como string"""

        return self.cpf[index]

    def __repr__(self):
        """Retorna uma representação 'real', ou seja:

        eval(repr(cpf)) == cpf

        """

        return "CPF('%s')" % "".join(str(x) for x in self.cpf)

    def __eq__(self, other):
        """Provê teste de igualdade para números de CPF"""

        return isinstance(other, CPF) and self.cpf == other.cpf

    def __str__(self):
        """Retorna uma representação do CPF na forma:

        123.456.789-10

        """

        d = iter("..-")
        s = map(str, self.cpf)
        for i in range(3, 12, 4):
            s.insert(i, d.next())
        r = "".join(s)
        return r

    def isValid(self):
        """Valida o número de cpf"""

        if _exceptions(self.cpf):
            return False

        s = self.cpf[:9]
        s.append(self._gen(s))
        s.append(self._gen(s))
        return s == self.cpf[:]
