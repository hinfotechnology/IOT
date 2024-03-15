{/* <script> */}
// Retrieve cart items from localStorage
var cart = JSON.parse(localStorage.getItem('cart')) || [];

// Get the cart items container element
var cartItemsContainer = document.getElementById('cart-items');

// Initialize total price
var totalPrice = 0;

// Loop through each item in the cart and add it to the cart view
cart.forEach(function (item) {
    var row = document.createElement('tr');
    row.innerHTML = `
        <td>${item.name}</td>
        <td>${item.quantity}</td>
        <td>$${item.price}</td>
        <td>$${(item.quantity * item.price).toFixed(2)}</td>
    `;
    cartItemsContainer.appendChild(row);

    // Update the total price
    totalPrice += item.quantity * item.price;
});

// Display the total price
var totalPriceElem = document.getElementById('total-price');
totalPriceElem.textContent = '$' + totalPrice.toFixed(2);
// Calculate the total price of items in the cart
function calculateTotalPrice(cart) {
    let totalPrice = 0;
    for (const item of cart) {
        totalPrice += item.quantity * item.price;
    }
    return totalPrice;
}


{/* </script> */}
