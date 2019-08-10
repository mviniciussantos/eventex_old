from django.core.exceptions import ValidationError


def validate_cpf(value):
    if not value.isdigit():
        raise ValidationError('O Cpf deve ter somente números', 'digits')

    if len(value) != 11:
        raise ValidationError('O Cpf deve ter 11 numeros', 'length')
