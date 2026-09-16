# helpers to serialize DAO rows for AI proposal JSON responses


def jsonable_row(rec):
    if not isinstance(rec, dict):
        return {}
    out = {}
    for key, value in rec.items():
        if hasattr(value, "isoformat"):
            out[key] = value.isoformat()
        elif value is None:
            out[key] = ""
        elif isinstance(value, list):
            out[key] = [
                jsonable_row(v) if isinstance(v, dict) else ("" if v is None else v)
                for v in value
            ]
        else:
            out[key] = value
    return out


def jsonable_rows(rows):
    return [jsonable_row(r) for r in (rows or []) if isinstance(r, dict)]


def entries_to_proposals(rows, limit=4, offset=0):
    """Map knowledge entries to AI proposal cards (no real LLM)."""
    items = jsonable_rows(rows)
    if offset:
        items = items[offset:] + items[:offset]
    proposals = []
    for rec in items[:limit]:
        title = str(rec.get("title") or "").strip() or "支援提案"
        content = str(rec.get("content") or "").strip()
        code = str(rec.get("knowledge_code") or "").strip()
        proposals.append(
            {
                "title": title,
                "body": content[:800] if content else "関連ナレッジに基づく支援案です。",
                "meta": ("関連ナレッジ：" + code) if code else "関連ナレッジ",
                "knowledge_entry_id": rec.get("knowledge_entry_id"),
                "knowledge_code": code,
            }
        )
    return proposals
