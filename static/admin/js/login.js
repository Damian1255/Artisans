$(document).ready(function () {
    $("#show_hide_password a").on('click', function (event) {
        event.preventDefault();
        if ($('#show_hide_password input').attr("type") == "text") {
            $('#show_hide_password input').attr('type', 'password');
            $('#show_hide_password i').addClass("bx-hide");
            $('#show_hide_password i').removeClass("bx-show");
        } else if ($('#show_hide_password input').attr("type") == "password") {
            $('#show_hide_password input').attr('type', 'text');
            $('#show_hide_password i').removeClass("bx-hide");
            $('#show_hide_password i').addClass("bx-show");
        }
    });
});

loginForm = document.getElementById('login');
loginForm.addEventListener("submit", function (event) {
    event.preventDefault();

    var username = loginForm.querySelector("input[name='username']");
    var password = loginForm.querySelector("input[name='password']");

    // Ajax call to login user 
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/admin/login', true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    xhr.onload = function () {
        if (xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
            if (response.success) {
                window.location.href = "/admin/";
            } else {
                show_error("Invalid username or password.")
                highlight_elements_red([username, password, document.getElementById("toggle-pwd")]);
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

function show_error(message) {
    var msgBox = document.getElementById("msg-box");
    msgBox.innerHTML = message;
}

function highlight_elements_red(element_arr) {
    element_arr.forEach(element => {
        element.style.borderColor = "red";
    });
}