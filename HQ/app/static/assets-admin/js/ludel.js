document.querySelector('#imageButton').addEventListener('click', function() {
    document.getElementById('imageInput').click();
});
document.getElementById('imageInput').addEventListener('change', function() {
    const form = document.getElementById('myForm');
    form.submit();
});

document.querySelector('#fileButton').addEventListener('click', function() {
    document.getElementById('fileInput').click();
});
document.getElementById('fileInput').addEventListener('change', function() {
    const form = document.getElementById('myForm');
    form.submit();
});

document.querySelector('#videoButton').addEventListener('click', function() {
    document.getElementById('videoInput').click();
});
document.getElementById('videoInput').addEventListener('change', function() {
    const form = document.getElementById('myForm');
    form.submit();
});

document.querySelector('#imageButton2').addEventListener('click', function() {
    document.getElementById('imageInput').click();
});

document.querySelector('#fileButton2').addEventListener('click', function() {
    document.getElementById('fileInput').click();
});

document.querySelector('#videoButton2').addEventListener('click', function() {
    document.getElementById('videoInput').click();
});



let mediaRecorder;
let audioChunks = [];

const startButton = document.getElementById('startButton');
const startButton2 = document.getElementById('startButton2');
const stopButton = document.getElementById('stopButton');
const audioPlayback = document.getElementById('audioPlayback');
const audioInput = document.getElementById('audioInput');

const imageButton = document.getElementById('imageButton');
const fileButton = document.getElementById('fileButton');
const videoButton = document.getElementById('videoButton');
const messageInput = document.getElementById('messageInput');
const for_buttons = document.getElementById('for_buttons');
const form = document.getElementById('myForm');

startButton.addEventListener('click', async () => {
    startButton.disabled = true;
    stopButton.disabled = false;
    startButton.hidden = true;
    stopButton.hidden = false;
    imageButton.hidden = true;
    fileButton.hidden = true;
    videoButton.hidden = true;
    messageInput.hidden = true;

    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);

    mediaRecorder.ondataavailable = (event) => {
        audioChunks.push(event.data);
    };

    mediaRecorder.onstop = () => {
        const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
        const audioUrl = URL.createObjectURL(audioBlob);
        audioPlayback.src = audioUrl;
        audioPlayback.hidden = false;
        stopButton.hidden = true;

        // Créer un fichier et le définir comme valeur de l'input file
        const file = new File([audioBlob], 'recording.wav', { type: 'audio/wav' });
        const dataTransfer = new DataTransfer();
        dataTransfer.items.add(file);
        audioInput.files = dataTransfer.files;

        // Réinitialiser les audioChunks pour un futur enregistrement
        audioChunks = [];
    };

    mediaRecorder.start();
});
startButton2.addEventListener('click', async () => {
    startButton.disabled = true;
    stopButton.disabled = false;
    startButton.hidden = true;
    stopButton.hidden = false;
    imageButton.hidden = true;
    fileButton.hidden = true;
    videoButton.hidden = true;
    messageInput.hidden = true;

    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);

    mediaRecorder.ondataavailable = (event) => {
        audioChunks.push(event.data);
    };

    mediaRecorder.onstop = () => {
        const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
        const audioUrl = URL.createObjectURL(audioBlob);
        audioPlayback.src = audioUrl;
        audioPlayback.hidden = false;
        stopButton.hidden = true;

        // Créer un fichier et le définir comme valeur de l'input file
        const file = new File([audioBlob], 'recording.wav', { type: 'audio/wav' });
        const dataTransfer = new DataTransfer();
        dataTransfer.items.add(file);
        audioInput.files = dataTransfer.files;

        // Réinitialiser les audioChunks pour un futur enregistrement
        audioChunks = [];
    };

    mediaRecorder.start();
});
stopButton.addEventListener('click', () => {
    startButton.disabled = false;
    startButton2.disabled = false;
    stopButton.disabled = true;
    mediaRecorder.stop();
    form.submit();
});


document.addEventListener('DOMContentLoaded', function() {
    function replaceCharacterInParagraphs() {
        // Sélectionne tous les paragraphes avec la classe 'to_affiche'
        const paragraphs = document.querySelectorAll('.to_affiche');

        // Parcourt chaque paragraphe et remplace le caractère '°' par '<br>'
        paragraphs.forEach(paragraph => {
            const originalText = paragraph.innerHTML;
            const newText = originalText.replace(/°/g, '<br>');
            paragraph.innerHTML = newText;
        });
    }

    // Appelle la fonction pour remplacer les caractères
    replaceCharacterInParagraphs();
});