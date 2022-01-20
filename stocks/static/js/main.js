// Is toggling login form to register form 
let value = false;
let toggleValue = false;
let nameValue = false;
let emailValue = false;
let passwordValue = false;
let login = document.getElementById("loginForm");
let caption = document.getElementById("caption");
let register = document.getElementById("registerForm");
let prompt = document.getElementById("promptForm");
let nameField = document.getElementById("name_field");
let nameFieldInput = document.getElementById("name_field_input");
let emailField = document.getElementById("email_field");
let emailFieldInput = document.getElementById("email_field_input");
let passwordPrompt = document.getElementById("promptBox");

if(passwordPrompt){
    passwordPrompt.style.display = "none";
}

if(emailFieldInput){
    emailFieldInput.style.display = "none";
}

if(nameField){
    nameFieldInput.style.display = "none";
}

if (register){
    register.style.display = "none";
}

if(prompt){
    prompt.style.display = "none";
}

let changePassword = () =>{
    if(passwordValue == false){
        passwordPrompt.style.display = "flex";
    }
    passwordValue = !passwordValue;

}

let passwordSave = () =>{
    if(passwordValue == true){
        passwordPrompt.style.display = "none";
    }
    passwordValue = !passwordValue;
}

let passwordCancel = () =>{
    if(passwordValue == true){
        passwordPrompt.style.display = "none";
    }
    passwordValue = !passwordValue;
}

let editName = () => {
    if(nameValue == false){
        nameField.style.display = "none";
        nameFieldInput.style.display = "flex";
    }
    nameValue = !nameValue;
}

let editNameCancel = () => {
    if(nameValue == true){
        nameField.style.display = "flex";
        nameFieldInput.style.display = "none";
    }
    nameValue = !nameValue;
}

let editEmail = () => {
    if(emailValue == false){
        emailField.style.display = "none";
        emailFieldInput.style.display = "flex";
    }
    emailValue = !emailValue;
}

let editEmailCancel = () => {
    if(emailValue == true){
        emailField.style.display = "flex";
        emailFieldInput.style.display = "none";
    }
    emailValue = !emailValue;
}


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