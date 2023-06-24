var updateForm = document.querySelector("#update-form");

// validate register form
updateForm.addEventListener("submit", function (event) {
    event.preventDefault();

    var id = updateForm.querySelector("input[name='id']").value;
    var first_name = updateForm.querySelector("input[name='first-name']");
    var last_name = updateForm.querySelector("input[name='last-name']");
    var email = updateForm.querySelector("input[name='email']");
    var password = updateForm.querySelector("input[name='password']");
    var dob = updateForm.querySelector("input[name='dob']");

    // clear any highlighted elements
    remove_highlight([password])

    // Ajax call to register user 
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/update-user/' + id, true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    xhr.onload = function () {
        if (xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);

            if (response.success) {
                show_msg("User updated successfully!", "green")
            } else {
                show_msg("User update failed.", "red")
            }
        } else {
            alert('An Internal error occurred.');
        }
    };
    xhr.send(JSON.stringify({
        first_name: first_name.value,
        last_name: last_name.value,
        email: email.value,
        password: password.value,
        dob: dob.value,
    }));
});

function show_msg(message, color) {
    var msgBox = document.getElementById("msg-box");
    msgBox.innerHTML = message;
    msgBox.style.color = color;

    setTimeout(function () {
        msgBox.innerHTML = "";
    }
        , 3000);
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