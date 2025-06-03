document.addEventListener("DOMContentLoaded", () => {
  const tapButton = document.getElementById("tapButton");
  const messageText = document.getElementById("messageText");
  const tempoDisplay = document.getElementById("tempoDisplay");
  let tempoClicks = [];
  const requiredClicks = 5;
  const minInterval = 300;
  const maxBPM = 220;

  messageText.innerText = "5回タップしてね";

  // タップボタン
  tapButton.addEventListener("click", () => {
    // ボタンアニメーションのトリガー
    tapButton.classList.add("tapped");
    setTimeout(() => {
      tapButton.classList.remove("tapped");
    }, 200);

    const clickTime = Date.now();
    const lastClickTime = tempoClicks[tempoClicks.length - 1] || 0;

    // タップが早すぎる場合は無視
    if (clickTime - lastClickTime < minInterval) {
      messageText.innerText =
        "タップが早すぎます。ゆっくりタップしてください。";
      return;
    }

    // タップ時間を記録
    tempoClicks.push(clickTime);

    // タップ回数に応じてメッセージを更新
    const remainingClicks = requiredClicks - tempoClicks.length;
    if (remainingClicks > 0) {
      messageText.innerText = `あと${remainingClicks}回タップしてね`;
    }

    // リアルタイムで BPM を計算して表示
    if (tempoClicks.length > 1) {
      const avgInterval =
        (clickTime - tempoClicks[0]) / (tempoClicks.length - 1);
      const calculatedTempo = Math.round(60000 / avgInterval);

      if (calculatedTempo > maxBPM) {
        messageText.innerText = "BPMが高すぎます。もう一度タップしてください。";
        tempoClicks = [];
        tempoDisplay.innerText = "Tempo: 0 BPM";
        return;
      }

      tempoDisplay.innerText = `Tempo: ${calculatedTempo} BPM`;
      if (calculatedTempo >= 80) {
        tapButton.style.backgroundColor = "#ff6a00"; // オレンジ
      } else {
        tapButton.style.backgroundColor = "#63d4db"; // 淡いブルー
      }
    }

    // 5回タップ
    if (tempoClicks.length === requiredClicks) {
      messageText.innerText = "プレイリストを作成中...";
      const avgInterval = (tempoClicks[4] - tempoClicks[0]) / 4;
      const calculatedTempo = Math.round(60000 / avgInterval);
      generatePlaylist(calculatedTempo);
    }
  });
  // リセットボタンのクリックイベント
  retryButton.addEventListener("click", () => {
    resetState();
    window.location.href = "/countTempo";
  });

  // リセット関数
  function resetState() {
    tempoClicks = [];
    messageText.innerText = "5回タップしてね";
    tempoDisplay.innerText = "Tempo: 0 BPM";
    tapButton.style.backgroundColor = "#63d4db"; // 初期色に戻す
  }
});
