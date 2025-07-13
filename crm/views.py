from django.shortcuts import render, redirect
from .models import DailyNote
from .forms import DailyNoteForm


def home(request):
    """
    Render the home page of the CRM application.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Rendered home page template.
    """

    if request.method == "POST":
        form = DailyNoteForm(request.POST)
        if form.is_valid():
            form.save()
            # Optionally, redirect to a success page or render the same page with a success message
            return redirect("home")
    else:
        form = DailyNoteForm()

    notes = DailyNote.objects.all()
    return render(request, "index.html", {"myForm": form, "notes": notes})
