function populateIds2() {
    // Get the URL of the current page
    const urlPuestoTrabajo2 = window.location.href;
    console.log("Current URL:", urlPuestoTrabajo2);

    // Split the URL by '/' and filter out any empty parts
    const parts2 = urlPuestoTrabajo2.split('/').filter(part => part !== '');
    console.log("URL parts2 after splitting and filtering:", parts2);
    
    // Get the last part of the URL
    let idPuestoTrabajo = parts2[parts2.length - 1];
    console.log("Extracted last part of the URL:", idPuestoTrabajo);

    // Get the hidden input element
    const inputElement = document.getElementById('idPuestoTrabajo');
    
    // Check if the element exists
    if (inputElement) {
        // Set hidden input value
        inputElement.value = idPuestoTrabajo;
        console.log("Hidden input value set to:", idPuestoTrabajo);
    } else {
        console.error("Element with id 'idPuestoTrabajo' not found.");
    }
}

// Call populateIds when the page loads
window.onload = function() {
    if (document.querySelector(".addElementsToAWorkstation")){
        populateIds2()
    }
};
