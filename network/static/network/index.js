
function handlePostEdit(id){
    // identify the post with postid
    // get the post content and prefill a form with a text area
    // make a put request to change the post content to the endpoint and get a json response that changes the result

    // console.log("hi")
    // console.log(id)
    let edit = document.querySelector(`#textarea_${id}`).value
    // console.log(edit)
    let content = document.querySelector(`#post_content_${id}`)
    let modal = document.querySelector(`#editButton_${id}`)
    fetch(`/editpost/${id}`,{
        method:"PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            content: edit
        })
    })
    .then(response => response.json())
    .then(result=>{
        console.log(result);
        content.innerHTML = result.content;
        
        // remove modal and overlay/backdrop
        modal.classList.remove = ('show');
        modal.setAttribute('aria-hidden', 'true');
        modal.setAttribute('style', 'display: none')
        modal.remove();
        let backdrop = document.querySelector('.modal-backdrop');
        backdrop.remove()

    })
   
}






