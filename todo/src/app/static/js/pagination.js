const rowsPerPage = 5;
let currentPage = 1;

// Function to fetch data from the server
async function fetchData(page) {
    const response = await fetch(`/novedades?page=${page}&per_page=${rowsPerPage}`, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    });
    const data = await response.json();
    return data;
}

// Function to display table based on current page
async function displayTable(page) {
    if (page < 1) return; // Prevent going to a negative page
    const data = await fetchData(page);
    const tableBody = document.querySelector("#myTable tbody");

    // Clear existing table rows
    tableBody.innerHTML = "";

    // Populate table with data
    data.cadena.forEach(item => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${data.idPT_dict[item[1]] || ''}</td>
            <td>${data.idElemento_dict[item[2]] || ''}</td>
            <td>${item[3]}</td>
            <td>${item[4]}</td>
        `;
        tableBody.appendChild(row);
    });

    // Update pagination
    updatePagination(page, data.can);

    // Update current page
    currentPage = page;

    // Disable buttons if out of range
    document.getElementById('prevButton').disabled = (currentPage === 1);
    document.getElementById('nextButton').disabled = (currentPage * rowsPerPage >= data.can);
}

// Function to update pagination links
function updatePagination(currentPage, totalItems) {
    const pageCount = Math.ceil(totalItems / rowsPerPage);
    const paginationContainer = document.getElementById("pagination");

    // Clear existing pagination links
    paginationContainer.innerHTML = "";

    // Add pagination links
    for (let i = 1; i <= pageCount; i++) {
        const pageLink = document.createElement("a");
        pageLink.href = "#";
        pageLink.innerText = i;
        pageLink.onclick = function (event) {
            event.preventDefault();
            displayTable(i);
        };
        if (i === currentPage) {
            pageLink.style.fontWeight = "bold";
        }
        paginationContainer.appendChild(pageLink);
        paginationContainer.appendChild(document.createTextNode(" "));
    }
}

// Attach event listeners to the buttons
document.getElementById('prevButton').addEventListener('click', () => {
    if (currentPage > 1) {
        displayTable(currentPage - 1);
    }
});

document.getElementById('nextButton').addEventListener('click', () => {
    displayTable(currentPage + 1);
});

// Initial display
document.addEventListener("DOMContentLoaded", function() {
    displayTable(currentPage);
});
