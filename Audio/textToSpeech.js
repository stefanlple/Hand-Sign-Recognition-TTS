/* Websocket */
let request = "request data";
const webSocket = new WebSocket("ws://localhost:8765");

webSocket.addEventListener("open", () => {
    console.log("We are connected!");

    webSocket.send(request);
});

webSocket.addEventListener("message", e => {
    console.log(e);
    if (e.data instanceof Blob) {
       //console.log(e.data); //blob data

       temp = e.data.text().then((value) => { //wait for the value of the text component from the blob to be read
        
        //console.log(value);           //undecoded base64 text
        let decodedText = atob(value);  //decodes base64
        //console.log(decodedText);     //decoded bas64 text

        let stringHexArray = (convertToHex(decodedText)).split(" "); //array of wav file with hex values as strings

        for (let i = 1; i < stringHexArray.length; i++) {
            let hex = parseInt(stringHexArray[i], 16); //converts each element from hex values as strings to ints (16 for hex)
            audioArray[i - 1] = hex; //ignores first element ("")
        }

        console.log(audioArray); //fully decoded array of the whole .wav-file (ready to use in WebAudio)

        playByteArray(audioArray);

       });
    }
});

function convertToHex(str) {
    var hex = '';
    for(var i=0;i<str.length;i++) {
        hex += ' '+str.charCodeAt(i).toString(16);
    }
    return hex;
}

/* Web Audio */
var context = new AudioContext();
let audioArray = [];
var buf; //audio buffer
var source; //contains the current audioBufferSourceNode after its creation

let gain = context.createGain();
let stereoPanner = context.createStereoPanner();
let convolver = context.createConvolver();
let filter = context.createBiquadFilter();

let selectListFilter = document.querySelector("#selectListFilter");

let isPlaying = false;
var startTime;
let elapsedTime = 0; //elapsed time between two button presses
let totalElapsedTime = 0; //total playtime of the sound
let stoppedWithButton = false;

stereoPanner.connect(filter);
filter.connect(context.destination);


function playByteArray(byteArray) {

    var arrayBuffer = new ArrayBuffer(byteArray.length);
    var bufferView = new Uint8Array(arrayBuffer);
    for (i = 0; i < byteArray.length; i++) {
      bufferView[i] = byteArray[i];
    }

    context.decodeAudioData(arrayBuffer, function(buffer) {
        buf = buffer;
    });
}

//play the loaded file (has to be called everytime because the audioBufferSourceNode is a one way use object)
function play(offset) {
    //create a source node from the buffer
    source = context.createBufferSource();
    source.buffer = buf;
    //connect to the gain node
    source.connect(gain);
    //play immediately with offset (offset = 0 -> start from beginning)
    source.start(0, offset);
    //source.loop = true;

    startTime = Date.now();

    source.addEventListener("ended", function(e) {
        isPlaying = false;

        if (!stoppedWithButton) {
            //sound ended because it was fully played
            elapsedTime = 0;
            totalElapsedTime = 0;
        } else {
            //sound ended because the button was pressed
            stoppedWithButton = false;
        }
        
        document.querySelector("#playStopButton").innerHTML = "Play";
    });
}

function stop() {
    stoppedWithButton = true;
    source.stop(0);
    elapsedTime = (Date.now() - startTime) / 1000; //elapsed time in seconds
    //console.log("Elapsed time in seconds: " + elapsedTime);
    totalElapsedTime = totalElapsedTime + elapsedTime;
    //console.log("Total elapsed time in seconds: " + totalElapsedTime);
}

function loadImpulseResponse(name) {
    if (name !== "none") {
        fetch("impulseResponses/" + name + ".wav")
            .then(response => response.arrayBuffer())
            .then(undecodedAudio => context.decodeAudioData(undecodedAudio))
            .then(audioBuffer => {
                if (convolver) {convolver.disconnect();}

                convolver = context.createConvolver();
                convolver.buffer = audioBuffer;
                convolver.normalize = true;

                gain.connect(convolver);
                convolver.connect(stereoPanner);
            })
            .catch(console.error);
    } else {
        if (convolver) {convolver.disconnect();}
        gain.connect(stereoPanner);
    }
}

loadImpulseResponse("none");

//resets slider handle positions when (re-)loading
document.querySelector("#gainSlider").value = 10;
document.querySelector("#panningSlider").value = 50;
document.querySelector("#frequencySlider").value = 1000;
document.querySelector("#detuneSlider").value = 0;
document.querySelector("#qSlider").value = 0;
document.querySelector("#gainSliderFilter").value = 0;

//resets the display of the selected element when (re-)loading
document.querySelector("#selectList").value = "none";
selectListFilter.value = "lowpass";

document.querySelector("#playStopButton").addEventListener("click", function(e) {
    if (isPlaying) {
        stop();
        e.target.innerHTML = "Play";
    } else {
        play(totalElapsedTime);
        e.target.innerHTML = "Stop";
    }
    isPlaying = !isPlaying;
});

document.querySelector("#testButton").addEventListener("click", function(e) {
    webSocket.send("test");
 });

 /** Gain */
 document.querySelector("#gainSlider").addEventListener("input", function(e) {
    let gainValue = (this.value / 10);
    document.querySelector("#gainOutput").innerHTML = gainValue + " dB";
    gain.gain.value = gainValue;
});

/** Panning */
document.querySelector("#panningSlider").addEventListener("input", function(e) {
    let panValue = ((this.value - 50) / 50);
    document.querySelector("#panningOutput").innerHTML = panValue + " LR";
    stereoPanner.pan.value = panValue;
});

/** Reverb */
document.querySelector("#selectList").addEventListener("change", function(e) {
    let name = e.target.options[e.target.selectedIndex].value;
    loadImpulseResponse(name);
});

/** Filter */
document.querySelector("#frequencySlider").addEventListener("mousemove", function(e) {
    let frequencyValue = (this.value);
    document.querySelector("#frequencyOutput").innerHTML = frequencyValue + " Hz";
    filter.frequency.value = frequencyValue;
});

document.querySelector("#detuneSlider").addEventListener("mousemove", function(e) {
    let detuneValue = (this.value);
    document.querySelector("#detuneOutput").innerHTML = detuneValue + " cents";
    filter.detune.value = detuneValue;
});

document.querySelector("#qSlider").addEventListener("mousemove", function(e) {
    let qValue = (this.value);
    document.querySelector("#qOutput").innerHTML = qValue + " ";
    filter.Q.value = qValue;
});

document.querySelector("#gainSliderFilter").addEventListener("mousemove", function(e) {
    let gainValue = (this.value);
    document.querySelector("#gainOutputFilter").innerHTML = gainValue + " dB";
    filter.gain.value = gainValue;
});

selectListFilter.addEventListener("change", function(e) {
    filter.type = selectListFilter.options[selectListFilter.selectedIndex].value;
});

