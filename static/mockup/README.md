# モックアップ分解一覧

出典: `商工会AIシステムのモックアップ.html`

## CSS（6 ブロック → `css/mockup.css` 統合）

- `css/mockup-part-01.css`
- `css/mockup-part-02.css`
- `css/mockup-part-03.css`
- `css/mockup-part-04.css`
- `css/mockup-part-05.css`
- `css/mockup-part-06.css`

## JavaScript / データ

| 文件 | 类型 | 备注 |
|------|------|------|
| `js/login_otp_input.js` | javascript | login_otp_input |
| `js/toast.js` | javascript | toast |
| `js/select_width.js` | javascript | select_width |
| `js/dom_utils.js` | javascript | dom_utils |
| `js/nav_toggle.js` | javascript | nav_toggle |
| `js/role_accent.js` | javascript | role_accent |
| `js/org_role_switcher.js` | javascript | org_role_switcher |
| `js/dashboard.js` | javascript | dashboard |
| `js/layout_sync.js` | javascript | layout_sync |
| `data/monthly-data.json` | json | monthly-data |
| `js/entry_form_wiring.js` | javascript | entry_form_wiring |
| `js/expert_import_modal.js` | javascript | expert_import_modal |
| `js/ai_proposal.js` | javascript | ai_proposal |
| `js/monthly.js` | javascript | monthly |
| `js/reports_annual_csv.js` | javascript | reports_annual_csv |
| `js/entry_screen.js` | javascript | entry_screen |
| `js/expert_import_wire.js` | javascript | expert_import_wire |
| `js/reports_list.js` | javascript | reports_list |
| `js/entry_history.js` | javascript | entry_history |
| `js/entry_jigyosho_autocomplete.js` | javascript | entry_jigyosho_autocomplete |
| `js/accounts.js` | javascript | accounts |
| `js/knowledge.js` | javascript | knowledge |
| `js/knowledge_search.js` | javascript | knowledge_search |
| `js/router.js` | javascript | router |

## 画面 HTML（`html/pages/` — 16画面）

| No | 画面名 | 文件 | 内容快照 |
|----|--------|------|----------|
| 1 | ログイン画面 | `html/pages/login.html` | 有 |
| 2 | 二段階認証画面 | `html/pages/verify_2fa.html` | 有 |
| 3 | ダッシュボード（全国連） | `html/pages/dashboard_national.html` | 有 |
| 4 | ダッシュボード（県連） | `html/pages/dashboard_pref.html` | 有 |
| 5 | ダッシュボード（商工会） | `html/pages/dashboard_shokokai.html` | 有 |
| 6 | 相談を受ける | `html/pages/form_ai_input.html` | 有 |
| 7 | 報告書を作る | `html/pages/form_new.html` | 有 |
| 8 | 専門家の報告を取り込む | `html/pages/form_expert_import.html` | 有 |
| 9 | 報告書を見る | `html/pages/reports.html` | 有 |
| 10 | 実績確認・帳票出力 | `html/pages/monthly.html` | 有 |
| 11 | AIと一緒に考える | `html/pages/search.html` | 有 |
| 12 | ナレッジを検索する | `html/pages/knowledge_search.html` | 有 |
| 13 | アカウント一覧 | `html/pages/accounts.html` | 有 |
| 14 | ナレッジ管理（①ファイル保管＝文書一覧） | `html/pages/documents_list.html` | 有 |
| 15 | ナレッジ管理（②タグ付け・レビュー＝知識データ一覧） | `html/pages/entries_list.html` | 有 |
| 16 | ナレッジ管理（③ベクトル反映） | `html/pages/vectors_list.html` | 有 |

- `html/pages/*.html` — 可单独打开的完整页面（含 CSS/JS）
- `html/pages/*_content.html` — JS 渲染后的画面内容快照

## 技術用 DOM 片段（`html/*.html`）

| view_id | 片段 | 说明 |
|---------|------|------|
| `view-home` | `html/home.html` | 静态HTML |
| `view-entry` | `html/entry.html` | 静态HTML |
| `view-reports` | `html/reports.html` | 静态HTML |
| `view-ai-proposal` | `html/ai_proposal.html` | 静态HTML |
| `view-monthly` | `html/monthly.html` | 静态HTML |
| `view-accounts` | `html/accounts.html` | 静态HTML |
| `view-knowledge` | `html/knowledge.html` | 静态HTML |
| `view-knowledge-search` | `html/knowledge_search.html` | 静态HTML |
| `view-login` | `html/login.html` | 静态HTML |
| `view-verify-2fa` | `html/verify_2fa.html` | 静态HTML |

原 mockup 按 `app-view` 切分的 DOM 片段；部分仅为 JS 空容器。

## レイアウト

- `layout/app_shell.html` — サイドバー＋`main-mount`（ビューはプレースホルダ）
- `preview.html` — 分解後 CSS/JS を読み込む統合プレビュー

再生成:

```powershell
$env:SHOKOKAI_REPO = "D:\eclipse17\workspace\shokokai-ai-flask"
py .cursor/skills/shokokai-freecode-sekkei/scripts/extract_mockup_assets.py
```
