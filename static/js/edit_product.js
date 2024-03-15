
// add_product.js
$(document).ready(function() {
    // Function to handle form submission
    function handleFormSubmission(event) {
        event.preventDefault();
        
        var productname = $('input[name="product_name"]').val();
        var rf_reader_id = $('input[name="rf_reader_id"]').val();
        var available_qty = $('input[name="available_qty"]').val();
        var price = $('input[name="price"]').val();
        
        $.ajax({
            url: '/add_product',
            method: 'POST',
            data: {
                product_name: productname,
                rf_reader_id: rf_reader_id,
                available_qty: available_qty,
                price: price
            },
            success: function(response) {
                if (response.status === 'success') {
                    alert('Product Added Successfully');
                    // Use history.replaceState to change the URL and prevent form resubmission
                    window.location.href = '/product_details';                
                }
                else {                
                    alert('Error adding product. Please try again.');
                }
            },
            error: function() {
                alert('An error occurred. Please try again later.');
            }
        });
    }
    
    // Bind the form submission to the handler function
    $('#addProductForm').on('submit', handleFormSubmission);
});

// delete product
function showConfirmation() {
    if (confirm('Are you sure you want to update the product details?')) {
      document.getElementById('editproduct').submit();
    }
  }
  function closePage() {
    if (confirm('Are you sure you want to close the page?')) {
        window.location.href = '/product_details';
    }
}  

// logic for apply filter in product details page
document.addEventListener('DOMContentLoaded', function() {
    var filterForm = document.getElementById('kt-toolbar-filter');
    var tableRows = document.querySelectorAll('#product-table tbody tr');

    filterForm.addEventListener('click', function(event) {
        if (event.target.matches('.btn-primary')) {
            applyFilters();
        }
    });

    function applyFilters() {
        var minPrice = parseFloat(document.querySelector('[data-kt-range-filter="min_price"]').value) || 0;
        var maxPrice = parseFloat(document.querySelector('[data-kt-range-filter="max_price"]').value) || Number.MAX_SAFE_INTEGER;
        var minQuantity = parseInt(document.querySelector('[data-kt-range-filter="min_quantity"]').value) || 0;
        var maxQuantity = parseInt(document.querySelector('[data-kt-range-filter="max_quantity"]').value) || Number.MAX_SAFE_INTEGER;

        tableRows.forEach(function(row) {
            var price = parseFloat(row.getAttribute('data-price'));
            var quantity = parseInt(row.querySelector('.available-qty').textContent);

            var hideRow = false;

            if ((price >= minPrice && price <= maxPrice) || (quantity >= minQuantity && quantity <= maxQuantity)) {
                hideRow = false;
            } else {
                hideRow = true;
            }

            if (hideRow) {
                row.style.display = 'none';
            } else {
                row.style.display = '';
            }
        });
    }

    function resetFilters() {
        // Clear input values
        var inputFields = document.querySelectorAll('[data-kt-range-filter]');
        inputFields.forEach(function(input) {
            input.value = '';
        });

        // Show all table rows
        tableRows.forEach(function(row) {
            row.style.display = '';
        });
    }
});

// for search logic 
document.addEventListener("DOMContentLoaded", function() {
    const searchInput = document.getElementById("searchProducts");
    const dataTable = document.querySelectorAll("#kt_customers_table tbody tr");
    let hiddenRows = []; // Store hidden rows

    searchInput.addEventListener("input", function() {
        const searchValue = searchInput.value.toLowerCase();

        dataTable.forEach((row, index) => {
            const nameColumn = row.querySelector("td:nth-child(2)"); // Assuming product name is in the second column
            const name = nameColumn.textContent.toLowerCase();
            const matchIndex = name.indexOf(searchValue);

            if (matchIndex !== -1) {
                const beforeMatch = name.substring(0, matchIndex);
                const matchedText = name.substring(matchIndex, matchIndex + searchValue.length);
                const afterMatch = name.substring(matchIndex + searchValue.length);

                nameColumn.innerHTML = `${beforeMatch}<span >${matchedText}</span>${afterMatch}`;

                // Make the row visible
                row.style.display = "";
                // Remove from hiddenRows if it was there
                if (hiddenRows.includes(index)) {
                    hiddenRows.splice(hiddenRows.indexOf(index), 1);
                }
            } else {
                nameColumn.innerHTML = name;
                row.style.display = "none";

                // Add to hiddenRows if not already there
                if (!hiddenRows.includes(index)) {
                    hiddenRows.push(index);
                }
            }
        });
    });
});

// Close Page Functionality
function closePage() {
    if (confirm('Are you sure you want to close the page?')) {
        history.back();
    }
}
