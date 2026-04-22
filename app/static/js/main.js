async function refreshLiveMatches() {
    const container = document.getElementById("matches-container");
    if (!container) return;

    try {
        const response = await fetch("/api/live");
        const matches = await response.json();

        container.innerHTML = "";

        matches.forEach(match => {
            const card = document.createElement("div");
            card.className = "match-card";
            card.innerHTML = `
                <p><strong>${match.home_team}</strong> ${match.home_score} - ${match.away_score} <strong>${match.away_team}</strong></p>
                <p>Status: ${match.status} | Minute: ${match.minute}</p>
                <a href="/match/${match.id}">View match details</a>
            `;
            container.appendChild(card);
        });
    } catch (error) {
        console.error("Error refreshing live matches:", error);
    }
}

setInterval(refreshLiveMatches, 60000);
