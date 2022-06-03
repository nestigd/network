// url to the posts API... TODO: find a way to make this dynamic -----------------------------------
const domain = window.parent.location.origin;
// by default set page to the first one

// Wait for document to load 
document.addEventListener('DOMContentLoaded', function (){

    // the filter variable is porvided by the url. It can be 'all/pagexx' or 'followed/pagexx' 
    let filter = document.querySelector('#filter').value;

    // The page is provided in the HTML by Django at first. It will be later updated by JS.
    let currentPage = document.querySelector('#current-page').value;

    // use the filter and current page to get the relevant posts
    getPost(filter, currentPage);
    
    // if follow-unfollow button has been loaded (you are in another user's profile page)... then add event listener
    if (document.querySelector('#follow-unfollow') != undefined){
        document.querySelector('#follow-unfollow').onclick = function () {
            console.log("clicked follow");
            changeFollowStatus(`${filter}`);
            console.log("performed follow");
        }
    }

    document.addEventListener

});



// this function makes a new DIV element and all its children containing the post information
function makePostDiv(post) {
    
    //remove any elements inside if there are any

    //create parent DIV for each new post
    const post_div = document.createElement('div');

    //create children
    const post_author = document.createElement('span');
    const post_author_link = document.createElement('a')
    const post_created = document.createElement('span');
    const post_text = document.createElement('div');
    const post_like = document.createElement('button')

    //populate parent and children with data from the parsed post
    post_div.id = `post_${post.id}`;
    post_div.dataset.user_id = post.poster_id;
    post_div.className = "post-div";
    post_author_link.innerHTML = post.poster;
    post_author_link.href = `${domain}/user/${post.poster_id}`;
    post_author_link.className = "post-span"
    post_created.innerHTML = post.timestamp;
    post_created.className = "post-span"
    post_text.innerHTML = post.body;
    post_text.className = "post-text"
    post_like.className = "btn btn-secondary";
    post_like.id = `like_button_${post.id}`;
    post_like.innerHTML = "0 Likes";

    //this adds the new elements to the document
    post_author.append(post_author_link);
    post_div.append(post_author, post_created, post_text, post_like);
    document.querySelector('#post_container').append(post_div);
}

// this function sends an AJAX request to the server and receives a list of "post" objects back
// it supports a filter parameter that specifies which kind of post are requested: 'all', 'followed', '{user_id}'
function getPost(filter, page){

    fetch(`${domain}/posts/${filter}&${page}`)
    .then(response => response.json())
    .then(data => {
    
        // empty the post container in case it is already populated
        document.querySelector('#post_container').innerHTML = "";

        // debugging helpers
        console.log(data["info"]);
        console.log(data["page"]);

        // populate container with new posts
        data['page'].forEach(post =>{
            makePostDiv(post);
        } );

        updatePaginator(filter, data["info"])
        // update paginator interface
        document.querySelector("#current-page-link").innerHTML = data["info"]["this_page"];

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
        
        if (button.innerHTML === "Follow"){
            button.innerHTML = "Unfollow";
        }
        else {
            button.innerHTML = "Follow";
        }
        
    })

    
}


function updatePaginator(filter, pageInfo){
    
    document.querySelector("#current-page-link").innerHTML = pageInfo.this_page;    
    
    // if filter is a number, prepend "user/" so that it becomes a valid url for a user page, otherwise it is already a valid url for 'index'.
    if (!isNaN(filter)){
        urlbuilder = `user/${filter}`;
    }else{
        urlbuilder = filter;
    }

    if (!pageInfo.has_previous) {
        document.querySelector("#previous-page").className = "page-item disabled";
    }else{
        document.querySelector("#previous-page").className = "page-item";
        document.querySelector("#previous-page-link").href = `${domain}/${urlbuilder}/page${(pageInfo.this_page) - 1}`;
    };

    if (!pageInfo.has_next) {
        document.querySelector("#next-page").className = "page-item disabled";
    }else{
        document.querySelector("#next-page").className = "page-item";
        document.querySelector("#next-page-link").href = `${domain}/${urlbuilder}/page${(pageInfo.this_page) + 1}`;
    }

}