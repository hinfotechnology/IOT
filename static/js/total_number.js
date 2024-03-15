function fetchAllData() {
    fetch('/get_data')
      .then(response => response.json())
      .then(data => {
        document.getElementById('numPurchasers').textContent = data.num_purchasers;
        document.getElementById('numProducts').textContent = data.num_products;
        document.getElementById('totalQuantity').textContent = data.total_quantity;
      })
      .catch(error => {
        console.error('Error fetching general data:', error);
      });
  
    fetch('/all_stock_data')
        .then(response => response.json())
        .then(data => {          
            // Update out-of-stock table
            updateTable('outOfStockTable', data.out_of_stock_products);

            // Update soon out-of-stock table
            updateTable('soonOutOfStockTable', data.soon_out_of_stock_products);
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
}

function updateTable(tableId, data) {
    const table = document.getElementById(tableId);
    table.innerHTML = ''; // Clear existing table content

    if (data.length > 0) {
        const tableHeader = '<thead><tr><th>RFID</th><th>Product Name</th><th>Quantity</th></tr></thead>';
        table.innerHTML += tableHeader;

        // Create table body
        const tableBody = document.createElement('tbody');
        data.forEach(product => {
            const row = `<tr style="text-align: center;"><td>${product.rfid}</td><td>${product.product_name}</td><td>${product.quantity}</td></tr>`;
            tableBody.innerHTML += row;
        });

        table.appendChild(tableBody);
    } else {
        table.innerHTML = `<tbody><tr><td colspan="2"> ${tableId === 'outOfStockTable' ? 'No out-of-stock' : 'No'} products found.</td></tr></tbody>`;
        table.style.tabletTextAlign="center"
    
    }

    
    table.style.borderCollapse='collapse'
    table.style.borderSpacing = '2px';
}

// Fetch all data when the DOM content is loaded
document.addEventListener('DOMContentLoaded', function () {
    fetchAllData(); 
});
