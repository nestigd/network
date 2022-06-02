// url to the posts API... TODO: find a way to make this dynamic -----------------------------------
const domain = window.parent.location.origin;


// Wait for document to load before adding any event listeners to the page
document.addEventListener('DOMContentLoaded', function (){

    // the page variable is porvided by the url. It can be 'all', 'followed' or an user
    let page = document.querySelector('#page').value;
    // use the page value as filtering variable to get the related posts
    getPost(`${page}`);
    
    
    if (document.querySelector('#follow-unfollow') != undefined){
        document.querySelector('#follow-unfollow').onclick = function () {
            console.log("clicked follow");
            changeFollowStatus(`${page}`);
            console.log("performed follow");
        }
    }

});



// this function makes a new DIV element and all its children containing the post information
function makePostDiv(post) {
    
    //create parent DIV for each new post
    const post_div = document.createElement('div');

    //create children
    const post_author = document.createElement('span');
    const post_author_link = document.createElement('a')
    const post_created = document.createElement('span');
    const post_text = document.createElement('div');

    //populate parent and children with data from the parsed post
    post_div.id = `post_${post.id}`;
    post_div.dataset.user_id = post.poster_id;
    post_div.className = "post_div";
    post_author_link.innerHTML = post.poster;
    post_author_link.href = `${domain}/user/${post.poster_id}`;
    post_created.innerHTML = post.timestamp;
    post_text.innerHTML = post.body;

    //this adds the new elements to the document
    post_author.append(post_author_link);
    post_div.append(post_author, post_created, post_text);
    document.querySelector('#post_container').append(post_div);
}

// this function sends an AJAX request to the server and receives a list of "post" objects back
// it supports a filter parameter that specifies which kind of post are requested: 'all', 'followed', '{user_id}'
function getPost(filter){

    fetch(`${domain}/posts/${filter}`)
    .then(response => response.json())
    .then(data => {
        data.forEach(post =>{
            console.log(post);
            makePostDiv(post);
        } );
    });
}


// TODO: ADD NEW DEDICATED UNFOLLOW BUTTON
// ADD DATASET TO FOLLOW AND UNFOLLOW BUTTONS
// PASS FOLLOW OR UNFOLLOW AS ARGUMENT TO THIS FUNCTION ANT THAT WILL GIVE THE API INFO ABOUT WHAT TO DO
// INITIALLY I WANTED TO USE THE SAME BUTTON TO FOLLOW/UNFOLLOW BUT IT WOULD BE EASY FOR A USER TO ACCIDENTALLY MESS UP
function changeFollowStatus (userToFollow){
    let button =  document.querySelector('#follow-unfollow');
      
    if (isNaN(userToFollow)){
        console.log("userToFollow variable is not a number.");
        alert("userToFollow variable is not a number.")
        return false
    }

    const payload = {
        "userToFollow" : userToFollow,
        "operation" : button.innerHTML
    }

    fetch(`${domain}/follow`,{
        method : 'post',
        body : JSON.stringify(payload),
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        alert(data["alert_msg"]);
        
        
        if (button.innerHTML === "Follow"){
            button.innerHTML = "Unfollow";
        }
        else {
            button.innerHTML = "Follow";
        }
        
    })

    
}
