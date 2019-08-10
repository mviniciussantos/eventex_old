from django.test import TestCase

from eventex.subscriptions.forms import SubscriptionForm


class SubscriptionFormTest(TestCase):
    def test_form_has_fields(self):
        """" Form must have 4 fields """
        expected = ['name', 'cpf', 'email', 'phone']
        form = SubscriptionForm()
        self.assertSequenceEqual(expected, list(form.fields))

    def test_cpf_is_digit(self):
        """ CPF must only accept digits"""
        form = self.make_validated_form(cpf='A2B4C678901')
        self.assertFormErrorCode(form, 'cpf', 'digits')

    def test_cpf_has_11_digits(self):
        """ CPF must have 11 digits"""
        form = self.make_validated_form(cpf='1234')
        self.assertFormErrorCode(form, 'cpf', 'length')

    def test_name_must_be_captalized(self):
        """ Name must be captalized."""
        form = self.make_validated_form(name='ViniCius SANTOS')
        self.assertEquals('Vinicius Santos', form.cleaned_data['name'])

    def test_email_is_optional(self):
        """Email is optional"""
        form = self.make_validated_form(email='')
        self.assertFalse(form.errors)

    def test_phone_is_optional(self):
        """Phone is optional"""
        form = self.make_validated_form(phone='')
        self.assertFalse(form.errors)

    def test_must_inform_email_or_phone(self):
        """Email and Phone are optionals, but one must be informed"""
        form = self.make_validated_form(email='', phone='')
        self.assertListEqual(['__all__'], list(form.errors))

    def assertFormErrorCode(self, form, field, code):
        errors = form.errors.as_data()
        error_list = errors[field]
        exception = error_list[0]

        self.assertEquals(code, exception.code)

    def assertFormErrorMessage(self, form, field, msg):
        errors = form.errors
        error_list = errors[field]

        self.assertListEqual([msg], error_list)

    def make_validated_form(self, **kwargs):
        valid = dict(name='Vinicius S', cpf='12345678901', email='vinicius@vs.com', phone='00 88888-8888')

        data = dict(valid, **kwargs)
        form = SubscriptionForm(data)
        form.is_valid()

        return form
