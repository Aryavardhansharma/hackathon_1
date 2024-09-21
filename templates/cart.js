const prices = {
    item1: 29.99,
    item2: 49.99,
};

function updatePrice(item) {
    const quantityInput = document.getElementById(`quantity-${item}`);
    const quantity = parseInt(quantityInput.value);
    const totalPrice = (prices[item] * quantity).toFixed(2);
    document.getElementById(`total-price-${item}`).textContent = `$${totalPrice}`;
    updateGrandTotal();
}

function changeQuantity(item, change) {
    const quantityInput = document.getElementById(`quantity-${item}`);
    let quantity = parseInt(quantityInput.value);
    quantity += change;
    if (quantity < 1) quantity = 1; // Prevent quantity from going below 1
    quantityInput.value = quantity;
    updatePrice(item);
}

function updateGrandTotal() {
    const totalItem1 = parseFloat(document.getElementById('total-price-item1').textContent.slice(1)) || 0;
    const totalItem2 = parseFloat(document.getElementById('total-price-item2').textContent.slice(1)) || 0;
    const grandTotal = (totalItem1 + totalItem2).toFixed(2);
    document.getElementById('grand-total').textContent = `$${grandTotal}`;
}

function processPayment() {
    const cardName = document.getElementById('card-name').value;
    const cardNumber = document.getElementById('card-number').value;
    const expiryDate = document.getElementById('expiry-date').value;
    const cvv = document.getElementById('cvv').value;

    if (cardName && cardNumber && expiryDate && cvv) {
        alert(`Payment processed for ${cardName} with total amount: ${document.getElementById('grand-total').textContent}`);
    } else {
        alert("Please fill out all payment information.");
    }
}

// Initialize the total prices on page load
updatePrice('item1');
updatePrice('item2');
