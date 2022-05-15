const textInput = document.querySelector('body')

function addPost(e) {
    e.prevenDefault();
   textInput.value=""; 
}