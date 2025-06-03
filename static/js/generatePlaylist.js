async function generatePlaylist(tempo) {
  try {
    const response = await fetch("/generate_playlist", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ tempo }),
    });

    let data;
    try {
      // JSON解析エラーも考慮
      data = await response.json();
    } catch (jsonError) {
      console.error("JSON解析エラー:", jsonError);
      throw new Error("サーバーから不正なレスポンスを受け取りました。");
    }

    if (response.ok) {
      document.getElementById("messageText").innerText =
        "プレイリストが作成されました！";

      // 要素が存在するかチェックしてから呼び出し
      if (
        window.displayTrackList &&
        typeof window.displayTrackList === "function"
      ) {
        window.displayTrackList(data);
      } else {
        console.error("displayTrackList 関数が見つかりません。");
      }
    } else {
      console.error("プレイリスト作成エラー:", data.error || "不明なエラー");
      document.getElementById(
        "messageText"
      ).innerText = `プレイリストの作成に失敗しました。: ${
        data.error || "楽曲が見つかりませんでした。"
      }`;
    }
  } catch (error) {
    console.error("プレイリスト作成エラー:", error);
    document.getElementById("messageText").innerText =
      "サーバーエラーが発生しました。もう一度お試しください。";
  }
}
