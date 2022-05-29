// Wait for document to load before adding any event listeners to the page
document.addEventListener('DOMContentLoaded', function (){

    // When the "share" button of the new post is clicked, call a function to send the post to the backend
    document.querySelector('#newpost_share').onclick = () => {
         submitpost();
        }

});

// TODO: function to make a new child div displaying every post
function makePostDiv(post) {
    
    //create parent DIV for each new post
    const post_div = document.createElement('div');

    //create children
    const post_author = document.createElement('span');
    const post_created = document.createElement('span');
    const post_text = document.createElement('div');

    //populate new elements with data

    post_div.id = `post_${post.id}`;
    post_author.innerHTML = post.poster
}

// needs to support the following filters: 'all', 'followed', '{user_id}'
function getPost(filter){
    
    fetch(`posts/${filter}`)
    .then(response => response.json())
    .then(data => {
        data.forEach(post =>{
            makePostDiv(post);
        } );
    });
}
