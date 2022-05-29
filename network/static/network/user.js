// url to the posts API... TODO: find a way to make this dynamic -----------------------------------
const postsAPIurl = "http://127.0.0.1:8000/posts"
const followAPIurl = "http://127.0.0.1:8000/follow"



// WAIT FOR PAGE TO GET LOADED
document.addEventListener('DOMContentLoaded', function (){

    // the page variable is provided by the url. It can be 'all', 'followed' or an user
    let page = document.querySelector('#page').value;
    // use the page value as filtering variable to get the related posts
    getPost(`${page}`);

    document.querySelector('#follow').onclick = function () {
        console.log("click");
        changeFollowStatus(`${page}`);
    }
   
});


// this function makes a new DIV element and all its children containing the post information
function makePostDiv(post) {
    
    //create parent DIV for each new post
    const post_div = document.createElement('div');

    //create children
    const post_author = document.createElement('span');
    const post_created = document.createElement('span');
    const post_text = document.createElement('div');

    //populate new elements with data
    post_div.id = `post_${post.id}`;
    post_div.className = "post_div"
    post_author.innerHTML = post.poster;
    post_created.innerHTML = post.timestamp;
    post_text.innerHTML = post.body;

    //this adds the new elements to the document
    post_div.append(post_author, post_created, post_text);
    document.querySelector('#post_container').append(post_div);
}

// this function sends an AJAX request to the server and receives a list of "post" objects back
// it supports a filter parameter that specifies which kind of post are requested: 'all', 'followed', '{user_id}'
function getPost(filter){

    fetch(`${postsAPIurl}/${filter}`)
    .then(response => response.json())
    .then(data => {
        data.forEach(post =>{
            console.log(post)
            makePostDiv(post);
        } );
    });
}

function changeFollowStatus (userToFollow){

    if (isNaN(userToFollow)){
        console.log("userToFollow variable is not a number.");
        return false
    }

    fetch(`${followAPIurl}`,{
        method : 'post',
        body : {
            "userToFollow" : JSON.stringify(userToFollow),
        }
    })
    .then(response => response.text())
    .then(text => {
        console.log(text);
        alert(text);
    })

}

