// searchScript.js
document.addEventListener("DOMContentLoaded", function() {
    const searchInput = document.getElementById("searchShop");
    const dataTable = document.querySelectorAll("#kt_table_users tbody tr");
    let hiddenRows = []; // Store hidden rows

    searchInput.addEventListener("input", function() {
        const searchValue = searchInput.value.toLowerCase();

        dataTable.forEach((row, index) => {
            const shopNameColumn = row.querySelector("td:nth-child(2)"); // Shop name is in the 2nd column
            const shopName = shopNameColumn.textContent.toLowerCase();
            const matchIndex = shopName.indexOf(searchValue);

            if (matchIndex !== -1) {
                const beforeMatch = shopName.substring(0, matchIndex);
                const matchedText = shopName.substring(matchIndex, matchIndex + searchValue.length);
                const afterMatch = shopName.substring(matchIndex + searchValue.length);

                shopNameColumn.innerHTML = `${beforeMatch}<span>${matchedText}</span>${afterMatch}`;

                // Make the row visible
                row.style.display = "";
                // Remove from hiddenRows if it was there
                if (hiddenRows.includes(index)) {
                    hiddenRows.splice(hiddenRows.indexOf(index), 1);
                }
            } else {
                shopNameColumn.innerHTML = shopName;
                row.style.display = "none";

                // Add to hiddenRows if not already there
                if (!hiddenRows.includes(index)) {
                    hiddenRows.push(index);
                }
            }
        });
    });
});
