// Get elements from the DOM
const tipsContainer = document.getElementById('tips-container');
const nextButton = document.getElementById('next-button');
const prevButton = document.getElementById('prev-button');
const tips = [
  'Take deep breaths',
  'Practice mindfulness meditation',
  'Engage in physical activity',
  'Get enough sleep',
  'Maintain a healthy diet',
  'Spend time with loved ones',
  'Limit screen time',
  'Listen to calming music',
  'Practice gratitude',
  'Take breaks and relax'
];
let currentTipIndex = 0;

// Function to display the current tip
function displayCurrentTip() {
  tipsContainer.textContent = tips[currentTipIndex];
}

// Function to go to the next tip
function nextTip() {
  currentTipIndex++;
  if (currentTipIndex >= tips.length) {
    currentTipIndex = 0;
  }
  displayCurrentTip();
}

// Function to go to the previous tip
function prevTip() {
  currentTipIndex--;
  if (currentTipIndex < 0) {
    currentTipIndex = tips.length - 1;
  }
  displayCurrentTip();
}

// Event listeners for next and previous buttons
nextButton.addEventListener('click', nextTip);
prevButton.addEventListener('click', prevTip);

// Display the initial tip
displayCurrentTip();
