$(".like-btn").click(function(e) {
    e.preventDefault()  // ページの読み込みを中止
    const this_ = $(this);
    const like_cnt = $(".liked-cnt");
    const likeUrl = this_.attr("data-href");
    if (likeUrl) {
        $.ajax({
            url: likeUrl,
            method: "GET",
            data: {
                "status": true
            },  // viewにdata辞書を渡す
            success: function(data) {  // viewからdata辞書を受け取る
                let change_like = like_cnt.text();
                if (data.followed) {
                    like_cnt.text(++change_like);
                    this_.addClass("on");  // liked=trueなら、いいね数を＋１しボタンの色を変更
                } else {
                    like_cnt.text(--change_like);
                    this_.removeClass("on");
                }
            }, error: function(error) {
                console.log("error")
            }
        })
    }
});
