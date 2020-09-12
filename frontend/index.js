const production = false;

const prefs = {
	//change this if you got a different port, or an external api-server
	/*
	online: https://xnaclyy.pythonanywhere.com
	localhost: http://127.0.0.1:5000/
	*/
	base_url: production ? "https://xnaclyy.pythonanywhere.com" : "http://127.0.0.1:5000",
	endpoints: ["/all", "/random", "/endpoints", "/scoreboard", "/stats", "/check"],
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
	if (lifes > 5) {
		alert("Injection or modification of lifes detected");
		location.reload();
	} else if (lifes == 4) {
		return lifesbutton.classList.replace("btn-success", "btn-warning");
	} else if (lifes == 2) {
		return lifesbutton.classList.replace("btn-warning", "btn-danger");
	} else if (!lifes) {
		var dt = new Date().getTime();
		var player = "xxxxx".replace(/[xy]/g, function (c) {
			var r = (dt + Math.random() * 5) % 5 | 0;
			dt = Math.floor(dt / 5);
			return (c == "x" ? r : (r & 0x3) | 0x8).toString(5);
		});
		var username = prompt(`Game over.\nYour game with a score of: ${score.split(" ")[1]} will be saved as: `);
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
async function checkForAnswer(answer) {
	let question = document.getElementById("question").textContent;
	let rightanswer = await fetch(
		prefs.base_url + prefs.endpoints[5] + `?q=${encodeURIComponent(question)}&a=${encodeURIComponent(answer)}`
	);
	rightanswer = await rightanswer.json();
	let score = document.getElementById("score");
	let lifes = document.getElementById("lifes");
	checkForLifes();
	if (rightanswer.content.success) {
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
		var { answers, question } = await response.json();
		// shuffle 'answers' to be random
		let temporaryValue, randomIndex;

		for (let i = 0; i < answers.length; i++) {
			randomIndex = Math.floor(Math.random() * i);

			temporaryValue = answers[i];
			answers[i] = answers[randomIndex];
			answers[randomIndex] = temporaryValue;
		}

		// replace placeholders with randomised 'antwort' values
		document.getElementById("question").textContent = question;
		b = document.getElementById("ant1");
		b.textContent = `A - ${answers[0]}`;
		b.style.display = "block";
		b1 = document.getElementById("ant2");
		b1.textContent = `B - ${answers[1]}`;
		b1.style.display = "block";

		b2 = document.getElementById("ant3");
		b2.textContent = `C - ${answers[2]}`;
		b2.style.display = "block";

		b3 = document.getElementById("ant4");
		b3.textContent = `D - ${answers[3]}`;
		b3.style.display = "block";

		document.getElementById("hr-upper").style.display = "block";
		document.getElementById("hr-lower").style.display = "block";
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

async function renderStats() {
	let stats = await fetch(
		prefs.base_url +
			prefs.endpoints[4] +
			"?auth=e1150d25-f56a-4688-aeb8-8163a3f4b6399eeacf73-fff8-4bfb-bcbb-5f2a40eef02d"
	);
	stats = await stats.json();
	let average = 0;
	let numbers_below_zero = [];
	for (var number in stats.all_scores_sorted) {
		if (Number(stats.all_scores_sorted[number]) < 0) {
			numbers_below_zero.push(Number(stats.all_scores_sorted[number]));
		}
		average += Number(stats.all_scores_sorted[number]);
	}
	document.getElementById("stats1").innerHTML +=
		" " + Math.round(stats.all_scores_sorted[stats.all_scores_sorted.length / 2]);
	document.getElementById("stats2").innerHTML += " " + Math.round(average / stats.all_scores_sorted.length);
	document.getElementById("stats3").innerHTML += " " + stats.highest_score;
	document.getElementById("stats4").innerHTML += " " + stats.lowest_score;
	document.getElementById("stats5").innerHTML += " " + numbers_below_zero.length;
	document.getElementById("stats6").innerHTML += ` ${stats.all_scores_sorted.length - numbers_below_zero.length}`;
	let myChart = document.getElementById("players").getContext("2d");

	new Chart(myChart, {
		type: "pie", // bar, horizontalBar, pie, line, doughnut, radar, polarArea
		data: {
			labels: ["Registered", "Unregistered"],
			datasets: [
				{
					label: "Players",
					data: [stats.registered_players, stats.players - stats.registered_players],
					//backgroundColor:'green',
					backgroundColor: ["#326a87", "#91afc5"],
					// borderWidth: 1,
					// borderColor: "#777",
					// hoverBorderWidth: 3,
					// hoverBorderColor: "#000",
				},
			],
		},
		options: {
			title: {
				display: true,
				text: "Players:",
				fontSize: 25,
			},
			legend: {
				display: false,
				position: "bottom",
				labels: {
					fontColor: "#000",
				},
			},
			layout: {
				padding: {
					left: 0,
					right: 0,
					bottom: 0,
					top: 0,
				},
			},
			tooltips: {
				enabled: true,
			},
		},
	});

	myChart = document.getElementById("high-low").getContext("2d");

	new Chart(myChart, {
		type: "bar", // bar, horizontalBar, pie, line, doughnut, radar, polarArea
		data: {
			labels: ["Lowestscore", "Highestscore"],
			datasets: [
				{
					label: "Scores",
					data: [stats.lowest_score, stats.highest_score],
					backgroundColor: ["#326a87", "#91afc5"],
				},
			],
		},
		options: {
			title: {
				display: true,
				text: "Scores:",
				fontSize: 25,
			},
			legend: {
				display: false,
				position: "bottom",
				labels: {
					fontColor: "#000",
				},
			},
			layout: {
				padding: {
					left: 0,
					right: 0,
					bottom: 0,
					top: 0,
				},
			},
			tooltips: {
				enabled: true,
			},
		},
	});

	myChart = document.getElementById("all-scores").getContext("2d");

	let dataarray = [];
	for (let x in stats.all_scores_unsorted) {
		// dataarray.push({ x: Number(x), y: stats.all_scores[x] });
		dataarray.push(x);
	}
	// console.log(dataarray);
	new Chart(myChart, {
		type: "line", // bar, horizontalBar, pie, line, doughnut, radar, polarArea
		data: {
			labels: dataarray,
			datasets: [
				{
					label: "Scores unsorted",
					data: stats.all_scores_unsorted,
					borderColor: ["#91afc5"],
					lineTension: 0,
					// pointStyle: "circle",
					radius: 1,
					hitRadius: 2,
					// borderDash: [10, 5],
				},
				{
					label: "Scores sorted",
					data: stats.all_scores_sorted,
					borderColor: ["#326a87"],
					lineTension: 0,
					radius: 1,
					hitRadius: 2,
					// borderDash: [5, 10],
				},
			],
		},
	});
}

// if window is loaded, try loading questions and answers
window.addEventListener("load", async () => {
	console.warn(
		`%cmade by:\n\n__  ___   _    _    ____ _  __   __
\\ \\/ / \\ | |  / \\  / ___| | \\ \\ / /
 \\  /|  \\| | / _ \\| |   | |  \\ V / 
 /  \\| |\\  |/ ___ \\ |___| |___| |  
/_/\\_\\_| \\_/_/   \\_\\____|_____|_|\n\n`,
		"font-family:monospace"
	);
	console.error("visit my github: https://github.com/xNaCly/semikurs-code");
	renderStats();
	modifyscoreboard();
	getQuestion();
	//displayerrormodal:
	$("#myModal").modal({ show: true });
	console.error(
		"POST requests to scoreboard/leaderboard currently disabled, we will keep you posted.\nwhich means: your score will not be saved."
	);
});
