const container = document.getElementById('container');


const numberOfBoxes = 20; 

for (let i = 1; i <= numberOfBoxes; i++) {
    
    const box = document.createElement('div');

    box.className = 'box';
    
    box.textContent = `Caja ${i}`;
    
    container.appendChild(box);
}