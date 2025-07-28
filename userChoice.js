backButton.onclick=function() {
    //window.location is for going to a different page, you can also do window.history.back()
    window.location.href="home.html";
}

document.getElementById("submit").onclick = async function() {
    const song = document.getElementById("Song").value;
    const artist = document.getElementById("Artist").value;

    try {
        const response = await fetch("http://127.0.0.1:5000/similar", { //sending request to flask
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ song, artist }), //in this format
        });

        if (!response.ok) {
            const err = await response.json();
            console.error("Server error:", err);
            alert("Error: " + err.error);
            return;
        }

        const data = await response.json();
        console.log("Received:", data.recommendations);

        const recommendationsDiv = document.getElementById("recommendations"); //clearing previous recommendations
        recommendationsDiv.innerHTML = "";

        data.recommendations.forEach((rec) => {
            const p = document.createElement("p");
            p.textContent = rec;
            recommendationsDiv.appendChild(p);
        });
     
    } catch (error) {
        alert("Failed to fetch recommendations.");
    }
};
