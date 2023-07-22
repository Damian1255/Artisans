var addcartbtn = document.getElementById("add-cart-btn");
var quantity = document.getElementById("quantity-value");
var product_id = document.getElementById("product-id");

addcartbtn.addEventListener("click", function (event) {
    // Ajax call to add product to cart
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/cart/add/', true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    xhr.onload = function () {
        if (xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
            if (response.success) {
                alert("Product added to cart successfully!")
            } else {
                alert("Product add to cart failed.")
            }
        } else {
            alert('An Internal error occurred.');
        }
    };
    
    xhr.send(JSON.stringify({
        product_id : product_id.value,
        quantity : quantity.value
    }));
});

function show_error(message) {
    var msgBox = document.getElementById("login-msg-box");
    msgBox.innerHTML = message;
}