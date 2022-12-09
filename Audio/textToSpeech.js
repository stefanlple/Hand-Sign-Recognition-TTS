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
var buf; // Audio buffer

let gain = context.createGain();
let stereoPanner = context.createStereoPanner();
let convolver = context.createConvolver();


//gain.connect(stereoPanner);
stereoPanner.connect(context.destination);


function playByteArray(byteArray) {

    var arrayBuffer = new ArrayBuffer(byteArray.length);
    var bufferView = new Uint8Array(arrayBuffer);
    for (i = 0; i < byteArray.length; i++) {
      bufferView[i] = byteArray[i];
    }

    context.decodeAudioData(arrayBuffer, function(buffer) {
        buf = buffer;
        play();
    });
}

// Play the loaded file
function play() {
    // Create a source node from the buffer
    var source = context.createBufferSource();
    source.buffer = buf;
    // Connect to the final output node (the speakers)
    source.connect(/*context.destination*/source.connect(gain));
    // Play immediately
    source.start(0);
    //source.loop = true;
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

//resets the display of the selected element when (re-)loading
document.querySelector("#selectList").value = "none";

document.querySelector("#playStopButton").addEventListener("click", function(e) {
   playByteArray(audioArray);
});

document.querySelector("#testButton").addEventListener("click", function(e) {
    webSocket.send("test");
 });

 document.querySelector("#gainSlider").addEventListener("input", function(e) {
    let gainValue = (this.value / 10);
    document.querySelector("#gainOutput").innerHTML = gainValue + " dB";
    gain.gain.value = gainValue;
});

document.querySelector("#panningSlider").addEventListener("input", function(e) {
    let panValue = ((this.value - 50) / 50);
    document.querySelector("#panningOutput").innerHTML = panValue + " LR";
    stereoPanner.pan.value = panValue;
});

document.querySelector("#selectList").addEventListener("change", function(e) {
    let name = e.target.options[e.target.selectedIndex].value;
    loadImpulseResponse(name);
});

