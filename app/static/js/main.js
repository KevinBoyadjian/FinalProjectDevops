async function refreshLiveMatches() {
    const container = document.getElementById("matches-container");
    if (!container) return;

    try {
        const response = await fetch("/api/live");
        const matches = await response.json();

        if (!matches.length) {
            container.innerHTML = `
                <div class="empty-state">
                    <div class="empty-icon">⚠</div>
                    <h3>No live matches right now</h3>
                    <p>Try refreshing or check again later.</p>
                </div>
            `;
            return;
        }

        container.innerHTML = "";

        matches.forEach(match => {
            const card = document.createElement("article");
            card.className = "match-card";
            card.innerHTML = `
                <div class="match-status">
                    <span class="live-badge">${match.status}</span>
                    <span class="minute">${match.minute}'</span>
                </div>

                <div class="teams">
                    <div class="team-row">
                        <span class="team-name">${match.home_team}</span>
                        <span class="team-score">${match.home_score ?? 0}</span>
                    </div>
                    <div class="team-row">
                        <span class="team-name">${match.away_team}</span>
                        <span class="team-score">${match.away_score ?? 0}</span>
                    </div>
                </div>

                <div class="card-footer">
                    <a class="details-link" href="/match/${match.id}">Match details</a>
                </div>
            `;
            container.appendChild(card);
        });
    } catch (error) {
        container.innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">✖</div>
                <h3>Failed to load matches</h3>
                <p>Please try again in a moment.</p>
            </div>
        `;
        console.error("Error refreshing live matches:", error);
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const refreshButton = document.getElementById("refresh-btn");

    if (refreshButton) {
        refreshButton.addEventListener("click", refreshLiveMatches);
    }

    setInterval(refreshLiveMatches, 60000);
});
