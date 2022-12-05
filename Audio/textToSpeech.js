/* Websocket */
const webSocket = new WebSocket("ws://localhost:8765");

webSocket.addEventListener("open", () => {
    console.log("We are connected!");

    webSocket.send("connected");
});

webSocket.addEventListener("message", e => {
    console.log(e);
    if (typeof(e.data) !== "string") {
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

        console.log(audioArray); //fully decoded array of the whole wav file (ready to use in WebAudio)
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
    source.connect(context.destination);
    // Play immediately
    source.start(0);
}

document.querySelector("#playStopButton").addEventListener("click", function(e) {
   playByteArray(audioArray);
});

