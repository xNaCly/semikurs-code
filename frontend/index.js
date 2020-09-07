const production = true;

const prefs = {
	//change this if you got a different port, or an external api-server
	/*
	online: https://xnaclyy.pythonanywhere.com
	localhost: http://127.0.0.1:5000/
	*/
	base_url: production ? "https://xnaclyy.pythonanywhere.com" : "http://127.0.0.1:5000",
	endpoints: ["/all", "/random", "/endpoints", "/scoreboard"],
};

var rightanswer = "";

// format answer
function submit(button) {
	let value = button.textContent.split(" - ")[1];
	checkForAnswer(value);
}

function checkForLifes() {
	let score = document.getElementById("score").textContent;
	let lifesbutton = document.getElementById("lifes");
	let lifes = Number(lifesbutton.textContent.split(" ")[1]);
	if (lifes == 4) {
		return lifesbutton.classList.replace("btn-success", "btn-warning");
	} else if (lifes == 2) {
		return lifesbutton.classList.replace("btn-warning", "btn-danger");
	} else if (!lifes) {
		if (production) {
			var dt = new Date().getTime();
			var player = "xxxxx".replace(/[xy]/g, function (c) {
				var r = (dt + Math.random() * 5) % 5 | 0;
				dt = Math.floor(dt / 5);
				return (c == "x" ? r : (r & 0x3) | 0x8).toString(5);
			});
			var username = prompt(
				`Game over.\nYour game with a score of: ${score.split(" ")[1]} will be saved as: `
			);
			if (!username) {
				username = `Player ${player}`;
			}
			fetch(
				prefs.base_url +
					prefs.endpoints[3] +
					`?name=${username}&score=${
						score.split(" ")[1]
					}&auth=e1150d25-f56a-4688-aeb8-8163a3f4b6399eeacf73-fff8-4bfb-bcbb-5f2a40eef02d`,
				{
					method: "POST",
				}
			);
		} else {
			alert("Game over :(");
		}

		location.reload();
	}
}

async function modifyscoreboard() {
	let response = await fetch(
		prefs.base_url +
			prefs.endpoints[3] +
			"?auth=e1150d25-f56a-4688-aeb8-8163a3f4b6399eeacf73-fff8-4bfb-bcbb-5f2a40eef02d&top=true"
	);
	response = await response.json();
	document.getElementById("score1").innerHTML += ` ${response.content["0"]
		.split(",")
		.splice(0, 2)
		.toString()
		.replace(",", " - ")}`;
	document.getElementById("score2").innerHTML += ` ${response.content["1"]
		.split(",")
		.splice(0, 2)
		.toString()
		.replace(",", " - ")}`;
	document.getElementById("score3").innerHTML += ` ${response.content["2"]
		.split(",")
		.splice(0, 2)
		.toString()
		.replace(",", " - ")}`;
	document.getElementById("score4").innerHTML += ` ${response.content["3"]
		.split(",")
		.splice(0, 2)
		.toString()
		.replace(",", " - ")}`;
	document.getElementById("score5").innerHTML += ` ${response.content["4"]
		.split(",")
		.splice(0, 2)
		.toString()
		.replace(",", " - ")}`;
	document.getElementById("score6").innerHTML += ` ${response.content["5"]
		.split(",")
		.splice(0, 2)
		.toString()
		.replace(",", " - ")}`;
	document.getElementById("score7").innerHTML += ` ${response.content["6"]
		.split(",")
		.splice(0, 2)
		.toString()
		.replace(",", " - ")}`;
	document.getElementById("score8").innerHTML += ` ${response.content["7"]
		.split(",")
		.splice(0, 2)
		.toString()
		.replace(",", " - ")}`;
	document.getElementById("score9").innerHTML += ` ${response.content["8"]
		.split(",")
		.splice(0, 2)
		.toString()
		.replace(",", " - ")}`;
	document.getElementById("score10").innerHTML += ` ${response.content["9"]
		.split(",")
		.splice(0, 2)
		.toString()
		.replace(",", " - ")}`;
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
			feedbackbutton = document.getElementById("feedbackalert");
			feedbackbutton.classList.remove("alert-success");
			feedbackbutton.classList.remove("alert-danger");
			feedbackbutton.innerHTML = "";
		}, 3000);

		let response = await fetch(
			prefs.base_url +
				prefs.endpoints[1] +
				"?auth=e1150d25-f56a-4688-aeb8-8163a3f4b6399eeacf73-fff8-4bfb-bcbb-5f2a40eef02d"
		);
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

		document.getElementsByClassName("liste")[0].style.display = "none";

		document.getElementById("hr-upper").style.display = "none";
		document.getElementById("hr-lower").style.display = "none";

		// if connection failed, display the alert

		document.getElementById("loader-error").style.display = "block";
		document.getElementById("alert").style.display = "block";
	}
}

// if window is loaded, try loading questions and answers
window.addEventListener("load", async () => {
	modifyscoreboard();
	getQuestion();
});
