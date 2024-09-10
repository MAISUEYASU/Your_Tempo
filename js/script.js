let tapTimes = [];
let tempo = 0;

// ボタンがクリックされた時の処理
document.getElementById("tapButton").addEventListener("click", function () {
  const currentTime = Date.now(); // 現在の時間を取得
  tapTimes.push(currentTime); //タップの時間を記録

  // 2回以上タップされている場合、テンポを計算する
  if (tapTimes.length > 1) {
    const intervals = tapTimes
      .slice(1) // 最初の要素を除く
      .map((time, i) => time - tapTimes[i]); // 各タップの間隔を計算
    const avgInterval = intervals.reduce((a, b) => a + b) / intervals.length; // 平均間隔
    tempo = Math.round(60000 / avgInterval); // BPMを計算
    document.getElementById("tempoDisplay").textContent = `Tempo: ${tempo} BPM`; // テンポを表示
  }

  // ５回以上タップした場合、テンポをサーバー送信してプレイリストを作成
  if (tapTimes.length > 5) {
    fetch("/create_playlist", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ tempo: tempo }), // 計測したテンポを送信
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.tracks) {
          // 取得したプレイリストの曲を表示
          document.getElementById(
            "playlist"
          ).innerHTML = `<h2>Generated Playlist:</h2>
            <ul>${data.tracks
              .map((track) => `<li>${track.name} by ${track.artist}</li>`)
              .join("")}</ul>`;
        } else {
          alert("エラーが発生しました: " + data.error);
        }
      })
      .catch((error) => {
        alert(
          "プレイリストの作成中にエラーが発生しました。もう一度お試しください。"
        );
        console.error("エラー:", error);
      });
    tapTimes = []; // タップの記録をリセット
  }
});
