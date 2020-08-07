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

    const $nav = $(".nav-drawer"); // ナビゲーション祖先
    const $menu = $(".nav-menu"); // ナビゲーションメニュー
    const $search = $(".nav-search"); // ナビゲーション検索
    const show = "show"; // {visibility: visible;} を付与
    const active = "active"; // メニューor検索をアクティブ状態に
    const stop = "scroll-stop"; // {position: fixed;} を付与

    let scrollTop; // 現在のスクロール位置

    // ヘッダー左のメニュークリックでナビゲーション展開
    $(".header-menu-btn").on("click", function() {
        if (! $nav.hasClass(show)) {
            scrollTop = $(window).scrollTop(); // 現在のスクロール位置を取得
            $("body").addClass(stop); // 背景スクロール禁止
            $("body").scrollTop(scrollTop); // fixedでtop0に戻る＝＞スクロール位置に再移動
            $nav.addClass(show); // ナビゲーション展開
            $menu.addClass(active); // メニューをアクティブに
        } else {
            if ($search.hasClass(active)) {
                $search.removeClass(active);
                $menu.addClass(active);
            } else {
                $("body").scrollTop(0); // いったんtop0に戻る
                $("body").removeClass(stop); // スクロール禁止解除
                window.scrollTo(0, scrollTop); // スクロール位置に再移動
                $nav.removeClass(show); // ナビゲーション折り畳み
                $menu.removeClass(active); // メニューのアクティブ解除
            }
        }
    });

    // ヘッダー右の検索クリックでナビゲーション展開
    $(".header-search-btn").on("click", function() {
        if (! $nav.hasClass(show)) {
            scrollTop = $(window).scrollTop(); // 現在のスクロール位置を取得
            $("body").addClass(stop); // 背景スクロール禁止
            $("body").scrollTop(scrollTop); // fixedでtop0に戻る＝＞スクロール位置に再移動
            $nav.addClass(show); // ナビゲーション展開
            $search.addClass(active); // 検索をアクティブに
        } else {
            if ($menu.hasClass(active)) {
                $menu.removeClass(active);
                $search.addClass(active);
            } else {
                $("body").scrollTop(0); // いったんtop0に戻る
                $("body").removeClass(stop); // スクロール禁止解除
                window.scrollTo(0, scrollTop); // スクロール位置に再移動
                $nav.removeClass(show); // ナビゲーション折り畳み
                $search.removeClass(active); // 検索のアクティブ解除
            }
        }
    });

    // ナビゲーション展開時のグレー背景部分をクリックしたとき、ナビゲーションを閉じる
    $(".nav-mask").on("click", function() {
        $("body").scrollTop(0); // いったんtop0に戻る
        $("body").removeClass(stop); // スクロール禁止解除
        window.scrollTo(0, scrollTop); // スクロール位置に再移動
        $nav.removeClass(show); // ナビゲーション折り畳み
        $menu.removeClass(active); // メニューのアクティブ解除
        $search.removeClass(active); // 検索のアクティブ解除
    });
});
