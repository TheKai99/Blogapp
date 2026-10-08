
console.log("JavaScript is working!");
console.log("hii");


const createBlogModal = document.getElementById("create-blog-modal");
const createBlogButton = document.getElementById("create-blog-btn");


createBlogButton.addEventListener("click" , function(){
    createBlogModal.style.display = "flex";
});



const closeBlogButton = document.getElementById("close-blog-modal");

closeBlogButton.addEventListener("click", function() {
    createBlogModal.style.display = "none";
});


const cancelBlogButton = document.getElementById("cancel-blog-btn");

cancelBlogButton.addEventListener("click" , function(){

    createBlogModal.style.display = "none";
})



createBlogModal.addEventListener("click", function(event) {

    if (event.target === createBlogModal) {
        createBlogModal.style.display = "none";
    }

});


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






