[Table of Contents](/README.md)

# Create Standard Test Cases for Our Project

Focus is on creating standard test cases for our project.

## Part 1

Go to your `CRM` app & scroll down until you see `tests.py` file.

`from django.test import TestCase` imports Django's base TestCase class, which gives us access to tools fo rtesting our app in isolation as well as a temporary DB we can use for simulated HTTP requests.

Have a few imports to complete:

1. **Reverse Function**:  helps us find the correct URL for named route (which we have in the `urls.py` file when a route has a name)

    `from django.urls import reverse`

2. Import the models to use

    `from .models import DailyNote`

3. create test class

    ```python
    class DailyNoteTests(TestCase):
        pass
    ```

4. In that test class, will need to create 3 methods that will correlate to 3 tests:

    - check that homepage loads

    ```python
    def test_home_page_loads(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
    ```

    - check creation of note via model

    ```python
    def test_create_note_model(self):
        note = DailyNote.objects.create(title='Test Note')
        self.assertEqual(note.title, 'Test Note')
        self.assertEqual(DailyNote.objects.count(), 1)
        
        # # Copilot Suggestion
        # response = self.client.post(reverse('create_daily_note'), {
        #     'title': 'Test Note',
        #     'content': 'This is a test note.'
        # })
        # self.assertEqual(response.status_code, 302)  # Should redirect after creation
        # self.assertTrue(DailyNote.objects.filter(title='Test Note').exists())
    ```

## Part 2

    - create note from POST on form

![from template](/IMGs/section-08/8-POST-form.png)

 ```python
   def test_create_note_from_post_form(self):
       # run a simulation for submitting the form
       response = self.client.post(reverse('home'), {
           'title': 'Posted Note',
       })
       # check new note was created as result of submission
       self.assertEqual(DailyNote.objects.count(), 1)
       # verify after submission that user is redirected to home page
       self.assertRedirects(response, reverse('home'))
   ```

# Running Tests On Our Cases

?