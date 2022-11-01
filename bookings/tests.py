from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from services.views import ServiceDetailsView
# Create your tests here.


class bookingRequestTest(APITestCase):

    def test_booking_create(self):
        response = self.client.get(ServiceDetailsView)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
