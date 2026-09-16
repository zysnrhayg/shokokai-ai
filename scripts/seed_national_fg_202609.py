"""全国連(00/0021) 令和8年9月向け F/G + KPI テストデータ投入。"""
from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)
os.environ.setdefault("PROJECT_ROOT", str(ROOT))
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv

load_dotenv(ROOT / ".env")

import utils.mysqldb_utils as db  # noqa: E402


PREF = "00"
SHO = "0021"
FY_ID = 3
YM = "2026-09"
THEME_ID = 14
INDUSTRY = "C"


def _exec(sql: str, params: dict | None = None):
    return db.querySQL(sql, params or {})


def main() -> int:
    rows = [
        ("F", "2026-09-10", "10:00", "10:30", "全国Fテスト", "全国Fテスト内容", "全国担当A", "全国テスト事業所A"),
        ("G-3", "2026-09-11", "11:00", "12:00", "全国G-3テスト", "全国G-3テスト内容", "全国担当B", "全国テスト事業所B"),
        ("G-2", "2026-09-12", "13:00", "13:30", "全国G-2テスト", "全国G-2テスト内容", "全国担当C", "全国テスト事業所C"),
    ]
    inserted = []
    for form_code, report_date, t0, t1, summary, content, person, biz in rows:
        sql = """
INSERT INTO trn_report (
  report_code, form_code, fiscal_year_id, prefecture_code, shokokai_cd,
  theme_id, industry_code, report_date,
  summary, content, time_start, time_end,
  business_person, business_name, staff_main_name,
  registered_at, status, created_by, updated_by
) VALUES (
  :report_code, :form_code, CAST(:fiscal_year_id AS integer), :prefecture_code, :shokokai_cd,
  CAST(:theme_id AS integer), :industry_code, CAST(:report_date AS date),
  :summary, :content, :time_start, :time_end,
  :business_person, :business_name, :staff_main_name,
  CAST(:report_date AS date), '登録済み', 1, 1
)
RETURNING report_id
"""
        code = "RPT-NAT-%s-%s" % (form_code.replace("-", ""), report_date.replace("-", ""))
        result = _exec(
            sql,
            {
                "report_code": code,
                "form_code": form_code,
                "fiscal_year_id": FY_ID,
                "prefecture_code": PREF,
                "shokokai_cd": SHO,
                "theme_id": THEME_ID,
                "industry_code": INDUSTRY,
                "report_date": report_date,
                "summary": summary,
                "content": content,
                "time_start": t0,
                "time_end": t1,
                "business_person": person,
                "business_name": biz,
                "staff_main_name": "全国職員テスト",
            },
        )
        recs = db.result_to_list_of_dict(result) or []
        if not recs:
            print("FAIL insert", form_code)
            return 1
        rid = recs[0].get("report_id")
        inserted.append((form_code, rid))
        _exec(
            """
INSERT INTO trn_report_theme (report_id, theme_id)
VALUES (CAST(:report_id AS integer), CAST(:theme_id AS integer))
ON CONFLICT DO NOTHING
""",
            {"report_id": rid, "theme_id": THEME_ID},
        )

    _exec(
        """
INSERT INTO trn_kpi_theme_breakdown (
  prefecture_code, shokokai_cd, fiscal_year_id, theme_id, year_month, support_count, created_by, updated_by
) VALUES (
  :prefecture_code, :shokokai_cd, CAST(:fiscal_year_id AS integer), CAST(:theme_id AS integer),
  :year_month, CAST(:support_count AS integer), 1, 1
)
ON CONFLICT (prefecture_code, shokokai_cd, fiscal_year_id, theme_id, year_month)
DO UPDATE SET
  support_count = trn_kpi_theme_breakdown.support_count + EXCLUDED.support_count,
  updated_at = to_char(now(), 'YYYYMMDDHH24MISS'),
  updated_by = 1
""",
        {
            "prefecture_code": PREF,
            "shokokai_cd": SHO,
            "fiscal_year_id": FY_ID,
            "theme_id": THEME_ID,
            "year_month": YM,
            "support_count": len(rows),
        },
    )

    _exec(
        """
INSERT INTO trn_kpi_monthly_stat (
  prefecture_code, shokokai_cd, fiscal_year_id, target_prefecture_code, target_shokokai_cd,
  year_month, support_count, ai_activity_count, created_by, updated_by
) VALUES (
  :prefecture_code, :shokokai_cd, CAST(:fiscal_year_id AS integer), NULL, NULL,
  :year_month, CAST(:support_count AS integer), 0, 1, 1
)
ON CONFLICT (prefecture_code, shokokai_cd, fiscal_year_id, target_prefecture_code, target_shokokai_cd, year_month)
DO UPDATE SET
  support_count = trn_kpi_monthly_stat.support_count + EXCLUDED.support_count,
  updated_at = to_char(now(), 'YYYYMMDDHH24MISS'),
  updated_by = 1
""",
        {
            "prefecture_code": PREF,
            "shokokai_cd": SHO,
            "fiscal_year_id": FY_ID,
            "year_month": YM,
            "support_count": len(rows),
        },
    )

    print("OK seeded national F/G for 2026-09:")
    for form_code, rid in inserted:
        print(" -", form_code, "report_id=", rid)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
