from django.test import TestCase

from eventex.subscriptions.models import Subscription


class SubscriptionDetailGet(TestCase):
    def setUp(self):
        self.obj = Subscription.objects.create(
            name='Vinicius Santos',
            cpf='12345678901',
            email='vinicius.santos@vs.com',
            phone='79-99999-9999'
        )
        self.resp = self.client.get('/inscricao/{}/'.format(self.obj.pk))

    def test_get(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_detail.html')

    def test_context(self):
        subscription = self.resp.context['subscription']

        self.assertIsInstance(subscription, Subscription)

    def test_html(self):
        contents = (self.obj.name, self.obj.cpf, self.obj.email, self.obj.phone)

        for content in contents:
            with self.subTest():
                self.assertContains(self.resp, content)


class SubscriptionDetailNotFound(TestCase):
    def test_not_found(self):
        resp = self.client.get('inscricao/0/')

        self.assertEqual(404, resp.status_code)
