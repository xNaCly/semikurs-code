const prefs = {
	//change this if you got a different port, or an external api-server
	/*
	online: https://xnaclyy.pythonanywhere.com
	localhost: http://127.0.0.1:5000/
	*/
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
		let response = await fetch(prefs.base_url + prefs.endpoints[1]);
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
		b = document.getElementById("ant1");
		b.textContent = `A - ${antworten[0]}`;
		b.style.display = "block";
		b1 = document.getElementById("ant2");
		b1.textContent = `B - ${antworten[1]}`;
		b1.style.display = "block";

		b2 = document.getElementById("ant3");
		b2.textContent = `C - ${antworten[2]}`;
		b2.style.display = "block";

		b3 = document.getElementById("ant4");
		b3.textContent = `D - ${antworten[3]}`;
		b3.style.display = "block";

		document.getElementById("hr-upper").style.display = "block";
		document.getElementById("hr-lower").style.display = "block";

		rightanswer = richtigeAntwort;
	} catch (e) {
		console.error(e);

		document.getElementById("hr-upper").style.display = "none";
		document.getElementById("hr-lower").style.display = "none";

		// if connection failed, display the alert

		document.getElementById("loader-error").style.display = "block";
		document.getElementById("alert").style.display = "block";
	}
}

// if window is loaded, try loading questions and answers
window.addEventListener("load", async () => {
	getQuestion();
});
