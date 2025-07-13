from django.test import TestCase
from django.urls import reverse

from .models import DailyNote


class DailyNoteTests(TestCase):

    # Test 1 - Check Home Page Loads
    def test_home_page_loads(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        # self.assertContains(response, "Daily Notes")
        # self.assertTemplateUsed(response, 'crm/home.html')
        self.assertTemplateUsed(response, "index.html")

    # Test 2 - Check Daily Note Creation via the Model
    def test_create_note_model(self):
        note = DailyNote.objects.create(title="Test Note")
        self.assertEqual(note.title, "Test Note")
        self.assertEqual(DailyNote.objects.count(), 1)

        # # Copilot Suggestion
        # response = self.client.post(reverse('create_daily_note'), {
        #     'title': 'Test Note',
        #     'content': 'This is a test note.'
        # })
        # self.assertEqual(response.status_code, 302)  # Should redirect after creation
        # self.assertTrue(DailyNote.objects.filter(title='Test Note').exists())

    # TEst 3 - creating a note from post form
    def test_create_note_from_post_form(self):
        # run a simulation for submitting the form
        response = self.client.post(
            reverse("home"),
            {
                "title": "Posted Note",
            },
        )
        # check new note was created as result of submission
        self.assertEqual(DailyNote.objects.count(), 1)
        # verify after submission that user is redirected to home page
        self.assertRedirects(response, reverse("home"))
