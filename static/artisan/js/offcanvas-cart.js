function getCart() {
    cartCount = document.getElementById("bag-number");
    cartList = document.getElementById("mini-cart");
    cartTitle = document.getElementById("cart-title");

    cartItem = document.getElementById("item-display");
    grandTotal = document.getElementById("grand-total");
    cartPageTitle = document.getElementById("cart-page-title");

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/cart/', true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    xhr.onload = function () {
        if (xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
            if (response.success) {
                cartCount.innerHTML = response.cart_count;
                cartList.innerHTML = response.offcanvas_cart;
                cartTitle.innerHTML = "Cart (" + response.cart_count + ")";

                try {
                    cartItem.innerHTML = response.cart_display;
                    grandTotal.innerHTML = response.total_display;
                    cartPageTitle.innerHTML = "Your cart items (" + response.cart_count + ")";
                } catch (error) {
                    console.log("Cart Aborted")
                }
                
            } else {
                alert("Unable to get cart.")
            }
        } else {
            alert('An Internal error occurred.');
        }
    };

    xhr.send();
}

getCart();