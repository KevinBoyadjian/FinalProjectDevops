async function refreshLiveMatches() {
    const container = document.getElementById("matches-container");
    if (!container) return;

    const league = container.dataset.league || "la-liga";

    try {
        const response = await fetch(`/api/live?league=${league}`);

        if (response.status === 429) {
            container.innerHTML = `
                <div class="empty-state">
                    <div class="empty-icon">⏳</div>
                    <h3>API limit reached</h3>
                    <p>Too many requests. Please wait a little before refreshing again.</p>
                </div>
            `;
            return;
        }

        const data = await response.json();
        const matches = data.matches || [];

        if (!matches.length) {
            container.innerHTML = `
                <div class="empty-state">
                    <div class="empty-icon">⚠</div>
                    <h3>No matches found right now</h3>
                    <p>Try another league or refresh later.</p>
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
                    <span class="minute">${match.minute || 0}'</span>
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

                <p class="match-league">${match.league}</p>

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
                <p>Please try again later.</p>
            </div>
        `;
        console.error(error);
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const refreshButton = document.getElementById("refresh-btn");

    if (refreshButton) {
        refreshButton.addEventListener("click", refreshLiveMatches);
    }

    setInterval(refreshLiveMatches, 30000);
});
