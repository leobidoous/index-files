from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class CNPJValidator(object):
    def __call__(self, cnpj):
        """
        Method to validate brazilian cnpjs
        source: http://wiki.python.org.br/Cnpj
        Tests:

        print Cnpj().validate('61882613000194')
        True
        print Cnpj().validate('61882613000195')
        False
        print Cnpj().validate('53.612.734/0001-98')
        True
        print Cnpj().validate('69.435.154/0001-02')
        True
        print Cnpj().validate('69.435.154/0001-01')
        False
        """
        # defining some variables
        list_validation_one = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        list_validation_two = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]

        # cleaning the cnpj
        cnpj = cnpj.replace("-", "")
        cnpj = cnpj.replace(".", "")
        cnpj = cnpj.replace("/", "")

        # finding out the digits
        verifiers = cnpj[-2:]

        # verifying the length of the cnpj
        if len(cnpj) != 14:
            raise ValidationError(_('CNPJ invalido'))

        # calculating the first digit
        accumulated_value = 0
        id = 0
        for digit in cnpj:

            # to do not raise index errors
            try:
                list_validation_one[id]
            except:
                break

            accumulated_value += int(digit) * int(list_validation_one[id])
            id += 1

        accumulated_value %= 11

        if accumulated_value < 2:
            first_digit = 0
        else:
            first_digit = 11 - accumulated_value

        first_digit = str(first_digit)  # converting to string, for later comparison

        # calculating the second digit
        # summing the two lists
        accumulated_value = 0
        id = 0

        # summing the two lists
        for digit in cnpj:

            # to do not raise index errors
            try:
                list_validation_two[id]
            except:
                break

            accumulated_value += int(digit) * int(list_validation_two[id])
            id += 1

        # defining the digit
        accumulated_value %= 11

        if accumulated_value < 2:
            second_digit = 0
        else:
            second_digit = 11 - accumulated_value

        second_digit = str(second_digit)

        # returning
        if not bool(verifiers == first_digit + second_digit):
            raise ValidationError(_('CNPJ invalido'))


@deconstructible
class CPFValidator(object):
    def __call__(self, cpf):
        # cleaning the cpf
        cpf = cpf.replace("-", "")
        cpf = cpf.replace(".", "")
        if (not cpf) or (len(cpf) < 11):
            raise ValidationError(_('CPF inválido'))
        if cpf == len(cpf) * cpf[0]:
            raise ValidationError(_('CPF inválido'))
        # Get the 9 first digits and generate the last 2
        inteiros = list(map(int, cpf))
        novo = inteiros[:9]
        while len(novo) < 11:
            r = sum([(len(novo) + 1 - i) * v for i, v in enumerate(novo)]) % 11
            if r > 1:
                f = 11 - r
            else:
                f = 0
            novo.append(f)
        # If the generated number is not equal to original number, it is invalid
        if not bool(novo == inteiros):
            raise ValidationError(_('CPF inválido'))


