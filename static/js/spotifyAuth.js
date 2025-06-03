document.addEventListener("DOMContentLoaded", () => {
  setupSpotifyLogin();
  checkSpotifyLoginStatus();
});

// Spotifyログインボタンのセットアップ
function setupSpotifyLogin() {
  const loginButton = document.getElementById("spotify-login-btn");
  if (loginButton) {
    loginButton.addEventListener("click", () => {
      window.location.href = "/login";
    });
  }
}

// Spotifyログイン状態のチェック
async function checkSpotifyLoginStatus() {
  try {
    const response = await fetch("/get_user_info");
    const data = await response.json();

    if (data.userName) {
      window.location.replace("/countTempo");
    }
  } catch (error) {
    console.error("ログイン状態の確認エラー:", error);
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const retryButton = document.getElementById("retryButton");
  if (retryButton) {
    retryButton.addEventListener("click", () => {
      window.location.href = "/countTempo";
    });
  }
});
