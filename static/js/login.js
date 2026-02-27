document.addEventListener("DOMContentLoaded", function() {

    const loginContainer = document.querySelector(".login-container");
    const registerContainer = document.querySelector(".register-container");

    const showRegisterBtn = document.getElementById("showRegister");
    const showLoginBtn = document.getElementById("showLogin");

    showRegisterBtn.addEventListener("click", function() {
        loginContainer.classList.add("hidden");
        registerContainer.classList.remove("hidden");
    });

    showLoginBtn.addEventListener("click", function() {
        registerContainer.classList.add("hidden");
        loginContainer.classList.remove("hidden");
    });

});