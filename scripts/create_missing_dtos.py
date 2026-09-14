# One-shot generator for DTO packages that services import but were never generated.
import os

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "app", "dto")

SPECS = {
    "entryupdateapi": ("EntryupdateapiDto", ["knowledgeentryid", "title", "knowledgedocumentid", "content", "themeids", "status"]),
    "dashboardinitapi": ("DashboardinitapiDto", ["rolecode"]),
    "entriesinitapi": ("EntriesinitapiDto", []),
    "entryforminitapi": ("EntryforminitapiDto", ["id"]),
    "entrysaveapi": ("EntrysaveapiDto", ["title", "knowledgedocumentid", "content", "themeids", "status"]),
    "formexportapi": ("FormexportapiDto", ["formcode", "report_id"]),
    "verify2faapi": ("Verify2faapiDto", ["code", "rememberdevice"]),
    "api119_getreportforms": ("Api119GetreportformsDto", []),
    "api121_getstaffoptions": ("Api121GetstaffoptionsDto", []),
}


def write_dto(pkg, cls, fields):
    d = os.path.join(ROOT, pkg)
    os.makedirs(d, exist_ok=True)
    initp = os.path.join(d, "__init__.py")
    if not os.path.isfile(initp):
        with open(initp, "w", encoding="utf-8", newline="\n") as f:
            f.write("# DTO placeholder package\n")
    extra_init = "".join(", %s=\"\"" % f for f in fields)
    extra_assign = "".join("        self.%s = %s\n" % (f, f) for f in fields)
    extra_get = "".join(",\n            d.get(\"%s\", \"\")" % f for f in fields)
    body = (
        "from utils.base_entity import BaseEntity\n\n"
        "class %s(BaseEntity):\n"
        "    def __init__(self, mode, actflg, triggerid, row%s):\n"
        "        super().__init__(mode, actflg, triggerid, row)\n"
        "%s"
        "\n"
        "    @staticmethod\n"
        "    def dict_to_json(d):\n"
        "        if d is None:\n"
        "            d = {}\n"
        "        return %s(\n"
        "            d.get(\"mode\", \"\"),\n"
        "            d.get(\"actflg\", \"\"),\n"
        "            d.get(\"triggerid\", \"\"),\n"
        "            d.get(\"row\", \"\")%s)\n"
    ) % (cls, extra_init, extra_assign, cls, extra_get)
    path = os.path.join(d, pkg + "_dto.py")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(body)
    print("wrote", path)


if __name__ == "__main__":
    for pkg, (cls, fields) in SPECS.items():
        write_dto(pkg, cls, fields)
    print("done")
