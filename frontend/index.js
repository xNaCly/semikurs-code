const prefs = {
	//change this if you got a different port, or an external api-server
	base_url: "https://xnaclyy.pythonanywhere.com",
	endpoints: ["/all", "/random", "/endpoints"],
};

var rightanswer = "";

// format answer
function submit(button) {
	var value = button.textContent.split(" - ")[1];
	checkForAnswer(value);
}

// self-explanatory
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
		// send request to local api server
		let response = await fetch(prefs.base_url + prefs.endpoints[1], {
			method: "GET",
			headers: { "Content-Type": "application/json", Origin: "http://localhost:3000" },
		});
		var { antworten, frage, richtigeAntwort } = await response.json();
		// shuffle 'antworten' to be random
		let temporaryValue, randomIndex;

		for (let i = 0; i < antworten.length; i++) {
			randomIndex = Math.floor(Math.random() * i);

			temporaryValue = antworten[i];
			antworten[i] = antworten[randomIndex];
			antworten[randomIndex] = temporaryValue;
		}

		// replace placeholders with randomised 'antwort' values
		document.getElementById("question").textContent = frage;
		document.getElementById("ant1").textContent = `A - ${antworten[0]}`;
		document.getElementById("ant2").textContent = `B - ${antworten[1]}`;
		document.getElementById("ant3").textContent = `C - ${antworten[2]}`;
		document.getElementById("ant4").textContent = `D - ${antworten[3]}`;
		rightanswer = richtigeAntwort;
	} catch {
		// if no connection is found, display the alert
		return (document.getElementById("alert").style.display = "block");
	}
}

// if window is loaded, try loading questions and answers
window.addEventListener("load", async () => {
	getQuestion();
});
