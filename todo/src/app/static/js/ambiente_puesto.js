function populateIds3() {
    // Get the URL of the current page
    const urlAmbiente = window.location.href;
    console.log("Current URL:", urlAmbiente);

    // Split the URL by '/' and filter out any empty parts
    const parts2 = urlAmbiente.split('/').filter(part => part !== '');
    console.log("URL parts2 after splitting and filtering:", parts2);
    
    // Get the last part of the URL
    let idAmbiente = parts2[parts2.length - 1];
    console.log("Extracted last part of the URL:", idAmbiente);

    // Get the hidden input element
    const inputElement = document.getElementById('idAmbiente');
    
    // Check if the element exists
    if (inputElement) {
        // Set hidden input value
        inputElement.value = idAmbiente;
        console.log("Hidden input value set to:", idAmbiente);
    } else {
        console.error("Element with id 'idAmbiente' not found.");
    }
}

// Call populateIds when the page loads
window.onload = function() {
    if (document.querySelector(".addWorkstationsToALearningClassroom")){
        populateIds3()
    }
};
