function getIdFromUrl(url) {
    const parts = url.split('/');
    return {
        idAmbiente: parts[parts.length - 1], // Second last part
    };
}

function populateIds() {
    // Get the URL of the current page
    const urlAmbiente = window.location.href;
    
    // Extract idPuestoTrabajo and idElemento from the URL
    const { idAmbiente } = getIdFromUrl(urlAmbiente);
    console.log({ idAmbiente })
    // Set hidden input values
    const r1 = document.getElementById('idAmbiente').value = idAmbiente;
    console.log("idAmbiente", r1)
}

// Call populateIds when the page loads
window.onload = function() {
    if (document.querySelector(".createGeneralANovelty")){
        populateIds()
    }
};