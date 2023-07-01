var editing = false;

var first_name_container = document.querySelector("#first-name-container");
var last_name_container = document.querySelector("#last-name-container");
var email_container = document.querySelector("#email-container");
var birthdate_container = document.querySelector("#birthdate-container");
var password_container = document.querySelector("#password-container");
var save_button_container = document.querySelector("#save-button-container");
var edit_button = document.querySelector("#edit-button");

var tmp_first_name = first_name_container.lastElementChild.innerHTML;
var tmp_last_name = last_name_container.lastElementChild.innerHTML;
var tmp_email = email_container.lastElementChild.innerHTML;
var tmp_birthdate = birthdate_container.lastElementChild.innerHTML;
var tmp_password = password_container.lastElementChild.innerHTML;

edit_button.addEventListener("click", function (event) {
    if (!editing) {
        editing = true;
        edit_button.innerHTML = "Cancel"
        first_name_container.innerHTML = '<label>First Name</label><input type="text" name="first-name" value="'+ tmp_first_name +'">'
        last_name_container.innerHTML = '<label>Last Name</label><input type="text" name="last-name" value="'+ tmp_last_name +'">'
        email_container.innerHTML = '<label>Email</label><input type="text" name="email" value="'+ tmp_email +'">'
        birthdate_container.innerHTML = '<label>Birthdate</label><input type="date" name="dob" value="'+ tmp_birthdate +'">'
        password_container.innerHTML = '<label>Password</label><input type="password" name="password" value="'+ tmp_password +'">'
        save_button_container.innerHTML = '<button class="btn" type="submit" id="save-button">Save</button>'
    } else { 
        editing = false;
        edit_button.innerHTML = "Edit"
        first_name_container.innerHTML = '<label>First Name</label><p>' + tmp_first_name + '</p>'
        last_name_container.innerHTML = '<label>Last Name</label><p>' + tmp_last_name + '</p>'
        email_container.innerHTML = '<label>Email</label><p>' + tmp_email + '</p>'
        birthdate_container.innerHTML = '<label>Birthdate</label><p>' + tmp_birthdate + '</p>'
        password_container.innerHTML = '<label>Password</label><p>' + tmp_password + '</p>'
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
    var password = updateForm.querySelector("input[name='password']");
    var dob = updateForm.querySelector("input[name='dob']");

    // clear any highlighted elements
    remove_highlight([password])

    // Ajax call to register user 
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/account/update-user/' + id, true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    xhr.onload = function () {
        if (xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);

            if (response.success) {
                show_msg("User updated successfully!", "green")
                tmp_first_name = first_name.value;
                tmp_last_name = last_name.value;
                tmp_email = email.value;
                tmp_birthdate = dob.value;
                tmp_password = password.value;

                edit_button.click();
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