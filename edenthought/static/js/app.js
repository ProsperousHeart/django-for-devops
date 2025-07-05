document.getElementById("note-form").onsubmit = function(event) {
    event.preventDefault(); // Prevent the default form submission

    alert("Your note was added!");
    this.submit();
}