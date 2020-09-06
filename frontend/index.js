const production = false;

const prefs = {
	//change this if you got a different port, or an external api-server
	/*
	online: https://xnaclyy.pythonanywhere.com
	localhost: http://127.0.0.1:5000/
	*/
	base_url: production ? "https://xnaclyy.pythonanywhere.com" : "http://127.0.0.1:5000/",
	endpoints: ["/all", "/random", "/endpoints"],
};

var rightanswer = "";

// format answer
function submit(button) {
	let value = button.textContent.split(" - ")[1];
	checkForAnswer(value);
}

function checkForLifes() {
	let lifesbutton = document.getElementById("lifes");
	let lifes = Number(lifesbutton.textContent.split(" ")[1]);
	if (lifes == 4) {
		return lifesbutton.classList.replace("btn-success", "btn-warning");
	} else if (lifes == 2) {
		return lifesbutton.classList.replace("btn-warning", "btn-danger");
	} else if (!lifes) {
		alert("Game over.\nYour game will be saved");
		location.reload();
	}
}

function feedback(rightorwrong) {
	let feedbackalert = document.getElementById("feedbackalert");
	feedbackalert.style.display = "flex";
	if (!rightorwrong) {
		feedbackalert.classList.remove("alert-success");
		feedbackalert.classList.add("alert-danger");
		feedbackalert.innerHTML = "Wrong answer!";
	} else if (rightorwrong) {
		feedbackalert.classList.remove("alert-danger");
		feedbackalert.classList.add("alert-success");
		feedbackalert.innerHTML = "Right answer!";
	}
}

// self-explanatory
function checkForAnswer(answer) {
	let score = document.getElementById("score");
	let lifes = document.getElementById("lifes");
	checkForLifes();
	if (rightanswer == answer) {
		// alert("Right answer");
		//update score
		let latestscore = score.textContent.split(" ");
		score.textContent = `Score: ${Number(latestscore[1]) + 100}`;

		//get new question
		feedback(true);
		return getQuestion();
	} else {
		// alert("Wrong answer");

		//update score
		let latestscore = score.textContent.split(" ");
		score.textContent = `Score: ${Number(latestscore[1]) - 100}`;

		//update lifes
		let latestlife = lifes.textContent.split(" ");
		lifes.textContent = `Lifes: ${Number(latestlife[1]) - 1}`;

		//get new question
		feedback(false);
		return getQuestion();
	}
}

async function getQuestion() {
	try {
		// send request to local api server
		setTimeout(() => {
			document.getElementById("feedbackalert").style.display = "none";
			document.getElementById("feedbackalert").classList.remove("alert-success");
			document.getElementById("feedbackalert").classList.remove("alert-danger");
		}, 3000);

		let response = await fetch(prefs.base_url + prefs.endpoints[1]);
		// display score if connection worked
		document.getElementById("score").style.display = "inline";
		document.getElementById("lifes").style.display = "inline";
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
