from django import forms
from django.core.exceptions import ValidationError


# class SubscriptionForm(forms.ModelForm):
#     class Meta:
#         model = Subscription
#         fields = ['name', 'cpf', 'email', 'phone']

def validate_cpf(value):
    if not value.isdigit():
        raise ValidationError('O Cpf deve ter somente números', 'digits')

    if len(value) != 11:
        raise ValidationError('O Cpf deve ter 11 numeros', 'length')


class SubscriptionForm(forms.Form):
    name = forms.CharField(label='Nome')
    cpf = forms.CharField(label='CPF', validators=[validate_cpf])
    email = forms.EmailField(label='Email')
    phone = forms.CharField(label='Telefone')

    def clean_name(self):
        name = self.cleaned_data['name']
        words = [w.capitalize() for w in name.split()]
        return ' '.join(words)
