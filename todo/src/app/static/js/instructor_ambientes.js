function populateIds4() {
    // Get the URL of the current page
    const urlInstructor = window.location.href;
    console.log("Current URL:", urlInstructor);

    // Split the URL by '/' and filter out any empty parts
    const parts2 = urlInstructor.split('/').filter(part => part !== '');
    console.log("URL parts2 after splitting and filtering:", parts2);
    
    // Get the last part of the URL
    let idInstructor = parts2[parts2.length - 1];
    console.log("Extracted last part of the URL:", idInstructor);

    // Get the hidden input element
    const inputElement = document.getElementById('idInstructor');
    
    // Check if the element exists
    if (inputElement) {
        // Set hidden input value
        inputElement.value = idInstructor;
        console.log("Hidden input value set to:", idInstructor);
    } else {
        console.error("Element with id 'idInstructor' not found.");
    }
}

// Call populateIds when the page loads
window.onload = function() {
    if (document.querySelector(".addClssToAnInstructor")){
        populateIds4()
    }
};
