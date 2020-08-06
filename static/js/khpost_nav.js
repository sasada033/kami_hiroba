// 下スクロール時にヘッダーを隠す＆上スクロール時に再出現
$(function() {

    let startPos = 0, winScrollTop = 0;

    $(window).on("scroll", function() {
        winScrollTop = $(this).scrollTop();

        if (winScrollTop > startPos) {
            if (winScrollTop - startPos >= 10 && winScrollTop >= 50) {
                $(".header-fixed").addClass("hide");
            }
        } else if (winScrollTop < startPos) {
            if (startPos - winScrollTop >= 10) {
                $(".header-fixed").removeClass("hide");
            }
        }

        if (winScrollTop >= startPos + 20 || winScrollTop <= startPos - 20) {
            startPos = winScrollTop;
        }
    });
});

// ナビゲーションメニュー開閉
$(function() {

    const $nav = $("#nav-drawer");
    const show = "db"; // {display: block;} を付与
    const stop = "scroll-stop"; // {position: fixed;} を付与

    let scrollTop; // 現在のスクロール位置

    // ヘッダー左のメニュークリックでナビゲーション展開
    $(".header-menu-btn").on("click", function() {
        if (! $nav.hasClass(show)) {
            scrollTop = $(window).scrollTop(); // 現在のスクロール位置を取得
            $("body").addClass(stop); // 背景スクロール禁止
            $("body").scrollTop(scrollTop); // fixedでtop0に戻る＝＞スクロール位置に再移動
            $nav.addClass(show); // ナビゲーション展開
        } else {
            $("body").scrollTop(0); // いったんtop0に戻る
            $("body").removeClass(stop); // スクロール禁止解除
            window.scrollTo(0, scrollTop); // スクロール位置に再移動
            $nav.removeClass(show); // ナビゲーション折り畳み
        }
    });

    // ナビゲーション展開時のグレー背景部分をクリックしたとき、ナビゲーションを閉じる
    $(".nav-mask").on("click", function() {
        $("body").scrollTop(0); // いったんtop0に戻る
        $("body").removeClass(stop); // スクロール禁止解除
        window.scrollTo(0, scrollTop); // スクロール位置に再移動
        $nav.removeClass(show); // ナビゲーション折り畳み
    });
});
