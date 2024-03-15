// for search logic 
document.addEventListener("DOMContentLoaded", function() {
    const searchInput = document.getElementById("searchCustomer");
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
