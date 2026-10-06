
console.log("JavaScript is working!");


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