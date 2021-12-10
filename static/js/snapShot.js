
  window.onload = async function () {
  if (
  !"mediaDevices" in navigator ||
  !"getUserMedia" in navigator.mediaDevices
  ) {
  document.write('Not support API camera')
  return;
  }

  const video = document.querySelector("#video");
  const canvas = document.querySelector("#canvas");
  const screenshotsContainer = document.querySelector("#screenshotsContainer");
  let videoStream = null
  let useFrontCamera = true; //camera trước
  const constraints = {
  video: {
      width: {
      min: 1280,
      ideal: 1920,
      max: 2560,
      },
      height: {
      min: 720,
      ideal: 1080,
      max: 1440,
      }
  },
  };

  // play
  btnPlay.addEventListener("click", function () {
  video.play();
  btnPlay.classList.add("is-hidden");
  btnPause.classList.remove("is-hidden");
  });

  // pause
  btnPause.addEventListener("click", function () {
  video.pause();
  btnPause.classList.add("is-hidden");
  btnPlay.classList.remove("is-hidden");
  });


  btnChangeCamera.addEventListener("click", function () {
  useFrontCamera = !useFrontCamera;
  init();
  });


  function stopVideoStream() {
  if (videoStream) {
      videoStream.getTracks().forEach((track) => {
      track.stop();
      });
  }
  }

  btnScreenshot.addEventListener("click", function () {
  let img = document.getElementById('screenshot');
  if (!img) {
      img = document.createElement("img");
      img.id = 'screenshot';
      img.style.width = '100%';
  }
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  canvas.getContext("2d").drawImage(video, 0, 0);
  img.src = canvas.toDataURL("image/png");
  screenshotsContainer.prepend(img);
  });

  async function init() {
  stopVideoStream();
  constraints.video.facingMode = useFrontCamera ? "user" : "environment";
  try {
      videoStream = await navigator.mediaDevices.getUserMedia(constraints);
      video.srcObject = videoStream;
  } catch (error) {
      console.log(error)
  }
  }
  init();
  }

  // const canvas = document.getElementById("canvas");
  // canvas.toBlob(function(blob) {
  //   const formData = new FormData();
  //   formData.append('screenshots', blob, 'filename.png');

  //   //post via axios or other transport method
  //   axios.post('./upload', formData);
  // });

