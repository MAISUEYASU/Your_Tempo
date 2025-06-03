// 要素が存在するまで待機する関数
function waitForElement(id, callback) {
  const element = document.getElementById(id);
  if (element) {
    callback();
  } else {
    setTimeout(() => waitForElement(id, callback), 100);
  }
}

// `displayTrackList` 関数の定義を待機してから設定
waitForElement("resultModal", () => {
  console.log("全ての要素がロードされました。");

  window.displayTrackList = function (data) {
    const playlistLink = document.getElementById("playlistLink");
    const trackList = document.getElementById("trackList");
    const resultModalElement = document.getElementById("resultModal");

    // 要素が取得できているか確認
    if (!playlistLink || !trackList || !resultModalElement) {
      console.error(
        "表示要素が見つかりません。playlistLink、trackList または resultModal が null です。"
      );
      return;
    }

    // プレイリストリンクの設定
    playlistLink.href = data.playlist_url;
    playlistLink.target = "_blank";
    playlistLink.classList.remove("d-none");

    // 楽曲リストの表示
    trackList.innerHTML = data.tracks
      .map(
        (track) =>
          `<li class="list-group-item d-flex align-items-center">
            <img src="${track.album_image}" alt="${track.name}" class="me-3" style="width: 50px; height: 50px;">
            <span>${track.name} - ${track.artist}</span>
          </li>`
      )
      .join("");

    // モーダルの表示
    try {
      const resultModal = new bootstrap.Modal(resultModalElement, {
        backdrop: "static",
        keyboard: false,
      });
      resultModal.show();
    } catch (error) {
      console.error("モーダル表示エラー:", error);
    }
  };
});
