const prefs = {
	base_url: "http://127.0.0.1:5000",
	endpoints: ["/all", "/random", "/endpoints"],
};

async function getQuestion() {
	let response = await fetch(prefs.base_url + prefs.endpoints[1]);
	var { antworten, frage } = await response.json();
	document.getElementById("question").textContent = frage;
	document.getElementById("ant1").textContent = antworten[0];
	document.getElementById("ant2").textContent = antworten[1];
	document.getElementById("ant3").textContent = antworten[2];
	document.getElementById("ant4").textContent = antworten[3];
}

window.addEventListener("load", async () => {
	getQuestion();
});
