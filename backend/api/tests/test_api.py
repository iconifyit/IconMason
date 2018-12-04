"""Test suite for the api views."""
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from iconmason.models import Icon


class APITestCase(TestCase):
    """Test suite for the api views."""

    fixtures = ['iconmason/tests/fixtures/icon.json']

    def setUp(self):
        """Define the test client and other test variables."""
        self.client = APIClient()
        self.icon = Icon.objects.get(pk="ae3c0261-f81e-41de-855b-82c1565959c6")

    def test_post_icon(self):
        """Test the api has Icon creation capability."""
        data = dict(
            name="Cool Icon",
            file="cool_icon.svg",  # TODO: make this a file upload
            tags=["awesome", "cool"],
            parent="9ef738b9-d5a3-4020-a863-e2dc633ca697"
        )
        response = self.client.post(
            reverse('create'),
            data,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_icon(self):
        """Test the api can get a given Icon."""
        response = self.client.get(
            reverse('crud', kwargs={'pk': self.icon.pk}),
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.icon)

    def test_update_icon(self):
        """Test the api can update a given Icon."""
        change_icon = {'name': 'New Cool Icon'}
        res = self.client.put(
            reverse('crud', kwargs={'pk': self.icon.pk}),
            change_icon,
            format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_delete_icon(self):
        """Test the api can delete an Icon."""
        response = self.client.delete(
            reverse('crud', kwargs={'pk': self.icon.pk}),
            format='json',
            follow=True
        )

        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
