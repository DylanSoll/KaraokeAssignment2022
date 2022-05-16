window.SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

class SpeechRecognitionHandler{
	constructor(interimResults = false,continuous = true){
    	this.interimResults=interimResults;
      this.continuous=continuous;
      this.recognition = new SpeechRecognition();
      this.recognition.interimResults = true;
      this.recognition.continuous = true;
   }
  	addResultListener(callback = (transcript, confidence)=>{
        console.log(`${(parseFloat(confidence)*100).toFixed(3)}% chance user said: '${transcript}'`)
      }){
      this.recognition.addEventListener('result', (e) => {
         const transcript = Array.from(e.results)
         .map(result => result[0])
         .map(result => result.transcript)
         //.join('')
         const confidence = Array.from(e.results)
               .map(result => result[0])
               .map(result => result.confidence)
         callback(transcript, confidence)
      })
   }
   start(){
      this.recognition.start()
   }
   stop(){
      this.recognition.stop()
   }
}

//const recognition = new SpeechRecognitionHandler()
//recognition.addResultListener()
//recognition.start()

//const AudioContext = window.AudioContext || window.webkitAudioContext;
//var context = new AudioContext({'sampleRate':44100});

function record_audio_segment(stream, audioElementId = 'audio', timeMS = 5000){
   const mediaRecorder = new MediaRecorder(stream);
   document.getElementById('get_audio_for_shazam').addEventListener('click', function(){
      mediaRecorder.start();
         setTimeout(()=>{mediaRecorder.stop()}, timeMS);
         mediaRecorder.addEventListener('dataavailable', (e) =>{
         var blob = new Blob([e.data], { 'type' : 'audio/raw; codecs=opus' });
         document.getElementById(audioElementId).src = window.URL.createObjectURL(blob);
         });
   });
   return
}



if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
   console.log('getUserMedia supported.');
   navigator.mediaDevices.getUserMedia (
      // constraints - only audio needed for this app
      {
         audio: true
      })
      // Success callback
      .then(function(stream) {
         //record_audio_segment(stream)

      })

      // Error callback
      .catch(function(err) {
         console.log('The following getUserMedia error occurred: ' + err);
      }
   );
} else {
   console.log('getUserMedia not supported on your browser!');
}