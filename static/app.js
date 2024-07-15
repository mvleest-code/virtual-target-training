const timerElement = document.getElementById('timer');
const targetContainer = document.getElementById('targetContainer');
let currentTarget = null;
let countdown = 10;

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
    currentTarget.style.top = `${Math.random() * 90}vh`;
    currentTarget.style.left = `${Math.random() * 90}vw`;
    currentTarget.style.backgroundImage = 'url(/static/target.png)';
    currentTarget.style.backgroundSize = 'cover';
    currentTarget.style.width = '100px';
    currentTarget.style.height = '100px';

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
    }, 5000);  // Target blijft nu 5 seconden staan
}

setInterval(updateTimer, 1000);  // Update de timer elke seconde