// File Upload Handling
document.getElementById("fileInput").addEventListener("change", function () {
    let transcriptionText = document.getElementById("transcriptionText");
    let summaryText = document.getElementById("summaryText");

    transcriptionText.innerText = "Processing audio...";
    summaryText.innerText = "Generating summary...";

    setTimeout(() => {
        transcriptionText.innerText = "Client: We need to finalize the report by Friday. Manager: Okay, I'll assign tasks.";
        summaryText.innerText = "Key Decision: Report due Friday. Action Item: Manager to assign tasks.";

        // Update Action Items
        let actionsList = document.getElementById("actionsList");
        actionsList.innerHTML = "<li>Manager: Assign report tasks by Friday</li>";
    }, 3000);
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
    if (body.classList.contains("dark-mode")) {
        darkModeToggle.innerText = "☀️ Light Mode";
    } else {
        darkModeToggle.innerText = "🌙 Dark Mode";
    }
});