document.addEventListener('DOMContentLoaded', function() {
    const loader = document.getElementById('loader');
    const cameraModal = document.getElementById('cameraModal');
    const timerElement = document.getElementById('timer');
    const thankYouElement = document.getElementById('thankYou');
    const video = document.getElementById('video');
    const timeElement = document.getElementById('time');
    const denyButton = document.getElementById('denyButton');
    const allowButton = document.getElementById('allowButton');

    let timerInterval;

    // Show the loader for 10 seconds
    setTimeout(function() {
        loader.style.display = 'none';
        cameraModal.style.display = 'block';
    }, 10000);

    denyButton.addEventListener('click', function() {
        alert("You have denied camera access. The app will not function properly.");
    });

    allowButton.addEventListener('click', function() {
        cameraModal.style.display = 'none';
        startCamera();
        timerElement.style.display = 'block';
        startTimer();
    });

    function startCamera() {
        navigator.mediaDevices.getUserMedia({ video: true })
            .then(function(stream) {
                video.srcObject = stream;
                video.style.display = 'block';
                setCameraStatus("ON");
            })
            .catch(function(err) {
                console.error("Error accessing camera: " + err);
                setCameraStatus("OFF");
            });
    }

    function stopCamera() {
        const stream = video.srcObject;
        const tracks = stream.getTracks();

        tracks.forEach(function(track) {
            track.stop();
        });

        video.srcObject = null;
        setCameraStatus("OFF");
    }

    function setCameraStatus(status) {
        fetch('/set_camera_status', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ status: status })
        }).then(response => response.json())
          .then(data => console.log(data));
    }

    function startTimer() {
        let time = 3 * 60 * 60; // 3 hours in seconds
        timerInterval = setInterval(function() {
            const hours = Math.floor(time / 3600);
            const minutes = Math.floor((time % 3600) / 60);
            const seconds = time % 60;

            timeElement.textContent = `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;

            if (time === 0) {
                clearInterval(timerInterval);
                stopCamera();
                timerElement.style.display = 'none';
                thankYouElement.style.display = 'block';
            } else {
                time--;
            }
        }, 1000);
    }
});
