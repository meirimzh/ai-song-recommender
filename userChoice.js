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

            const songDiv = document.createElement("div");
            songDiv.className="recommendation"

            const p = document.createElement("p");
            p.textContent = rec;
            songDiv.appendChild(p)
            recommendationsDiv.appendChild(songDiv);
        });
            const heartContainer = document.createElement("div");
            heartContainer.className = 'heart-container';
            heartContainer.style.marginTop = '5px';

            const ratingInstruction = document.createElement("p");
            ratingInstruction.textContent = "how would you rate the recommendations?";
            ratingInstruction.style.color = "purple";
            ratingInstruction.style.margin="10px 0";
            ratingInstruction.style.fontWeight ="bold";
            heartContainer.appendChild(ratingInstruction);

            for (let i = 1; i <= 5; i++) {
                const heart = document.createElement("span");
                heart.innerHTML = "❤️";
                heart.style.cursor = "pointer";
                heart.style.fontSize = "20px";
                heart.dataset.value = i;
                
                heart.addEventListener('click', async () => {
                    const rating = parseInt(heart.dataset.value);
                    try {
                        const feedbackResponse = await fetch('http://127.0.0.1:5000/feedback', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            input_song: song,
                            rating: rating
              })
        });
            const feedbackData = await feedbackResponse.json();
            if (feedbackResponse.ok) {
              alert('Thank you for your rating!');
            } else {
              alert(feedbackData.error || 'Failed to send feedback');
            }
          } catch (error) {
            alert('Error sending feedback');
          }
        });

        heartContainer.appendChild(heart);
      }

      recommendationsDiv.appendChild(heartContainer);
    
    } catch (error) {
        alert("Failed to fetch recommendations.");
    }
};
