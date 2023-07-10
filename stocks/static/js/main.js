// Is toggling login form to register form 
let value = false;
let toggleValue = false;
let nameValue = false;
let emailValue = false;
let passwordValue = false;
let menuValue = false;
let login = document.getElementById("loginForm");
let caption = document.getElementById("caption");
let prompt = document.getElementById("promptForm");
let nameField = document.getElementById("name_field");
let nameFieldInput = document.getElementById("name_field_input");
let emailField = document.getElementById("email_field");
let emailFieldInput = document.getElementById("email_field_input");
let passwordPrompt = document.getElementById("changePasswordForm");
let siteMenu = document.getElementById("siteMenu");
let passwordField = document.getElementById("password_field");
let errorMessage = document.getElementsByClassName("error_message");
let numberOfVolumeElements = 5;

window.dispatchEvent(new Event('resize'));

if (siteMenu) {
    siteMenu.style.display = "none";
}
if (passwordPrompt) {
    passwordPrompt.style.display = "none";
}

if (emailFieldInput) {
    emailFieldInput.style.display = "none";
}

if (nameField) {
    nameFieldInput.style.display = "none";
}

if (prompt) {
    prompt.style.display = "none";
}

let showMenu = () => {
    if (menuValue == false) {
        siteMenu.style.display = "flex";
        siteMenu.style.width = "100vw";
        document.body.style.overflow = "hidden";
    } else {
        siteMenu.style.display = "none";
        siteMenu.style.width = "0";
        document.body.style.overflow = "visible";
    }
    menuValue = !menuValue;

}

let changePassword = () => {
    if (passwordValue == false) {
        passwordPrompt.style.display = "flex";
        passwordField.style.display = "none";
    }
    passwordValue = !passwordValue;
}

let passwordSave = () => {
    if (passwordValue == true) {
        passwordPrompt.style.display = "none";
        passwordField.style.display = "flex";
    }
    passwordValue = !passwordValue;
}

let passwordCancel = () => {
    if (passwordValue == true) {
        passwordPrompt.style.display = "none";
        passwordField.style.display = "flex";
        if (errorMessage.length > 0) {
            for (let i = 0; i < errorMessage.length; i++) {
                document.getElementsByClassName("error_message")[i].style.display = "none";
            }
        }
    }
    passwordValue = !passwordValue;
}

let editName = () => {
    if (nameValue == false) {
        nameField.style.display = "none";
        nameFieldInput.style.display = "flex";
    }
    nameValue = !nameValue;
}

let editNameCancel = () => {
    if (nameValue == true) {
        nameField.style.display = "flex";
        nameFieldInput.style.display = "none";
    }
    nameValue = !nameValue;
}

let editEmail = () => {
    if (emailValue == false) {
        emailField.style.display = "none";
        emailFieldInput.style.display = "flex";
    }
    emailValue = !emailValue;
}

let editEmailCancel = () => {
    if (emailValue == true) {
        emailField.style.display = "flex";
        emailFieldInput.style.display = "none";
    }
    emailValue = !emailValue;
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
    };
    toggleValue = !toggleValue;
}

function disableScroll() {
    // To get the scroll position of current webpage
    TopScroll = window.pageYOffset || document.documentElement.scrollTop;
    LeftScroll = window.pageXOffset || document.documentElement.scrollLeft,

        // if scroll happens, set it to the previous value
        window.onscroll = function () {
            window.scrollTo(LeftScroll, TopScroll);
        };
}

function enableScroll() {
    window.onscroll = function () { };
}

var xhttp = new XMLHttpRequest();
xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
        const loader_count = document.getElementsByClassName("loader").length;
        for (i = 0; i < loader_count; i++) {
            document.getElementsByClassName("loader")[i].style.display = 'none';
            document.getElementsByClassName('content')[i].style.visibility = "visible";
            let more_button = document.getElementsByClassName('index-button');
            if (more_button.length > 0) {
                document.getElementsByClassName('index-button')[i].style.visibility = "visible";
            }
        }
    }
    if (document.getElementById("user_name") !== null) {
        updateUser();
    }

    if (errorMessage.length > 0) {
        passwordPrompt.style.display = "flex";
        passwordField.style.display = "none";
    }
};
xhttp.open("GET", "/", true);
xhttp.send();

function elementTemplate(templateData) {
    template = `<div class="formation-content formation-content-list">
                    <button class="button-lista" onclick='location.href="/${templateData}/volume";'>
                        ${templateData}
                    </button>
                </div>`
    return template
};


function valueUpdate(value) {
    let resultList = document.getElementById(value);
    let html = ''
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            let elementLength = resultList.querySelectorAll(".button-lista").length;
            numberOfVolumeElements = elementLength;
            let templateDates = JSON.parse(this.responseText)['values'].slice(numberOfVolumeElements, numberOfVolumeElements + 6);
            templateDates.forEach(element => {
                html += elementTemplate(element);
            });
            resultList.insertAdjacentHTML("beforeend", html);
        }
    };
    xhttp.open("GET", `/morevalues/${value}`, true);
    xhttp.send();
}

function updateUser() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            let user_name = JSON.parse(this.responseText)['user'];
            let user_email = JSON.parse(this.responseText)['email'];
            const current_user_name = document.getElementById("user_name")
            const current_email = document.getElementById("user_email")
            current_user_name.innerHTML = "Name : " + user_name;
            current_email.innerHTML = "Email : " + user_email;
        }
    }
    xhttp.open("GET", "/update", true);
    xhttp.send();
}



// Copy link to clipboard
let shareLink = (ticker) => {
    site_url = window.location.href;
    base_url = window.location.origin;

    if (site_url.split('/').includes("volume")) {
        navigator.clipboard.writeText(base_url + "/stocks/" + ticker)
            .then(() => { alert(base_url + "/stocks/" + ticker + "\n Link skopiowany do showka."); })
            .catch((error) => { alert(`Copy failed! ${error}`); });
    }

    if (site_url.split('/').includes("mean")) {
        site_url = site_url.split("#")[0];
        navigator.clipboard.writeText(site_url + "#" + ticker)
            .then(() => { alert(site_url  + "#" + ticker + "\n Link skopiowany do showka."); })
            .catch((error) => { alert(`Copy failed! ${error}`); });
        
    }
    
}