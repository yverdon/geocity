import re
import urllib.parse
import uuid
from datetime import date

from django.conf import settings
from django.contrib.auth.models import Permission
from django.core import mail
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from permits import models, services

from . import factories
from .utils import LoggedInIntegrator

class AdminSiteTestCase(LoggedInIntegrator, TestCase):

    def test_integrator_can_only_see_own_requests(self):
        print(LoggedInIntegrator)
        print("hello")
        print("world")
        print("im")
        print("testing")
        print("new")
        print("things")
        self.assertEqual(True, False)