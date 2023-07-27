var editing = false;

var first_name_container = document.querySelector("#first-name-container");
var last_name_container = document.querySelector("#last-name-container");
var email_container = document.querySelector("#email-container");
var birthdate_container = document.querySelector("#birthdate-container");
var save_button_container = document.querySelector("#save-button-container");
var edit_button = document.querySelector("#edit-button");

var tmp_first_name = first_name_container.lastElementChild.innerHTML;
var tmp_last_name = last_name_container.lastElementChild.innerHTML;
var tmp_email = email_container.lastElementChild.innerHTML;
var tmp_birthdate = birthdate_container.lastElementChild.innerHTML;

edit_button.addEventListener("click", function (event) {
    if (!editing) {
        editing = true;
        edit_button.innerHTML = "Cancel"
        first_name_container.innerHTML = '<label>First Name</label><input type="text" name="first-name" value="' + tmp_first_name + '">'
        last_name_container.innerHTML = '<label>Last Name</label><input type="text" name="last-name" value="' + tmp_last_name + '">'
        email_container.innerHTML = '<label>Email</label><input type="text" name="email" value="' + tmp_email + '">'
        birthdate_container.innerHTML = '<label>Birthdate</label><input type="date" name="dob" value="' + tmp_birthdate + '">'
        save_button_container.innerHTML = '<button class="btn" type="submit" id="save-button">Save</button>'
    } else {
        editing = false;
        edit_button.innerHTML = "Edit"
        first_name_container.innerHTML = '<label>First Name</label><p>' + tmp_first_name + '</p>'
        last_name_container.innerHTML = '<label>Last Name</label><p>' + tmp_last_name + '</p>'
        email_container.innerHTML = '<label>Email</label><p>' + tmp_email + '</p>'
        birthdate_container.innerHTML = '<label>Birthdate</label><p>' + tmp_birthdate + '</p>'
        save_button_container.innerHTML = ''
    }
});

var updateForm = document.querySelector("#update-form");

updateForm.addEventListener("submit", function (event) {
    event.preventDefault();

    var id = updateForm.querySelector("input[name='id']").value;
    var first_name = updateForm.querySelector("input[name='first-name']");
    var last_name = updateForm.querySelector("input[name='last-name']");
    var email = updateForm.querySelector("input[name='email']");
    var dob = updateForm.querySelector("input[name='dob']");

    // Ajax call to register user 
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/account/update-user/' + id, true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    xhr.onload = function () {
        if (xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);

            if (response.success) {
                tmp_first_name = first_name.value;
                tmp_last_name = last_name.value;
                tmp_email = email.value;
                tmp_birthdate = dob.value;

                edit_button.click();
                document.getElementById("UserUpdateDialog").showModal();
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
        dob: dob.value,
    }));
});

var passwordUpdateForm = document.getElementById("password-update-form");
var current_password = passwordUpdateForm.querySelector("input[name='current_password']");
var new_password = passwordUpdateForm.querySelector("input[name='new_password']");
var confirm_password = passwordUpdateForm.querySelector("input[name='confirm_password']");
var msg = document.getElementById("msg");

passwordUpdateForm.addEventListener("submit", function (event) {
    event.preventDefault();
    
    remove_highlight([current_password, new_password, confirm_password])
    msg.innerHTML = ""

    if (new_password.value != confirm_password.value) {
        highlight_elements_red([new_password, confirm_password])
        msg.innerHTML = "Passwords do not match."
        return
    }
    // Ajax call to update password
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/account/password/update', true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    xhr.onload = function () {
        if (xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);

            if (response.success) {
                passwordUpdateForm.reset();
                document.getElementById("AccountUpdateDialog").close();
                document.getElementById("PasswordUpdateDialog").showModal()
            } else {
                msg.innerHTML = "Current password is incorrect."
                highlight_elements_red([current_password])
            }
        } else {
            alert('An Internal error occurred.');
        }
    };
    xhr.send(JSON.stringify({
        user_id: passwordUpdateForm.querySelector("input[name='pwd_customer_id']").value,
        current_password: current_password.value,
        new_password: new_password.value,
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