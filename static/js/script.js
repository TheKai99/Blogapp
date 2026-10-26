
console.log("JavaScript is working!");
console.log("hii");


///----------------------------------------------------------------------------------//
////  Load current User for the detaisl to display on navbar and chenging the navboar //
//////////////////from the simple to loggin user nav //////////////////////////////////////

async function loadcurrentuser() {

    console.log("loading current user!:");

    const token = localStorage.getItem("access_token");

    console.log("Token exists:", !!token);

    if (!token) {
        return;
    }

    try {
        const response = await fetch("/user/me", {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        if (!response.ok) {
            if (response.status == 401) {
                localStorage.removeItem("access_token");

            }
            return;
        }

        const user = await response.json();

        console.log("Current user:", user.id);

        const postActions = document.getElementById("post-actions");

        console.log("Post actions element:", postActions);
        console.log("Blog author ID:", postActions?.dataset.authorId);

        if (postActions && user.id === Number(postActions.dataset.authorId)) {
            postActions.classList.remove("d-none");
            console.log("Edit/Delete buttons displayed");
        }

        const loggedInNav = document.getElementById('loggedInNav');
        const loggedOutNav = document.getElementById('loggedOutNav');

        loggedInNav.classList.remove('d-none');
        loggedInNav.classList.add('d-flex');
        loggedOutNav.classList.add('d-none');
        document.getElementById('usernameDisplay').textContent = user.email;


        return user;

    } catch (error) {
        console.error("Error loading current user:", error);
    }


};




// blog create button and model section
const createBlogModal = document.getElementById("create-blog-modal");
const createBlogButton = document.getElementById("create-blog-btn");

createBlogButton.addEventListener("click", function () {
    createBlogModal.style.display = "flex";
});


// close button
const closeBlogButton = document.getElementById("close-blog-modal");

closeBlogButton.addEventListener("click", function () {
    createBlogModal.style.display = "none";
});


//cancel blog
const cancelBlogButton = document.getElementById("cancel-blog-btn");

cancelBlogButton.addEventListener("click", function () {

    createBlogModal.style.display = "none";
})


// to disappear the model when we click anywhere else except the model or form
createBlogModal.addEventListener("click", function (event) {

    if (event.target === createBlogModal) {
        createBlogModal.style.display = "none";
    }

});


// to get the data from the model form and then send it to the api endpoints the page refresh along with the jwt
const createBlogForm = document.querySelector(".create-blog-form");


createBlogForm.addEventListener("submit", async function (event) {

    event.preventDefault();

    const title = document.getElementById("blog-title").value;
    const content = document.getElementById("blog-content").value;

    const token = localStorage.getItem("access_token");

    if (!token) {
        console.error("token not even exist!!");
        return;
    }

    console.log("Sending", title, content);

    const response = await fetch("/blog/create", {
        method: "POST",
        headers: {
            "content-type": "application/json",
            "Authorization": `Bearer ${token}`
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

if (updateBlogbutton) {
    updateBlogbutton.addEventListener("click", function () {

        updateBlogModal.style.display = "flex";
    });
}


// close button edit
const closeEditButton = document.getElementById("close-edit-btn");

if (closeEditButton) {
    closeEditButton.addEventListener("click", function () {
        updateBlogModal.style.display = "none";
    });

}

//cancel blog edit
const cancelEditButton = document.getElementById("cancel-edit-btn");

if (cancelEditButton) {
    cancelEditButton.addEventListener("click", function () {

        updateBlogModal.style.display = "none";
    })
}


if (updateBlogModal) {
    updateBlogModal.addEventListener("click", function (event) {

        if (event.target === updateBlogModal) {
            updateBlogModal.style.display = "none";
        }

    });
}


// For the update or edit blog model and actions

const updateBlogForm = document.querySelector(".update-blog-form");

if (updateBlogForm) {
    updateBlogForm.addEventListener("submit", async function (event) {

        event.preventDefault();

        const title = document.getElementById("update-blog-title").value;
        const content = document.getElementById("update-blog-content").value;

        const blogId = updateBlogForm.dataset.blogId;

        console.log("Getting", title, content, blogId);
        

        const token = localStorage.getItem("access_token");

        const response = await fetch(`/blog/${blogId}`, {
            method: "PATCH",
            headers: {
                "content-type": "application/json",
                "Authorization": `Bearer ${token}`
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
}



//---------------------------------------------------------------------------------------//
//// delete blog model-- del del del
//---------------------------------------------------------------------------------------//


const delBlogbutton = document.getElementById("delete-blog-btn");
const delBlogModal = document.getElementById("delete-blog-modal");

if (delBlogbutton) {
    delBlogbutton.addEventListener("click", function () {

        delBlogModal.style.display = "flex";

    });
}

const canceldelModal = document.getElementById("cancel-delete-btn");

if (canceldelModal) {
    canceldelModal.addEventListener("click", function () {

        delBlogModal.style.display = "none";

    });
}

if (delBlogModal) {
    delBlogModal.addEventListener("click", function (event) {

        if (event.target === delBlogModal) {
            delBlogModal.style.display = "none";
        }

    });
}

const delBlogForm = document.querySelector(".delete-blog-form");


if (delBlogForm) {
    delBlogForm.addEventListener("submit", async function (event) {

        event.preventDefault();

        const blogId = delBlogForm.dataset.blogId;

        const token = localStorage.getItem("access_token");


 
        const response = await fetch(`/blog/${blogId}`, {
            method: "DELETE",
            headers: {
                "content-type": "application/json",
                "Authorization": `Bearer ${token}`
            }
        });

        if (response.ok) {
            window.location.href = "/blog/home";   // or window.location.href = "/" to go to the blogs page
        } else {
            console.error("Failed:", response.status, await response.text());
        }

    });
}









// profile update section------------------------------------------//
//-----------------------------------------------------------------//












document.addEventListener("DOMContentLoaded", () => {
    loadcurrentuser();
});
