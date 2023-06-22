var registerForm = document.getElementById("register");

// validate register form
registerForm.addEventListener("submit", function (event) {
    event.preventDefault();

    var first_name = registerForm.querySelector("input[name='first-name']").value;
    var last_name = registerForm.querySelector("input[name='last-name']").value;
    var email = registerForm.querySelector("input[name='email']").value;
    var username = registerForm.querySelector("input[name='username']").value;
    var password = registerForm.querySelector("input[name='password']").value;
    var rePassword = registerForm.querySelector("input[name='re-password']").value;

    if (password != rePassword) {
        registerForm.querySelector("input[name='password']").style.borderColor = "red";
        registerForm.querySelector("input[name='re-password']").style.borderColor = "red";

        show_reg_error("Passwords do not match!")
        return;
    }

    // Ajax call to register user 
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/register', true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    xhr.onload = function () {
        if (xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);

            if (response.available && response.success) {
                alert('Registration successful!');
                window.location.href = "/login";
            } else {
                show_reg_error("Email or Username already exists!")
            }
        } else {
            alert('Error registering.');
        }
    };
    xhr.send(JSON.stringify({
        first_name: first_name,
        last_name: last_name,
        email: email,
        username: username,
        password: password
    }));
});

function show_reg_error(message) {
    var msgBox = document.getElementById("reg-msg-box");
    msgBox.innerHTML = message;
}