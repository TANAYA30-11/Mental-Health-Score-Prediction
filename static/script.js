const form = document.getElementById("predictionForm");

const submitBtn = document.getElementById("submitBtn");
const loading = document.getElementById("loading");
const result = document.getElementById("result");
const score = document.getElementById("score");
const errorBox = document.getElementById("error");


form.addEventListener("submit", async function (event) {

    event.preventDefault();

    // Hide previous messages
    result.classList.add("hidden");
    errorBox.classList.add("hidden");

    // Collect form data
    const studentData = {
        age: Number(document.getElementById("age").value),

        gender: document.getElementById("gender").value,

        country: document.getElementById("country").value.trim(),

        academic_level:
            document.getElementById("academic_level").value,

        most_used_platform:
            document.getElementById("platform").value,

        purpose_of_use:
            document.getElementById("purpose").value,

        avg_daily_usage_hours:
            Number(document.getElementById("usage").value),

        daily_unlocks:
            Number(document.getElementById("unlocks").value),

        study_hours:
            Number(document.getElementById("study").value),

        physical_activity_hours:
            Number(document.getElementById("activity").value),

        sleep_hours_per_night:
            Number(document.getElementById("sleep").value),

        stress_level:
            document.getElementById("stress").value
    };

    // Show loading
    loading.classList.remove("hidden");
    submitBtn.disabled = true;
    submitBtn.textContent = "Predicting...";

    try {

        // Send request to FastAPI
        const API_URL = "https://mental-health-score-prediction-1-emx5.onrender.com";

        const response = await fetch(`${API_URL}/predict`, {

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(studentData)
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                typeof data.detail === "string"
                    ? data.detail
                    : JSON.stringify(data.detail || data)
            );
        }

        // Display prediction
        score.textContent =
            Number(data.predicted_mental_health_score).toFixed(2);

        result.classList.remove("hidden");

    } catch (error) {

        errorBox.textContent =
            "Error: " + error.message;

        errorBox.classList.remove("hidden");

    } finally {

        loading.classList.add("hidden");
        submitBtn.disabled = false;
        submitBtn.textContent =
            "Predict Mental Health Score";
    }
});