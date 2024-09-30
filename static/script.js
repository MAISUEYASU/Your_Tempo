// Spotifyユーザーのトップアーティストを基におすすめの楽曲を取得
function getTopTracks(access_token) {
  fetch("https://api.spotify.com/v1/me/top/artists?limit=5", {
    headers: {
      Authorization: "Bearer " + access_token,
    },
  })
    .then((response) => response.json())
    .then((data) => {
      const seed_artists = data.items.map((artist) => artist.id).join(",");
      return fetch(
        `https://api.spotify.com/v1/recommendations?seed_artists=${seed_artists}&limit=10`,
        {
          headers: {
            Authorization: "Bearer " + access_token,
          },
        }
      );
    })
    .then((response) => response.json())
    .then((recommendations) => {
      document.getElementById("playlist").innerHTML = `
					<h2>おすすめのプレイリスト:</h2>
					<ul>
							${recommendations.tracks
                .map(
                  (track) => `
									<li>
											<a href="https://open.spotify.com/track/${track.id}" target="_blank">
													${track.name} by ${track.artists[0].name}
											</a>
									</li>
							`
                )
                .join("")}
					</ul>
			`;
    });
}

// タップされた後にプレイリストを生成
let tapTimes = [];

document.getElementById("tapButton").addEventListener("click", function () {
  const currentTime = Date.now();
  tapTimes.push(currentTime);

  if (tapTimes.length > 1) {
    const intervals = tapTimes.slice(1).map((time, i) => time - tapTimes[i]);
    const avgInterval = intervals.reduce((a, b) => a + b) / intervals.length;
    const tempo = Math.round(60000 / avgInterval);
    document.getElementById("tempoDisplay").textContent = `Tempo: ${tempo} BPM`;

    if (tapTimes.length > 5) {
      fetch("/generate_playlist", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ tempo: tempo }),
      })
        .then((response) => response.json())
        .then((data) => {
          const filteredTracks = data.tracks.filter(
            (track) => !/\b(BPM|bpm|tempo|TEMPO)\b/.test(track.name)
          );
          document.getElementById("playlist").innerHTML = `
									<h2>生成されたプレイリスト:</h2>
									<ul>
											${filteredTracks
                        .map(
                          (track) => `
													<li style="display: flex; align-items: center;">
															<img src="${track.album_image}" alt="Album cover" width="50" height="50" style="margin-right: 10px;">
															<a href="https://open.spotify.com/track/${track.id}" target="_blank">
																	${track.name} by ${track.artists[0].name}
															</a>
													</li>
											`
                        )
                        .join("")}
									</ul>
							`;
        })
        .catch((error) => {
          alert(
            "プレイリストの作成中にエラーが発生しました。もう一度お試しください。"
          );
          console.error("エラー:", error);
        });

      tapTimes = [];
    }
  }
});
