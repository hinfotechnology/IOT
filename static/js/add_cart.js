// Get all "Add to Cart" buttons by their class name
const addToCartButtons = document.querySelectorAll('.addToCartBtn');

// Create an empty shopping cart (an array to store products)
const shoppingCart = [];

// Function to add a product to the shopping cart
function addToCart(event) {
    const button = event.target;
    const productName = button.getAttribute('data-name');
    const productQuantity = parseInt(button.getAttribute('data-quantity'));
    const productPrice = parseFloat(button.getAttribute('data-price'));

    // Create a product object
    const product = {
        name: productName,
        quantity: productQuantity,
        price: productPrice
    };

    // Add the product to the shopping cart
    shoppingCart.push(product);

    // You can update the cart UI or send the data to a server here
}

// Attach a click event listener to each "Add to Cart" button
addToCartButtons.forEach(button => {
    button.addEventListener('click', addToCart);
});


// Function to display cart items on the "View Cart" page
function displayCart() {
    const cartItems = document.getElementById('cartItems');
    const totalPriceElement = document.getElementById('totalPrice');
    let totalPrice = 0;

    // Clear existing cart items
    cartItems.innerHTML = '';

    // Iterate through the shopping cart and display each item
    shoppingCart.forEach(item => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${item.name}</td>
            <td>${item.quantity}</td>
            <td>$${item.price.toFixed(2)}</td>
            <td>$${(item.quantity * item.price).toFixed(2)}</td>
        `;

        cartItems.appendChild(row);

        // Calculate total price
        totalPrice += item.quantity * item.price;
    });

    // Update the total price
    totalPriceElement.textContent = totalPrice.toFixed(2);
}

// Call the displayCart function when the "View Cart" page loads
window.addEventListener('load', displayCart);
