// Is toggling login form to register form 
let value = false;
document.getElementById("registerForm").style.display = "none";
let formsToggle = () =>{
    if (value == false){
        // Login form
        document.getElementById("loginForm").style.animation = "fadeOut 0.7s";
        document.getElementById("caption").style.animation = "fadeOut 0.7s";
        setTimeout(()=>{
            document.getElementById("loginForm").style.display = "none";
        },650);

        setTimeout(()=>{
        // Register form
        document.getElementById("registerForm").style.animation = "fadeIn 0.7s";
        document.getElementById("caption").style.animation = "fadeIn 0.7s";
        document.getElementById("registerForm").style.display = "flex";
        document.getElementById("caption").innerHTML  = "Register";
        },650);

    }else{
        // Login form
        document.getElementById("registerForm").style.animation = "fadeOut 0.7s";
        document.getElementById("caption").style.animation = "fadeOut 0.7s";
        setTimeout(()=>{
            document.getElementById("registerForm").style.display = "none";
        },650);

        setTimeout(()=>{
            // Register form
            document.getElementById("loginForm").style.animation = "fadeIn 0.7s";
            document.getElementById("caption").style.animation = "fadeIn 0.7s";
            document.getElementById("loginForm").style.display = "flex";
            document.getElementById("caption").innerHTML  = "Login";
        },650);


    }
    value = !value;
}

