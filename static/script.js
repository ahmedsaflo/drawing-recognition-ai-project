const canvas = document.getElementById('cizimAlani');
const ctx = canvas.getContext('2d');

let cizim = false;
ctx.fillStyle = 'white';
ctx.fillRect(0, 0, canvas.width, canvas.height);

canvas.addEventListener('mousedown', () => { cizim = true; });
canvas.addEventListener('mouseup', () => { cizim = false; ctx.beginPath(); });
canvas.addEventListener('mousemove', (event) => {
    if (!cizim) return;
    ctx.lineWidth = 5;
    ctx.lineCap = 'round';
    ctx.strokeStyle = 'black';
    ctx.lineTo(event.clientX - canvas.offsetLeft, event.clientY - canvas.offsetTop);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(event.clientX - canvas.offsetLeft, event.clientY - canvas.offsetTop);
});
document.getElementById('kaydetButonu').addEventListener('click', () => {
    const imageData = canvas.toDataURL('image/png'); 
    fetch('/kaydet', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ image: imageData }),
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
    })
    .catch(error => {
        console.error('Hata:', error);
    });
});
document.getElementById('temizleButonu').addEventListener('click', () => {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = 'white'; 
    ctx.fillRect(0, 0, canvas.width, canvas.height);
});