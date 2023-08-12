document.addEventListener('DOMContentLoaded', function(){
    // try{
        const followlink = document.querySelector('#followlink');
        const urllink = followlink.href;
    // }catch(err){console.log("User not signed in/User own profile")}
    
    
    // Handles if followlink is not display and listen for a click event on the follow/unfollow button
        followlink.addEventListener('click', function(event){
            event.preventDefault()
            if (followlink.textContent === 'Unfollow'){
                changeFollowingToFalse(urllink);
            }else{
                changeFollowingToTrue(urllink);
            }
        })
   
    
    //Immediately DOM has finished mounted, check if the current user is following
    isFollowing(urllink)
    
    //change the context of the button on whether the current user is following or not
    function isFollowing(urllink){

        fetch(`${urllink}`)
        .then(response => response.json())
        .then(result=>{
            console.log(result);

            if (result.userisafollower){
                document.querySelector('#followlink').textContent = 'Unfollow';
                document.querySelector('#followlink').style.color = 'red';
            }else{
                document.querySelector('#followlink').textContent = 'Follow';
                document.querySelector('#followlink').style.color = 'blue';
            }
        }) 
    }

    // Function for the user to edit his post in the profile page
    


})


//function to call the API to add the current user as a follower
function changeFollowingToTrue(urllink){
    fetch(`${urllink}`,{
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
        userisafollower: true
        })
    })
    .then(response=>{
        if (response.status == 201){
            document.querySelector('#followlink').textContent = 'Unfollow';
            document.querySelector('#followlink').style.color = 'red';
            let followerspan = document.querySelector('#followernum')
            let followers = followerspan.textContent;     
            followerspan.textContent = parseInt(followers) + 1;
        }
    })
    console.log("success, now you are following")
}


//function to call the API to remove the current user as a follower
function changeFollowingToFalse(urllink){
    fetch(`${urllink}`,{
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
        userisafollower: false
        })
    })
    .then(response=>{
            if (response.status == 201){
                document.querySelector('#followlink').textContent = 'Follow';
                document.querySelector('#followlink').style.color = 'blue';
                let followerspan = document.querySelector('#followernum')
                let followers = followerspan.textContent;     
                followerspan.textContent = parseInt(followers) - 1;
            }
        })
    console.log("success. Unfollowed successfully")
}



