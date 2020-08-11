const prefs = {
	base_url: "http://127.0.0.1:5000",
	endpoints: ["/all", "/random", "/endpoints"],
};

var rightanswer = "";

function submit(button) {
	var value = button.textContent.split(" - ")[1];
	checkForAnswer(value);
}

function checkForAnswer(answer) {
	if (rightanswer == answer) {
		alert("Right answer");
		return getQuestion();
	} else {
		alert("Wrong answer");
		return getQuestion();
	}
}

async function getQuestion() {
	try {
		let response = await fetch(prefs.base_url + prefs.endpoints[1]);
		var { antworten, frage, richtigeAntwort } = await response.json();
		document.getElementById("question").textContent = frage;
		document.getElementById("ant1").textContent = `A - ${antworten[0]}`;
		document.getElementById("ant2").textContent = `B - ${antworten[1]}`;
		document.getElementById("ant3").textContent = `C - ${antworten[2]}`;
		document.getElementById("ant4").textContent = `D - ${antworten[3]}`;
		rightanswer = richtigeAntwort;
	} catch {
		return alert("Request to REST-Api failed.");
	}
}

window.addEventListener("load", async () => {
	getQuestion();
});
