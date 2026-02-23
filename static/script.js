const chatForm = document.getElementById("chatForm");
const userInput = document.getElementById("userInput");
const chatLog = document.getElementById("chatLog");
const sendBtn = document.getElementById("sendBtn");
const statusLine = document.getElementById("status");
const micBtn = document.getElementById("micBtn");
const faqItems = document.querySelectorAll(".faq-item");
const admissionsOptions = document.querySelectorAll(".admissions-option");
const programOptions = document.querySelectorAll(".program-option");
const chatSection = document.getElementById("chatSection");
const navbar = document.querySelector(".navbar");
const themeToggle = document.getElementById("themeToggle");
const themeIcon = document.querySelector(".theme-icon");
const askMeLink = document.getElementById("askMeLink");

// Set initial message time
const initialTime = document.getElementById("initialTime");
if (initialTime) {
	const now = new Date();
	initialTime.textContent = now.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
}

// Ask Me Link - Scroll to chat and focus input
if (askMeLink) {
	askMeLink.addEventListener("click", (e) => {
		e.preventDefault();
		chatSection.scrollIntoView({ behavior: "smooth" });
		setTimeout(() => {
			userInput.focus();
		}, 600);
	});
}

// Dark mode toggle
function setTheme(isDark) {
	if (isDark) {
		document.body.classList.add("dark-mode");
		themeIcon.textContent = "☀️";
		localStorage.setItem("theme", "dark");
	} else {
		document.body.classList.remove("dark-mode");
		themeIcon.textContent = "🌙";
		localStorage.setItem("theme", "light");
	}
}

// Check for saved theme preference or default to light mode
const savedTheme = localStorage.getItem("theme");
if (savedTheme === "dark") {
	setTheme(true);
}

// Toggle theme on button click
if (themeToggle) {
	themeToggle.addEventListener("click", () => {
		const isDark = document.body.classList.contains("dark-mode");
		setTheme(!isDark);
	});
}

async function sendMessage(text) {
	const trimmed = text.trim();
	if (!trimmed) return;
	addMessage(trimmed, "user");
	userInput.value = "";
	sendBtn.disabled = true;
	statusLine.textContent = "Thinking...";

	try {
		const response = await fetch("/chat", {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({ message: trimmed })
		});
		const data = await response.json();
		if (response.ok) {
			addMessage(data.reply, "bot");
		} else {
			addMessage(data.error || "Something went wrong.", "bot");
		}
	} catch (err) {
		addMessage("Network error. Please try again.", "bot");
	} finally {
		sendBtn.disabled = false;
		statusLine.textContent = "";
	}
}

async function fetchProgramDetails(programName) {
	addMessage(`Fetching details for ${programName}...`, "user");
	sendBtn.disabled = true;
	statusLine.textContent = "Loading program details...";

	try {
		const response = await fetch(`/program/${encodeURIComponent(programName)}`);
		const data = await response.json();
		if (response.ok) {
			addMessage(data.details, "bot");
		} else {
			addMessage(data.error || "Program details not found.", "bot");
		}
	} catch (err) {
		addMessage("Network error. Please try again.", "bot");
	} finally {
		sendBtn.disabled = false;
		statusLine.textContent = "";
	}
}

function submitQuestion(question) {
	userInput.value = question;
	sendMessage(question);
}

function scrollToChat() {
	if (!chatSection) return;
	chatSection.scrollIntoView({ behavior: "smooth", block: "start" });
}

function closeNavbar() {
	if (!navbar) return;
	if (document.activeElement && typeof document.activeElement.blur === "function") {
		document.activeElement.blur();
	}
	navbar.classList.add("nav-closed");
}

// Remove nav-closed class when hovering over navbar again
if (navbar) {
	navbar.addEventListener("mouseenter", () => {
		navbar.classList.remove("nav-closed");
	});
}

faqItems.forEach((item) => {
	item.addEventListener("click", () => {
		const question = item.querySelector("strong").textContent;
		submitQuestion(question);
	});
});

admissionsOptions.forEach((item) => {
	item.addEventListener("click", (event) => {
		event.preventDefault();
		const question = item.dataset.question || item.textContent.trim();
		submitQuestion(question);
		closeNavbar();
		scrollToChat();
	});
});

programOptions.forEach((item) => {
	item.addEventListener("click", (event) => {
		event.preventDefault();
		const programName = item.dataset.program || item.textContent.trim();
		fetchProgramDetails(programName);
		closeNavbar();
		scrollToChat();
	});
});

userInput.addEventListener("keydown", (event) => {
	if (event.key === "Enter" && !event.shiftKey) {
		event.preventDefault();
		chatForm.dispatchEvent(new Event("submit"));
	}
});

function addMessage(text, role) {
	const now = new Date();
	const timeString = now.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
	
	const bubble = document.createElement("div");
	bubble.className = `msg ${role}`;
	
	const messageText = document.createElement("div");
	messageText.className = "msg-text";
	
	// Format text: convert ** to bold and handle newlines
	let formattedText = text
		.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')  // Convert **text** to <strong>text</strong>
		.replace(/\n/g, '<br>');                           // Convert newlines to <br>
	
	messageText.innerHTML = formattedText;
	
	const messageTime = document.createElement("div");
	messageTime.className = "msg-time";
	messageTime.textContent = timeString;
	
	bubble.appendChild(messageText);
	bubble.appendChild(messageTime);
	chatLog.appendChild(bubble);
	chatLog.scrollTop = chatLog.scrollHeight;
}

chatForm.addEventListener("submit", async (event) => {
	event.preventDefault();
	await sendMessage(userInput.value);
});

// --- Voice Input (Mic Button) ---
if (window.SpeechRecognition || window.webkitSpeechRecognition) {
	const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
	const recognition = new SpeechRecognition();
	recognition.lang = "en-US";
	recognition.interimResults = false;
	recognition.maxAlternatives = 1;

	let listening = false;

	micBtn.addEventListener("click", () => {
		if (!listening) {
			recognition.start();
		} else {
			recognition.stop();
		}
	});

	recognition.addEventListener("start", () => {
		listening = true;
		micBtn.classList.add("active");
		statusLine.textContent = "Listening...";
	});

	recognition.addEventListener("end", () => {
		listening = false;
		micBtn.classList.remove("active");
		statusLine.textContent = "";
	});

	recognition.addEventListener("result", (event) => {
		const transcript = event.results[0][0].transcript;
		userInput.value = transcript;
		sendMessage(transcript);
	});
} else {
	micBtn.disabled = true;
	micBtn.title = "Speech recognition not supported in this browser.";
}
