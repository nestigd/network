// Wait for document to load before adding any event listeners to the page
document.addEventListener('DOMContentLoaded', function (){

    // When the "share" button of the new post is clicked, call a function to send the post to the backend
    document.querySelector('#newpost_share').onclick = () => {
         alert('clicked');
        }

});

