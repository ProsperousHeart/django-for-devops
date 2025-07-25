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

NAvigate to your main project app folder and open `settings.py` - for this test, comment out PROD DB and use the SQLite in the interim.

In command prompt run:  `python manage.py test`

![test run outcome](/IMGs/section-08/8-test-outcome.png)

Switch the databases so your PROD DB is to be used moving forward.

# [Format & Cleanup Code With Black](https://www.udemy.com/course/python-django-for-devops-terraform-render-docker-cicd/learn/lecture/49770359#overview)

[Black](https://pypi.org/project/black/) - is a code formatter that automatically rewrites code to ensure it follows a consistent rule in terms of styling & helps make it cleaner.

Run in CMD prompt:  `pip install black`

To have it automatically update, run:  `black .`

![black reformatting output](/IMGs/section-08/8-black-reformatting-output.png)

# [Linting with Ruff](https://www.udemy.com/course/python-django-for-devops-terraform-render-docker-cicd/learn/lecture/49770429#overview)

Linting is the process of analyzing code for potential errors, style issues, or bad practices.

[Ruff](https://pypi.org/project/ruff/) - a python linter written in Rust. (Also a code formatter but more robust than Black in terms of linting capabilities.) Helps ID & fix issues to keep code clean.

Run in command prompt:  `pip install ruff`

Also creates a Ruff cache in your directory to improve speed.

Run in CMD:  `ruff check`

If there is an issue, it will tell you what and where. Otherwise, it will look something like this:

![ruff check outcome](/IMGs/section-08/8-ruff-check.png)

# [Source Code Cleanup & Package Updates](https://www.udemy.com/course/python-django-for-devops-terraform-render-docker-cicd/learn/lecture/49922143#overview)

Delete the `.ruff_cache` and `staticfiles` directories from main project folder.

Update `requirements.txt` file to include the new packages.

