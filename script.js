const video = document.getElementById('videoElement');
const startButton = document.getElementById('startButton');
const stopButton = document.getElementById('stopButton');
let stream;

// Start webcam
startButton.addEventListener('click', () => {
  startWebcam();
});

// Stop webcam
stopButton.addEventListener('click', () => {
  stopWebcam();
});

function startWebcam() {
  navigator.mediaDevices.getUserMedia({ video: true })
    .then(mediaStream => {
      stream = mediaStream;
      video.srcObject = stream;
    })
    .catch(error => {
      console.error('Unable to access the webcam stream:', error);
    });
}

function stopWebcam() {
  if (stream) {
    const tracks = stream.getTracks();
    tracks.forEach(track => {
      track.stop();
    });
    video.srcObject = null;
  }
}
