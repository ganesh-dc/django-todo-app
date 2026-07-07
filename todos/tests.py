from django.test import TestCase
from django.urls import reverse


class AuthRouteTests(TestCase):
    def test_unauthenticated_home_redirects_to_login(self):
        response = self.client.get(reverse("todo_list"))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('login')}?next=/")

    def test_login_page_renders_for_unauthenticated_users(self):
        response = self.client.get(reverse("login"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Log in")
