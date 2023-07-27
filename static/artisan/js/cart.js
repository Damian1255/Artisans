function deleteItemFromCart(product_id) {
    // Ajax call to add product to cart
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/cart/delete/item/', true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    xhr.onload = function () {
        if (xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
            if (response.success) {
                location.reload();
            } else {
                alert("Product removal from cart failed.")
            }
        } else {
            alert('An Internal error occurred.');
        }
    };
    
    xhr.send(JSON.stringify({
        product_id : product_id
    }));
}

function clearCart() {
    // Ajax call to add product to cart
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/cart/clear/', true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    xhr.onload = function () {
        if (xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
            if (response.success) {
                location.reload();
            } else {
                alert("Cart clear failed.")
            }
        } else {
            alert('An Internal error occurred.');
        }
    };
    
    xhr.send();
}

function updateCart(cart_id, newquantity) {
    quantityPicker = document.getElementById("quantity-" + cart_id)
    quantity_value = parseInt(quantityPicker.value) + newquantity;

    if (quantity_value >= 1 && quantity_value <= quantityPicker.max) {
        // Ajax call to add product to cart
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/cart/update/', true);
        xhr.setRequestHeader('Content-Type', 'application/json');

        xhr.onload = function () {
            if (xhr.status === 200) {
                var response = JSON.parse(xhr.responseText);
                if (response.success) {
                    getCart();
                } else {
                    alert("Cart update failed.")
                }
            } else {
                alert('An Internal error occurred.');
            }
        };
        
        xhr.send(JSON.stringify({
            cart_id : cart_id,
            quantity : quantity_value
        }));
    }
}