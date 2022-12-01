let synth = window.speechSynthesis;
let utterance = new SpeechSynthesisUtterance("Das ist ein langer Beispieltext, um zu testen, ob pausieren und fortfahren funktioniert");

let context = new AudioContext();
var sound = new Audio(synth.speak(utterance));
let source = context.createMediaElementSource(sound);
let gain = context.createGain();

source.connect(gain);
gain.connect(context.destination);

gain.gain.value = 10;

document.querySelector("#playStopButton").addEventListener("click", function(e) {
    //synth.speak(utterance);
    sound.play();
});

document.querySelector("#pauseButton").addEventListener("click", function(e) {
    //synth.pause();
});

document.querySelector("#resumeButton").addEventListener("click", function(e) {
    //synth.resume();
});