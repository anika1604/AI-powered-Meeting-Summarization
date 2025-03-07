// Enable "Generate Details" button when a file is selected and change its color
document.getElementById("fileInput").addEventListener("change", function () {
    const generateButton = document.getElementById("generateDetails");

    if (this.files.length > 0) {
        generateButton.disabled = false;
        generateButton.style.backgroundColor = "#2DAA9E"; // Change color
        generateButton.style.color = "white"; // Ensure text is visible
    } else {
        generateButton.disabled = true;
        generateButton.style.backgroundColor = ""; // Reset to default
    }
});

// Handle file processing and show loading animation
document.getElementById("generateDetails").addEventListener("click", function () {
    const transcriptionText = document.getElementById("transcriptionText");
    const summaryText = document.getElementById("summaryText");
    const actionsList = document.getElementById("actionsList");
    const loading = document.getElementById("loading");

    // Clear previous content
    transcriptionText.innerHTML = "";
    summaryText.innerHTML = "";
    actionsList.innerHTML = "";

    // Show loading animation
    loading.style.display = "flex";

    // Simulate processing delay
    setTimeout(() => {
        // Mock data
        const longText = "Client: We need to finalize the report by Friday. Manager: Okay, I'll assign tasks. Additionally, we must ensure that all stakeholders are informed, and the design team reviews the layout. Marketing should prepare promotional materials, and the finance team needs to approve the budget.";

        // Append generated content
        transcriptionText.appendChild(generateTextPreview(longText));
        summaryText.appendChild(generateTextPreview("Key Decision: Report due Friday. Action Item: Manager to assign tasks. Ensure all teams are aligned."));
        actionsList.appendChild(generateTextPreview("Manager: Assign report tasks by Friday"));

        // Hide loading animation
        loading.style.display = "none";
    }, 3000); // Simulate 3 seconds of processing
});

// Function to limit text to 200 characters with "Read More" button
function generateTextPreview(fullText) {
    const preview = fullText.length > 200 ? fullText.substring(0, 200) + "..." : fullText;

    // Create a container for the text and button
    const container = document.createElement("div");
    container.classList.add("text-container");

    // Add the preview text
    const previewSpan = document.createElement("span");
    previewSpan.classList.add("text-preview");
    previewSpan.textContent = preview;
    container.appendChild(previewSpan);

    // Add the full text (hidden by default)
    const fullTextSpan = document.createElement("span");
    fullTextSpan.classList.add("full-text");
    fullTextSpan.textContent = fullText;
    fullTextSpan.style.display = "none"; // Hide full text initially
    container.appendChild(fullTextSpan);

    // Add the "Read More" button if needed
    if (fullText.length > 200) {
        const readMoreButton = document.createElement("button");
        readMoreButton.classList.add("read-more", "small-btn");
        readMoreButton.textContent = "Read More";
        container.appendChild(readMoreButton);
    }

    return container; // Return the DOM element
}

// Event delegation for Read More/Read Less functionality
document.addEventListener("click", function (event) {
    if (event.target.classList.contains("read-more")) {
        // Handle "Read More" click
        const container = event.target.closest('.text-container');
        const previewSpan = container.querySelector('.text-preview');
        const fullTextSpan = container.querySelector('.full-text');
        const button = container.querySelector('.read-more');

        // Toggle visibility
        previewSpan.style.display = "none";
        fullTextSpan.style.display = "inline";
        button.textContent = "Read Less";
        button.classList.replace("read-more", "read-less"); // Change class for styling
    } else if (event.target.classList.contains("read-less")) {
        // Handle "Read Less" click
        const container = event.target.closest('.text-container');
        const previewSpan = container.querySelector('.text-preview');
        const fullTextSpan = container.querySelector('.full-text');
        const button = container.querySelector('.read-less');

        // Toggle visibility
        previewSpan.style.display = "inline";
        fullTextSpan.style.display = "none";
        button.textContent = "Read More";
        button.classList.replace("read-less", "read-more"); // Change class for styling
    }
});

// Live Recording Feature
let mediaRecorder;
let chunks = [];

document.getElementById("startRecording").addEventListener("click", async () => {
    let stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);

    mediaRecorder.ondataavailable = (event) => chunks.push(event.data);
    mediaRecorder.onstop = () => {
        let audioBlob = new Blob(chunks, { type: "audio/wav" });
        console.log("Recording saved!", audioBlob);
        document.getElementById("recordingStatus").innerText = "Recording saved!";
    };

    mediaRecorder.start();
    document.getElementById("recordingStatus").innerText = "Recording...";
    document.getElementById("startRecording").disabled = true;
    document.getElementById("stopRecording").disabled = false;
});

document.getElementById("stopRecording").addEventListener("click", () => {
    mediaRecorder.stop();
    document.getElementById("startRecording").disabled = false;
    document.getElementById("stopRecording").disabled = true;
});

// Dark Mode Toggle
const darkModeToggle = document.getElementById("darkModeToggle");
const body = document.body;

darkModeToggle.addEventListener("click", () => {
    body.classList.toggle("dark-mode");
    darkModeToggle.innerText = body.classList.contains("dark-mode") ? "☀️ Light Mode" : "🌙 Dark Mode";
});