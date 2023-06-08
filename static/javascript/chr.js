let timerInterval;
let minutes = 25;
let seconds = 0;
let breakDuration = 5; // Default break duration
let repetitions = 1; // Default number of repetitions
let currentRepetition = 0;

function startTimer() {
  breakDuration = parseInt(document.getElementById("break-duration").value, 10);
  repetitions = parseInt(document.getElementById("repetitions").value, 10);

  timerInterval = setInterval(updateTimer, 1000);
}

function pauseTimer() {
  clearInterval(timerInterval);
}

function stopTimer() {
  clearInterval(timerInterval);
  minutes = 25;
  seconds = 0;
  currentRepetition = 0;
  updateTimer();
}

function updateTimer() {
  const minutesDisplay = document.getElementById("minutes");
  const secondsDisplay = document.getElementById("seconds");

  if (seconds === 0) {
    if (minutes === 0) {
      if (currentRepetition < repetitions) {
        // Break time
        minutes = breakDuration;
        currentRepetition++;
      } else {
        // Timer and repetitions finished
        clearInterval(timerInterval);
        // Perform additional actions or show notifications here
        return;
      }
    } else {
      minutes--;
      seconds = 59;
    }
  } else {
    seconds--;
  }

  minutesDisplay.textContent = padTime(minutes);
  secondsDisplay.textContent = padTime(seconds);

  
}

function padTime(time) {
  return time.toString().padStart(2, "0");
}
