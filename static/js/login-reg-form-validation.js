var registerForm = document.getElementById("register");
var loginForm = document.getElementById("login");

// validate register form
registerForm.addEventListener("submit", function (event) {
    event.preventDefault();

    var first_name = registerForm.querySelector("input[name='first-name']");
    var last_name = registerForm.querySelector("input[name='last-name']");
    var email = registerForm.querySelector("input[name='email']");
    var username = registerForm.querySelector("input[name='username']");
    var password = registerForm.querySelector("input[name='password']");
    var rePassword = registerForm.querySelector("input[name='re-password']");
    var dob = registerForm.querySelector("input[name='dob']");
    var gender = registerForm.querySelector("select[name='gender']");

    // clear any highlighted elements
    remove_highlight([password, rePassword, gender])

    // validate gender
    if (gender.value == "") {
        highlight_elements_red([gender])
        show_reg_error('Please select your gender.')
        return
    }

    // validate password
    if (password.value != rePassword.value) {
        highlight_elements_red([password, rePassword])
        show_reg_error('Passwords do not match.')
        return
    }

    // Ajax call to register user 
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/account/register', true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    xhr.onload = function () {
        if (xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);

            if (response.success) {
                registerForm.reset()
                window.location.href = "/account/login";
            } else {
                show_reg_error("Email or Username already exists.")
            }
        } else {
            alert('An Internal error occurred.');
        }
    };
    xhr.send(JSON.stringify({
        first_name: first_name.value,
        last_name: last_name.value,
        email: email.value,
        username: username.value,
        password: password.value,
        dob: dob.value,
        gender: gender.value,
        isadmin: false
    }));
});

// validate login form
loginForm.addEventListener("submit", function (event) {
    event.preventDefault();

    var username = loginForm.querySelector("input[name='username']");
    var password = loginForm.querySelector("input[name='password']");

    // Ajax call to login user 
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/account/login', true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    xhr.onload = function () {
        if (xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);

            if (response.success) {
                window.location.href = "/";
            } else {
                show_login_error("Invalid username or password.")
                highlight_elements_red([username, password]);
            }
        } else {
            alert('An Internal error occurred.');
        }
    };
    xhr.send(JSON.stringify({
        username: username.value,
        password: password.value
    }));
});

function show_reg_error(message) {
    var msgBox = document.getElementById("reg-msg-box");
    msgBox.innerHTML = message;
}

function show_login_error(message) {
    var msgBox = document.getElementById("login-msg-box");
    msgBox.innerHTML = message;
}

function highlight_elements_red(element_arr) {
    element_arr.forEach(element => {
        element.style.borderColor = "red";
    });
}

function remove_highlight(element_arr) {
    element_arr.forEach(element => {
        element.style.borderColor = "";
    });
}