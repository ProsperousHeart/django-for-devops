document.getElementById('note-form').onsubmit = function(event){

    event.preventDefault();

    alert("Your note was added!");

    this.submit();

}