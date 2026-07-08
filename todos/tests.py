from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse


class AuthRouteTests(TestCase):
    def test_unauthenticated_home_renders_dashboard_with_signup_cta(self):
        response = self.client.get(reverse("todo_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sign up")

    def test_login_page_renders_for_unauthenticated_users(self):
        response = self.client.get(reverse("login"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Log in")

    def test_unauthenticated_task_submission_redirects_to_login_with_message(self):
        response = self.client.post(reverse("todo_list"), {"title": "New task"})

        self.assertRedirects(response, f"{reverse('login')}?next=/")
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Please log in to add a task." in str(message) for message in messages))
