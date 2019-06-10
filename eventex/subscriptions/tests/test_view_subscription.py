from django.core import mail
from django.test import TestCase

from eventex.subscriptions.forms import SubscriptionForm


class SubscribeTest(TestCase):
    def setUp(self):
        self.resp = self.client.get('/inscricao/')

    def test_get(self):
        """ Get /inscricao/ Must return status code 200 """
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """ Must use subscriptions/subscription_form.html"""
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_form.html')

    def test_html(self):
        """ Must have html elements"""
        self.assertContains(self.resp, '<form')
        self.assertContains(self.resp, '<input', 6)
        self.assertContains(self.resp, 'type="text"')
        self.assertContains(self.resp, 'type="email"')
        self.assertContains(self.resp, 'type="submit"')

    def test_csrf(self):
        """ Must have csrfmiddlewaretoken"""
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """ Context must have subscription form"""
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_fields(self):
        """ Form must have 4 fields"""
        form = self.resp.context['form']
        self.assertSequenceEqual(['name', 'cpf', 'email', 'phone'], list(form.fields))


class SubscribePostTest(TestCase):
    def setUp(self):
        data = dict(name='Vinicius Santos', cpf='12345678901', email='vinicius.santos@vs.com', phone='79-99999-9999')
        self.resp = self.client.post('/inscricao/', data)

    def test_post(self):
        """
        Valid Post should redirect to /inscricao/
        """
        self.assertEqual(302, self.resp.status_code)

    def test_send_email(self):
        self.assertEqual(1, len(mail.outbox))

    def test_email_subscription(self):
        email = mail.outbox[0]
        expect = 'Confirmação de inscrição'

        self.assertEqual(expect, email.subject)

    def test_email_from(self):
        email = mail.outbox[0]
        expect = 'contato@eventex.com'

        self.assertEqual(expect, email.from_email)

    def test_email_subscription_email_to(self):
        email = mail.outbox[0]
        expect = ['contato@eventex.com.br', 'vinicius.santos@vs.com']

        self.assertEqual(expect, email.to)

    def test_subscription_email_body(self):
        email = mail.outbox[0]

        self.assertIn('Vinicius Santos', email.body)
        self.assertIn('12345678901', email.body)
        self.assertIn('vinicius.santos@vs.com', email.body)
        self.assertIn('79-99999-9999', email.body)


class SubscribeInvalidPost(TestCase):
    def setUp(self):
        self.resp = self.client.post('/inscricao/', {})

    def test_post(self):
        """Invalid POST should NOT redirect"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_form.html')

    def test_has_form(self):
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_has_errors(self):
        form = self.resp.context['form']
        self.assertTrue(form, form.errors)


class SubscreibrSuccessMessage(TestCase):
    def test_message(self):
        data = dict(name='Vinicius Santos', cpf='12345678901', email='vinicius.santos@vs.com', phone='79-99999-9999')

        response = self.client.post('/inscricao/', data, follow=True)

        self.assertContains(response, 'Inscrição realizada com sucesso')
