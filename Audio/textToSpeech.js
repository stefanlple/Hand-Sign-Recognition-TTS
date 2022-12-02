let context = new AudioContext();
var sound = new Audio("../speech.mp3");
let source = context.createMediaElementSource(sound);
let gain = context.createGain();
let isPlaying = false;

source.connect(gain);
gain.connect(context.destination);

gain.gain.value = 1;

document.querySelector("#playStopButton").addEventListener("click", function(e) {
    if (isPlaying) {
        sound.pause();
        e.target.innerHTML = "Play";
    } else {
        sound.play();
        e.target.innerHTML = "Stop";
    }
    isPlaying = !isPlaying;
});