from django.test import TestCase
from django.urls import reverse

from .models import DailyNote


class DailyNoteTests(TestCase):

    # Test 1 - Home page loading
    def test_home_page_loads(self):

        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, "index.html")

    # Test 2 - Create Note via the model
    def test_create_note_model(self):

        note = DailyNote.objects.create(title="Test Note")

        self.assertEqual(note.title, "Test Note")

        self.assertEqual(DailyNote.objects.count(), 1)

    # Test 3 - Create a note via the POST form
    def test_create_note_via_post(self):

        response = self.client.post(reverse("home"), {"title": "Posted note"})

        self.assertEqual(DailyNote.objects.count(), 1)

        self.assertRedirects(response, reverse("home"))
