const rowsPerPage = 5;
let currentPage = 1;

// Function to fetch data from the server
async function fetchData(page) {
    try {
        const response = await fetch(`/novedades?page=${page}&per_page=${rowsPerPage}`, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        });
        if (!response.ok) {
            throw new Error('Network response was not ok.');
        }
        const data = await response.json();
        console.log('Fetched data:', data); // Log fetched data
        return data;
    } catch (error) {
        console.error('Fetching data failed:', error);
        // Handle error, show a message to the user, etc.
    }
}

// Function to display table based on current page
async function displayTable(page) {
    if (page < 1) return; // Prevent going to a negative page
    const data = await fetchData(page);
    if (!data) return;

    const tableBody = document.querySelector("#myTable tbody");

    // Clear existing table rows
    tableBody.innerHTML = "";

    // Populate table with data
    data.cadena.forEach(item => {
        const row = document.createElement("tr");
        let elementosHTML = '';

        // Handle different data formats
        if (Array.isArray(item[2])) {
            elementosHTML = item[2].map(elem => `${data.idElemento_dict[elem]}`).join('<br>');
        } else {
            elementosHTML = data.idElemento_dict[item[1]];
        }

        row.innerHTML = `
            <td>${data.idPT_dict[item[1]] || item[1]}</td>
            <td>${elementosHTML}</td>
            <td>${item[3]}</td>
            <td>${item[4]}</td>
            <td><button class="btn w3-red w3-hover-yellow" onclick='Confirmar("Desea Borrar el novedad?", "/novedades/d/${item[0]}")' title="Borrar"><i class="fa fa-trash"></i></button></td>
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

    for (let i = 1; i <= pageCount; i++) {
        const pageLink = document.createElement("a");
        pageLink.href = "#";
        pageLink.textContent = i;
        pageLink.classList.add("pagination-link");
        if (i === currentPage) {
            pageLink.classList.add("active");
        }
        pageLink.addEventListener("click", (event) => {
            event.preventDefault();
            displayTable(i);
        });
        paginationContainer.appendChild(pageLink);
    }
}

// Event listeners for pagination buttons
document.getElementById("prevButton").addEventListener("click", () => {
    if (currentPage > 1) {
        displayTable(currentPage - 1);
    }
});
document.getElementById("nextButton").addEventListener("click", () => {
    displayTable(currentPage + 1);
});

// Initial display
document.addEventListener('DOMContentLoaded', () => {
    displayTable(1);
});
