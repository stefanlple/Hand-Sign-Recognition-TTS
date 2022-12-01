let synth = window.speechSynthesis;
let utterance = new SpeechSynthesisUtterance("Das ist ein langer Beispieltext, um zu testen, ob pausieren und fortfahren funktioniert");


document.querySelector("#playStopButton").addEventListener("click", function(e) {
    synth.speak(utterance);
});

document.querySelector("#pauseButton").addEventListener("click", function(e) {
    synth.pause();
});

document.querySelector("#resumeButton").addEventListener("click", function(e) {
    synth.resume();
});