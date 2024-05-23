function getIdFromUrl(url) {
    const parts = url.split('/');
    return {
        workstationId: parts[parts.length - 2], // Second last part
        elementId: parts[parts.length - 1]      // Last part
    };
}

function populateIds() {
    // Get the URL of the current page
    const urlPuestoTrabajo = window.location.href;
    
    // Extract idPuestoTrabajo and idElemento from the URL
    const { workstationId, elementId } = getIdFromUrl(urlPuestoTrabajo);
    console.log({ workstationId, elementId })
    // Set hidden input values
    const r1 = document.getElementById('idPuestoTrabajo').value = workstationId;
    console.log("idPuestoTrabajo", r1)
    const r2 = document.getElementById('idElemento').value = elementId;
    console.log("idElemento", r2)
}

// Call populateIds when the page loads
window.onload = function() {
    if (document.querySelector(".createANovelty")){
        populateIds()
    }
};