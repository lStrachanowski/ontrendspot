// Is toggling login form to register form 
let value = false;
let toggleValue = false;
let login = document.getElementById("loginForm");
let caption = document.getElementById("caption");
let register = document.getElementById("registerForm");
let prompt = document.getElementById("promptForm");
register.style.display = "none";
prompt.style.display = "none";

let formsToggle = () => {
    if (value == false) {
        // Login form
        login.style.animation = "fadeOut 0.7s";
        caption.style.animation = "fadeOut 0.7s";
        setTimeout(() => {
            login.style.display = "none";
        }, 650);

        setTimeout(() => {
            // Register form
            register.style.animation = "fadeIn 0.7s";
            caption.style.animation = "fadeIn 0.7s";
            register.style.display = "flex";
            caption.innerHTML = "Register";
        }, 650);

    } else {
        // Login form
        register.style.animation = "fadeOut 0.7s";
        caption.style.animation = "fadeOut 0.7s";
        setTimeout(() => {
            register.style.display = "none";
        }, 650);

        setTimeout(() => {
            // Register form
            login.style.animation = "fadeIn 0.7s";
            caption.style.animation = "fadeIn 0.7s";
            login.style.display = "flex";
            caption.innerHTML = "Login";
        }, 650);


    }
    value = !value;
}

let promptToggle = () => {
    if (toggleValue == false) {
        // Login form
        login.style.animation = "fadeOut 0.7s";
        caption.style.animation = "fadeOut 0.7s";
        setTimeout(() => {
            login.style.display = "none";
        }, 650);
        setTimeout(() => {
            // Prompt form
            prompt.style.animation = "fadeIn 0.7s";
            caption.style.animation = "fadeIn 0.7s";
            caption.innerHTML = "Reset password";
            prompt.style.display = "flex";
        }, 650);
    } else {
        // Login form
        caption.style.animation = "fadeOut 0.7s";
        prompt.style.animation = "fadeOut 0.7s";
        setTimeout(() => {
            prompt.style.display = "none";
        }, 650);

        setTimeout(() => {
            // Register form
            login.style.animation = "fadeIn 0.7s";
            caption.style.animation = "fadeIn 0.7s";
            login.style.display = "flex";
            caption.innerHTML = "Login";
        }, 650);

    };
    toggleValue = !toggleValue;
}