// File Upload Handling
document.getElementById("fileInput").addEventListener("change", function () {
    let transcriptionText = document.getElementById("transcriptionText");
    let summaryText = document.getElementById("summaryText");
    let actionsList = document.getElementById("actionsList");

    transcriptionText.innerText = "Processing audio...";
    summaryText.innerText = "Generating summary...";
    actionsList.innerText = "Generating actions..."

    // setTimeout(() => {
    //     transcriptionText.innerText = "Client: We need to finalize the report by Friday. Manager: Okay, I'll assign tasks.";
    //     summaryText.innerText = "Key Decision: Report due Friday. Action Item: Manager to assign tasks.";

    //     // Update Action Items
    //     let actionsList = document.getElementById("actionsList");
    //     actionsList.innerHTML = "<li>Manager: Assign report tasks by Friday</li>";
    // }, 3000);
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

document.getElementById("submit").addEventListener("click", function(event){
    event.preventDefault();  // Prevent default form submission

    var fileInput = document.getElementById("fileInput");
    var formData = new FormData();
    formData.append("file", fileInput.files[0]);

    // Send the file to Flask server
    fetch("/upload", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);  // Handle the response from Flask
        // alert("File uploaded successfully!");
        window.location.reload();
    })
    .catch(error => {
        console.error("Error:", error);
    });
});

