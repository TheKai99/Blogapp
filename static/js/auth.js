
const registerForm = document.querySelector("#register-form");

if (registerForm) {
    registerForm.addEventListener("submit", async function (event) {
        event.preventDefault();

        const username = document.querySelector("#username").value.trim();
        const email = document.querySelector("#email").value.trim();
        const password = document.querySelector("#password").value;
        const confirmPassword = document.querySelector("#confirm-password").value;

        const errorBox = document.querySelector("#register-error");
        const submitButton = document.querySelector("#register-submit");

        errorBox.classList.add("d-none");
        errorBox.textContent = "";

        if (password !== confirmPassword) {
            errorBox.textContent = "Passwords do not match.";
            errorBox.classList.remove("d-none");
            return;
        }

        submitButton.disabled = true;

        try {
            const response = await fetch("/user/register", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    username: username,
                    email: email,
                    password: password
                })
            });

            if (response.ok) {
                window.location.href = "/user/login";
            } else {
                const errorData = await response.json();

                errorBox.textContent =
                    typeof errorData.detail === "string"
                        ? errorData.detail
                        : "Registration failed. Please check your details.";

                errorBox.classList.remove("d-none");
            }
        } catch (error) {
            console.error("Registration error:", error);

            errorBox.textContent =
                "Unable to connect to the server. Please try again.";

            errorBox.classList.remove("d-none");
        } finally {
            submitButton.disabled = false;
        }
    });
}





const loginForm = document.querySelector("#login-form");

if (loginForm) {
    loginForm.addEventListener("submit", async function (event) {
        event.preventDefault();

        const username = document.querySelector("#login-username").value.trim();
        const password = document.querySelector("#login-password").value;

        const errorBox = document.querySelector("#login-error");
        const submitButton = document.querySelector("#login-submit");

        errorBox.classList.add("d-none");
        errorBox.textContent = "";
        submitButton.disabled = true;

        try {
            const formData = new FormData();
            formData.append("username", username);
            formData.append("password", password);

            const response = await fetch("/user/login", {
                method: "POST",
                body: formData
            });

            const data = await response.json();

            if (response.ok) {
                // storing the jwt in the local storage
                localStorage.setItem("access_token", data.access_token);

                // get token from the cookie

                window.location.href = "/blog/home";

            } else {
                errorBox.textContent =
                    typeof data.detail === "string"
                        ? data.detail
                        : "Login failed. Please check your credentials.";

                errorBox.classList.remove("d-none");
            }



        } catch (error) {
            console.error("Login error:", error);

            errorBox.textContent =
                "Unable to connect to the server. Please try again.";

            errorBox.classList.remove("d-none");
        } finally {
            submitButton.disabled = false;
        }
    });
}


const logOutBtn = document.getElementById("account-logout-btn");

logOutBtn.addEventListener("click" , function(){

    localStorage.removeItem("access_token");

    window.location.href = "/blog/home";


});