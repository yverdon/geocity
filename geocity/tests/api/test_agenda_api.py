from django.test import TestCase
from rest_framework.test import APIClient


class AgendaAPITestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.client = APIClient()


# Test avec tous les status, s'affichent qu'avec les bons status
# Test élément dans light et pas élément pas dans light
# Test configuration, si le moindre élément manque, rien ne s'affiche
# Les filtres apparaissent que s'il y a un domaine
# Check order element (features, dates)
# Check filters work correctly (domaines, types, dates, etc..)
# Check if filters work correctly together, when we put multiple times
# Check if too much filters throw an error
