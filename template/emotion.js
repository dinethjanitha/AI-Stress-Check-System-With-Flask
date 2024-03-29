document.addEventListener('DOMContentLoaded', () => {
    let videoElement = document.getElementById('videoElement');
    let startButton = document.getElementById('startButton');
    let stopButton = document.getElementById('stopButton');

    let mediaRecorder;
    let chunks = [];
    let startTime;

    startButton.addEventListener('click', () => {
        startButton.disabled = true;
        stopButton.disabled = false;

        navigator.mediaDevices.getUserMedia({ video: true })
        .then(function(stream) {
            videoElement.srcObject = stream;
            mediaRecorder = new MediaRecorder(stream);
            startTime = new Date().getTime();

            mediaRecorder.ondataavailable = function(event) {
                chunks.push(event.data);
            };

            mediaRecorder.onstop = function() {
                let endTime = new Date().getTime();
                let recordingTime = Math.round((endTime - startTime) / 1000); // in seconds

                let blob = new Blob(chunks, { type: 'video/webm' });
                chunks = [];

                let formData = new FormData();
                formData.append('video', blob, 'recorded.webm');

                let request = new XMLHttpRequest();
                request.open('POST', 'save_video.php', true);
                request.onreadystatechange = function() {
                    if (request.readyState === 4 && request.status === 200) {
                        console.log('Video uploaded successfully');
                    }
                };
                request.send(formData);
            };

            mediaRecorder.start();
            setTimeout(() => {
                mediaRecorder.stop();
                startButton.disabled = false;
                stopButton.disabled = true;
            }, 60000); // 1 minute
        })
        .catch(function(error) {
            console.log("Error accessing webcam: " + error.message);
        });
    });

    stopButton.addEventListener('click', () => {
        mediaRecorder.stop();
        startButton.disabled = false;
        stopButton.disabled = true;
    });
});
