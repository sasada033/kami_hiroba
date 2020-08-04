$("#card-search-form").submit(function(e) {
    e.preventDefault()  // ページの読み込みを中止
    const this_ = $(this);
    const searchUrl = this_.attr("action");
    const keyword = $(".card-search-keyword").val();
    const gametitle = $(".card-search-gametitle option:selected");
    const search_results = $(".search-results");
    if (gametitle.val() == "") {  // ゲームタイトル未選択の場合
        search_results.empty();  // 検索結果をリセット
        let span = $("<span>", {text: 'ゲームを選択してください。'});
        search_results.prepend(span);  // エラーメッセージを表示
    } else if (keyword == "") {  // 検索キーワード未入力の場合
        search_results.empty();  // 検索結果をリセット
        let span = $("<span>", {text: 'キーワードを入力してください。'});
        search_results.prepend(span);  // エラーメッセージを表示
    } else {
        $.ajax({
            url: searchUrl,
            method: "GET",
            data: {
                "keyword": keyword,  // viewにdata辞書を渡す
                "gametitle": gametitle.text(),
            },
            success: function(data) {  // viewからdata辞書を受け取る
                search_results.empty();  // 検索結果をリセット
                if (!data.queryset) {  // 検索結果が空の場合
                    let span = $("<span>", {text: `「${keyword}」に一致するカードは見つかりませんでした。`});
                    search_results.prepend(span);  // エラーメッセージを表示
                } else {
                    let html_result = '';
                    for (let results of data.queryset) {  // querysetから値を取り出す
                        let div_result = '<div class="">';
                        let a = "<a>" + results[0] + "</a>";  // 検索結果を表示(カード名のみaタグ)
                        div_result += a;
                        for (let result of results.slice(1)) {
                            let span = "<span>" + result + "</span>";  // 検索結果を表示(カード名以外spanタグ)
                            div_result += span;
                        }
                        let button = $("<button>", {  // 検索結果ひとつひとつに選択ボタンを用意
                            type: "button", id: "card-append-button", "class": "form-control search-button",
                            value: results[0], text: "選択",
                        });
                        div_result += "</div>";
                        html_result += div_result;
                    }
                    search_results[0].innerHTML = html_result;
                }
            }, error: function(error) {
                console.log("error")
            }
        })
    }
});
$(document).on("click", "#card-append-button", function() {
    const name = $(this).val();
    const option = $("<option>", {  // 検索結果の選択ボタンを押すとそのカード名がセレクトボックスにバインドされる
        text: `《${name}》`,
    });
    $("#card-appended-list").append(option);
});
$(document).on("click", "#card-insert-button", function() {
    function insertContent(html) {  // ckeditorのテキストエリアにて、キャレット位置に引数htmlを挿入する関数
        for (let i in CKEDITOR.instances) {
            CKEDITOR.instances[i].insertHtml(html);
        }
        return true;
    }
    const name = $("#card-appended-list option:selected").text().slice(1, -1);
    const content = `《<a class="jquery-disabled" href="/">${name}</a>》`;
    insertContent(content)  // セレクトボックスで選択中のカード名をテキストエリアに挿入
});

