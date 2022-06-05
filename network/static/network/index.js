// a sessionUserName variable is declared inside layout.html Django template.

// domain variable that will be used for URL construction
const domain = window.parent.location.origin;

// Wait for document to load 
document.addEventListener('DOMContentLoaded', function (){

    // the filter variable is provided in the url. It can be 'all/page##', 'followed/page##' or '${userid}'/page##
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

    // listen for clicks on "edit" buttons or "cancel". 
    document.addEventListener('click', function(event){
        
        // the postId will be useful in every function that will be called after
        postId = event.target.parentElement.id;
        
        // below are all the possible buttons we may want to react to:\\
        target = event.target.classList
        
        // call a function to display the correct form div while passing the id of the post to edit (in necessary)
        if (target.contains('edit')){
            displayEditForm(true, postId);
        }
        
        if(target.contains('cancel-edit')){
            displayEditForm(false, null);
        };

       if (target.contains('like')){
            likePost(postId);
       }

    })
    
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
    //const post_likenum = document.createElement('span');


    //populate parent 
    post_div.id = `${post.id}`;
    post_div.dataset.user_id = post.poster_id;
    post_div.className = "post-div";

    //populate children with data from the parsed post
    post_author_link.innerHTML = post.poster;
    post_author_link.href = `${domain}/user/${post.poster_id}`;
    post_author_link.className = "post-span";
    post_created.innerHTML = post.timestamp;
    post_created.className = "post-span";
    post_text.innerHTML = post.body;
    post_text.className = `post-text`;
    post_text.id = `post-${post.id}-text`;

    //post_likenum.innerHTML = "0 likes (W.I.P.)";
    
    //this adds the new elements to the document
    post_author.append(post_author_link);
    post_div.append(post_author, post_created, post_text,);
    document.querySelector('#post_container').append(post_div);

    //users need to be authenticated to edit or like posts
    if (userIsAuthenticated){

        // "EDIT" and "LIKE" butttons are mutually exclusive. User cannot like his own post, or edit someone else's 
        if (post.poster == sessionUserName){
            
            // generate EDIT button
            const post_edit = document.createElement('button');
            post_div.append(post_edit);
            
            post_edit.className = "btn btn-secondary edit";
            post_edit.innerHTML = "Edit";
        
            post_div.append(post_edit);


        }else{
            // generate LIKE button
            const post_like = document.createElement('button');
            post_div.append(post_like);

            post_like.className = "btn btn-primary like";
            post_like.id = `like-${post.id}`;
            
            // "Like" or "Unlike" depending on the information store in the database.
            post_like.innerHTML = "Like";
            if (post.liked){
                post_like.innerHTML = "Unlike";
            }

        }
    }


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

function displayEditForm (bool, postId){
    
    if (bool === true){
        
        // hide new post form if it exists
        if(document.querySelector("#new-post-form-container")){
            document.querySelector("#new-post-form-container").style.display = 'none';
        }
        // display edit post form while preparing url parameters and displaying the old text
        document.querySelector("#edit-post-form-container").style.display = 'block';
        document.querySelector('#edit_post_form').action = `${domain}/edit/${postId}`;
        document.querySelector('#edit_post_text').value = document.querySelector(`#post-${postId}-text`).innerHTML;
    }else{
        
        // display new post form if it exists
        if(document.querySelector("#new-post-form-container")){
            document.querySelector("#new-post-form-container").style.display = 'block';
        }
        // hide the edit form. resetting its values is not necessary as they will be overwritten if the function gets called again.
        document.querySelector("#edit-post-form-container").style.display = 'none';
        
    }
    
    console.log(`post numer ${postId} will be edited`);
}

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

function likePost(postId){
    // get CSRF token from helper in HTML header    
    csrftoken = document.getElementsByName('csrfmiddlewaretoken')[0].value

    // select the correct like button
    let button = document.querySelector(`#like-${postId}`);

    // assemble data
    const payload = {
        "postId" : postId,
        "likeStatus" : button.innerHTML,
    }

    // send put request
    fetch(`${domain}/like`, {
        method : 'put',
        body : JSON.stringify(payload),
        headers: { "X-CSRFToken": csrftoken },
        credentials : 'same-origin',
    })
    .then(response => response.json())
    .then(data => {
        
        console.log(data["status"]);

        // change button content after receiving reply
        if (data["status"] === "liked"){
            button.innerHTML = "Unlike";
        
        }else if (data["status"] === "unliked"){
            button.innerHTML = "Like";
        }
    })

}