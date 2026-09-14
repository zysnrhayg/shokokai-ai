# -*- coding: utf-8 -*-
"""Copy mockup_extracted frontend into this Flask project."""
import os
import re
import shutil

SRC = r"C:\EDIS\mockup_extracted"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DST_STATIC = os.path.join(ROOT, "static", "mockup")
DST_TPL = os.path.join(ROOT, "templates")


def rewrite_static_html(text: str) -> str:
    text = text.replace(
        'href="../../css/mockup.css"',
        'href="/static/mockup/css/mockup.css"',
    )
    text = text.replace(
        'href="css/mockup.css"',
        'href="/static/mockup/css/mockup.css"',
    )
    text = re.sub(
        r'src="\.\./\.\./js/([^"]+)"',
        r'src="/static/mockup/js/\1"',
        text,
    )
    text = re.sub(r'src="js/([^"]+)"', r'src="/static/mockup/js/\1"', text)
    return text


def copy_assets() -> None:
    os.makedirs(DST_STATIC, exist_ok=True)
    for name in ("css", "js", "data", "html", "layout"):
        src = os.path.join(SRC, name)
        dst = os.path.join(DST_STATIC, name)
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
        print("copied", name)
    for name in ("preview.html", "README.md", "manifest.json"):
        shutil.copy2(os.path.join(SRC, name), os.path.join(DST_STATIC, name))
        print("copied", name)

    for root, _dirs, files in os.walk(os.path.join(DST_STATIC, "html")):
        for fname in files:
            if not fname.endswith(".html"):
                continue
            path = os.path.join(root, fname)
            with open(path, "r", encoding="utf-8") as fh:
                text = fh.read()
            with open(path, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(rewrite_static_html(text))

    preview_path = os.path.join(DST_STATIC, "preview.html")
    with open(preview_path, "r", encoding="utf-8") as fh:
        preview = fh.read()
    with open(preview_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(rewrite_static_html(preview))

    layout_path = os.path.join(DST_STATIC, "layout", "app_shell.html")
    with open(layout_path, "r", encoding="utf-8") as fh:
        layout = fh.read()
    with open(layout_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(rewrite_static_html(layout))
    print("rewrote static html paths")


def build_app_template() -> None:
    with open(os.path.join(SRC, "preview.html"), "r", encoding="utf-8") as fh:
        html = fh.read()

    html = html.replace(
        "<title>商工会AIシステムのモックアップ（統合版：ホーム／相談を受ける・報告書を作る・専門家の報告を取り込む／報告書を見る／月次帳票を出力する を1ファイルに統合、CSS/JS完全内蔵）（分解プレビュー）</title>",
        "<title>商工会AIシステム</title>",
    )
    html = html.replace(
        '<link rel="stylesheet" href="css/mockup.css">',
        '<link rel="stylesheet" href="{{ url_for(\'static\', filename=\'mockup/css/mockup.css\') }}">',
    )
    html = re.sub(
        r'<script src="js/([^"]+)"></script>',
        lambda m: (
            '<script src="{{ url_for(\'static\', filename=\'mockup/js/'
            + m.group(1)
            + '\') }}"></script>'
        ),
        html,
    )
    html = re.sub(
        r'<script id="monthly-data" type="application/json">[\s\S]*?</script>',
        '<script id="monthly-data" type="application/json">{{ monthly_data|safe }}</script>',
        html,
        count=1,
    )
    html = html.replace('<div id="app-shell">', '<div id="app-shell" style="display:none;">')
    html = html.replace(
        '<a class="top-bar-btn" href="#login">🚪 ログアウト</a>',
        '<a class="top-bar-btn" href="{{ url_for(\'logout\') }}">🚪 ログアウト</a>',
    )
    html = html.replace(
        "</head>",
        "<script>window.__IS_LOGGED_IN = {{ 'true' if logged_in else 'false' }};</script>\n</head>",
    )

    out_tpl = os.path.join(DST_TPL, "app.html")
    with open(out_tpl, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(html)
    print("wrote", out_tpl, "bytes", os.path.getsize(out_tpl))

    legacy = os.path.join(DST_TPL, "login_legacy.html")
    old_login = os.path.join(DST_TPL, "login.html")
    if os.path.exists(old_login) and not os.path.exists(legacy):
        shutil.copy2(old_login, legacy)
        print("backed up login.html -> login_legacy.html")


def main() -> None:
    if not os.path.isdir(SRC):
        raise SystemExit("source not found: " + SRC)
    copy_assets()
    build_app_template()
    print("done")


if __name__ == "__main__":
    main()
