// Is toggling login form to register form 
let value = false;
document.getElementById("registerForm").style.display = "none";
let formsToggle = () =>{
    let login = document.getElementById("loginForm");
    let caption = document.getElementById("caption");
    let register = document.getElementById("registerForm");

    if (value == false){
        // Login form
        login.style.animation = "fadeOut 0.7s";
        caption.style.animation = "fadeOut 0.7s";
        setTimeout(()=>{
            // elements[0].style.display = "none";
            login.style.display = "none";
        },650);

        setTimeout(()=>{
        // Register form
        register.style.animation = "fadeIn 0.7s";
        caption.style.animation = "fadeIn 0.7s";
        register.style.display = "flex";
        caption.innerHTML  = "Register";
        },650);

    }else{
        // Login form
        register.style.animation = "fadeOut 0.7s";
        caption.style.animation = "fadeOut 0.7s";
        setTimeout(()=>{
            register.style.display = "none";
        },650);

        setTimeout(()=>{
            // Register form
            login.style.animation = "fadeIn 0.7s";
            caption.style.animation = "fadeIn 0.7s";
            login.style.display = "flex";
            caption.innerHTML  = "Login";
        },650);


    }
    value = !value;
}

