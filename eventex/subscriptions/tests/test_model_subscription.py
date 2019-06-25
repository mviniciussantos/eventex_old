from datetime import datetime

from django.test import TestCase

from eventex.subscriptions.models import Subscription


class SubscriptionModelTest(TestCase):
    def setUp(self):
        self.obj = Subscription(
            name='Vinicius Santos',
            cpf='12345678901',
            email='vinicius.santos@vs.com',
            phone='79-99999-9999'
        )

        self.obj.save()

    def test_create(self):
        self.assertTrue(Subscription.objects.exists())

    def test_created_at(self):
        self.assertIsInstance(self.obj.created_at, datetime)

    def test_str(self):
        self.assertEqual('Vinicius Santos', str(self.obj))

    def test_paid_default_to_false(self):
        """Por default o pagamento deve ser False """
        self.assertEqual(False, self.obj.paid)
