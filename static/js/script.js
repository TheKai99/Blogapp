
console.log("JavaScript is working!");
console.log("hii");

// blog create button and model section
const createBlogModal = document.getElementById("create-blog-modal");
const createBlogButton = document.getElementById("create-blog-btn");

createBlogButton.addEventListener("click" , function(){
    createBlogModal.style.display = "flex";
});


// close button
const closeBlogButton = document.getElementById("close-blog-modal");

closeBlogButton.addEventListener("click", function() {
    createBlogModal.style.display = "none";
});


//cancel blog
const cancelBlogButton = document.getElementById("cancel-blog-btn");

cancelBlogButton.addEventListener("click" , function(){

    createBlogModal.style.display = "none";
})


// to disappear the model when we click anywhere else except the model or form
createBlogModal.addEventListener("click", function(event) {

    if (event.target === createBlogModal) {
        createBlogModal.style.display = "none";
    }

});


// to get the data from the model form and then send it to the api endpoints the page refresh
const createBlogForm = document.querySelector(".create-blog-form");

createBlogForm.addEventListener("submit" , async function(event){

    event.preventDefault();

    const title = document.getElementById("blog-title").value;
    const content = document.getElementById("blog-content").value;

    
    console.log("Sending" , title , content);

    const response = await fetch("/blog/create" ,{
        method:"POST",
        headers: {
            "content-type":"application/json"
        },
        body: JSON.stringify({
            title: title,
            content: content
        })
    });

    if (response.ok) {
        window.location.reload();   // or window.location.href = "/" to go to the blogs page
    } else {
        console.error("Failed:", response.status, await response.text());
         }

});



//---------------------------------------------------------------------------------------//
//// Edit blog model-- update edit  , fetch data to api endpoints
//---------------------------------------------------------------------------------------//


const updateBlogModal = document.getElementById("update-blog-modal");
const updateBlogbutton = document.getElementById("update-blog-btn");

updateBlogbutton.addEventListener("click" , function(){

    updateBlogModal.style.display = "flex";
});


// close button edit
const closeEditButton = document.getElementById("close-edit-btn");

closeEditButton.addEventListener("click", function() {
    updateBlogModal.style.display = "none";
});


//cancel blog edit
const cancelEditButton = document.getElementById("cancel-edit-btn");

cancelEditButton.addEventListener("click" , function(){

    updateBlogModal.style.display = "none";
})


updateBlogModal.addEventListener("click", function(event) {

    if (event.target === updateBlogModal) {
        updateBlogModal.style.display = "none";
    }

});


// For the update or edit blog model and actions

const updateBlogForm = document.querySelector(".update-blog-form");

updateBlogForm.addEventListener("submit" , async function(event){

    event.preventDefault();

    const title = document.getElementById("update-blog-title").value;
    const content = document.getElementById("update-blog-content").value;

    const blogId = updateBlogForm.dataset.blogId;

    console.log("Getting" , title , content , blogId);


    const response = await fetch(`/blog/${blogId}` ,{
        method:"PATCH",
        headers: {
            "content-type":"application/json"
        },
        body: JSON.stringify({
            title: title,
            content: content
        })
    });

    if (response.ok) {
        window.location.reload();   // or window.location.href = "/" to go to the blogs page
    } else {
        console.error("Failed:", response.status, await response.text());
         }


});



//---------------------------------------------------------------------------------------//
//// delete blog model-- del del del
//---------------------------------------------------------------------------------------//


const delBlogbutton = document.getElementById("delete-blog-btn");
const delBlogModal = document.getElementById("delete-blog-modal");

delBlogbutton.addEventListener("click" , function(){

    delBlogModal.style.display = "flex";

});

const canceldelModal = document.getElementById("cancel-delete-btn");

canceldelModal.addEventListener("click" , function(){

    delBlogModal.style.display = "none";

});

delBlogModal.addEventListener("click" , function(event){

    if(event.target === delBlogModal){
        delBlogModal.style.display = "none";
    }

});

const delBlogForm = document.querySelector(".delete-blog-form");

delBlogForm.addEventListener("submit" , async function(event){

    event.preventDefault();

    const blogId = delBlogForm.dataset.blogId;

    

    const response = await fetch(`/blog/${blogId}` ,{
        method:"DELETE",
        headers: {
            "content-type":"application/json"
        }
    });

    if (response.ok) {
        window.location.href="/blog/home";   // or window.location.href = "/" to go to the blogs page
    } else {
        console.error("Failed:", response.status, await response.text());
         }

});







