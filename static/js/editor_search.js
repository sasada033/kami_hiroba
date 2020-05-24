$("#card-search-form").submit(function(e) {
    e.preventDefault()  // ページの読み込みを中止
    const this_ = $(this);
    const searchUrl = this_.attr("action");
    const keyword = $(".card-search-keyword").val();
    const gametitle = $(".card-search-gametitle").val();
    const search_results = $(".search-results");
    if (gametitle == "") {  // ゲームタイトル未選択の場合
        search_results.empty();  // 検索結果をリセット
        let span = $("<span>", {text: 'ゲームを選択してください。'});
        search_results.prepend(span);  // エラーメッセージを表示
    } else if (keyword == "") {
        search_results.empty();  // 検索結果をリセット
        let span = $("<span>", {text: 'キーワードを入力してください。'});
        search_results.prepend(span);  // エラーメッセージを表示
    } else {
        $.ajax({
            url: searchUrl,
            method: "GET",
            data: {
                "keyword": keyword,  // viewにdata辞書を渡す
                "gametitle": gametitle,
            },
            success: function(data) {  // viewからdata辞書を受け取る
                search_results.empty();  // 検索結果をリセット
                if (!data.queryset) {  // 検索結果が空の場合
                    let span = $("<span>", {text: `「${keyword}」に一致するカードは見つかりませんでした。`});
                    search_results.prepend(span);  // エラーメッセージを表示
                } else {
                    for (let results of data.queryset) {
                        for (let result of results) {
                            let span = $("<span>", {text: result});  // 検索結果を表示
                            search_results.append(span);
                        }
                        let button = $("<button>", {
                            type: "button", id: "card-append-button", "class": "form-control search-button",
                            value: results[0], text: "選択",
                        });
                        search_results.append(button)
                    }
                }
            }, error: function(error) {
                console.log("error")
            }
        })
    }
});
$(document).on("click", "#card-append-button", function() {
    const name = $(this).val();
    const option = $("<option>", {
        text: `《${name}》`,
    });
    $("#card-appended-list").append(option);
});
$(document).on("click", "#card-insert-button", function() {
    function insertContent(html) {  // ckeditorのテキストボックス内にて、キャレット位置に引数htmlを挿入
        for (let i in CKEDITOR.instances) {
            CKEDITOR.instances[i].insertHtml(html);
        }
        return true;
    }
    const name = $("#card-appended-list option:selected").text().slice(1, -1);
    const content = `《<a class="jquery-disabled" href="/">${name}</a>》`;
    insertContent(content)
});

