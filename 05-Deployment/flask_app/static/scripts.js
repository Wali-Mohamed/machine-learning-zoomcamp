function submitPrediction() {
    const job = document.getElementById("job").value;
    const duration = document.getElementById("duration").value;
    const poutcome = document.getElementById("poutcome").value;

    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `job=${job}&duration=${duration}&poutcome=${poutcome}`,
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('prediction-message').textContent = data.message;
        document.getElementById('result').style.display = 'block';
        document.getElementById('feedback-section').style.display = 'block';
    })
    .catch(error => console.error('Error:', error));
}

function submitFeedback() {
    const thumbsUp = document.querySelector('input[name="thumbs_up"]:checked').value;
    const comment = document.getElementById('comment').value;

    fetch('/feedback', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ thumbs_up: thumbsUp === 'true', comment }),
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        document.getElementById('feedback-section').style.display = 'none';
    })

    .catch(error => console.error('Error:', error));
}
