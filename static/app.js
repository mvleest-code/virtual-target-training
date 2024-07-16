const body = document.querySelector('body');
const timerElement = document.getElementById('timer');
const targetContainer = document.getElementById('targetContainer');
let currentTarget = null;
let countdown = 10;
let targetSize = 100; // Size of the target in pixels

function updateTimer() {
    timerElement.textContent = `Next target in: ${countdown}s`;
    if (countdown === 0) {
        createTarget();
        countdown = 10;  // Reset countdown after showing the target
    } else {
        countdown--;
    }
}

function createTarget() {
    if (currentTarget) {
        currentTarget.remove();
    }

    currentTarget = document.createElement('div');
    currentTarget.classList.add('target');
    currentTarget.style.backgroundImage = 'url(/static/target.png)';
    currentTarget.style.backgroundSize = 'cover';
    currentTarget.style.width = `${targetSize}px`;
    currentTarget.style.height = `${targetSize}px`;

    // Ensure the target is fully visible within the viewport
    const maxWidth = window.innerWidth - targetSize;
    const maxHeight = window.innerHeight - targetSize;
    const top = Math.random() * maxHeight;
    const left = Math.random() * maxWidth;

    currentTarget.style.top = `${top}px`;
    currentTarget.style.left = `${left}px`;

    currentTarget.addEventListener('click', () => {
        currentTarget.remove();
        currentTarget = null;
    });

    targetContainer.appendChild(currentTarget);

    setTimeout(() => {
        if (currentTarget) {
            currentTarget.remove();
            currentTarget = null;
        }
    }, 5000);  // Target remains for 5 seconds
}

function fetchStats() {
    fetch('/get_stats')
        .then(response => response.json())
        .then(data => {
            statsElement.innerHTML = `
                <p>Fastest reaction time: ${data.min_time.toFixed(2)}s</p>
                <p>Slowest reaction time: ${data.max_time.toFixed(2)}s</p>
                <p>Average reaction time: ${data.average_time.toFixed(2)}s</p>
                <p>Total shots: ${data.shot_count}</p>
            `;
        });
}

setInterval(updateTimer, 1000);  // Update the timer every second
setInterval(fetchStats, 1000);  // Fetch stats every second
