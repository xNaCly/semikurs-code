const prefs = {
	base_url: "http://127.0.0.1:5000/",
	endpoints: ["all", "random", "endpoints"],
};

async function getQuestion() {
	let response = await fetch(prefs.base_url + prefs.endpoints[1] + "/");
	response = await response.json();
	document.getElementById("question").textContent = response.frage;
	document.getElementById("ant1").textContent = response.antworten[0];
	document.getElementById("ant2").textContent = response.antworten[1];
	document.getElementById("ant3").textContent = response.antworten[2];
	document.getElementById("ant4").textContent = response.antworten[3];
}

window.addEventListener("load", async () => {
	getQuestion();
});
