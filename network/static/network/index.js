// Wait for document to load before adding any event listeners to the page
document.addEventListener('DOMContentLoaded', function (){

    // When the "share" button of the new post is clicked, call a function to send the post to the backend
    document.querySelector('#newpost_share').onclick = () => {
         submitpost();
        }

});

// TODO: function to make a new child div displaying every post
function makePostDiv(post) {
    const id = post.id;
    
}

// TODO: AJAX request to get posts from backend
// TODO: needs to support the following filters: 'all', 'followed', '{user_id}'
function getPost(filter){
    
    fetch(`posts/${filter}`)
    .then(response => response.json())
    .then(data => {
        data.forEach(makePostDiv, this);
    });

}