// Is toggling login form to register form 
let value = false;
document.getElementById("registerForm").style.display = "none";
let formsToggle = () =>{
    if (value == false){
        document.getElementById("loginForm").style.display = "none";
        document.getElementById("registerForm").style.display = "flex";
        document.getElementById("caption").innerHTML  = "Register";
    }else{
        document.getElementById("registerForm").style.display = "none";
        document.getElementById("loginForm").style.display = "flex";
        document.getElementById("caption").innerHTML  = "Login";
    }
    value = !value;
}

