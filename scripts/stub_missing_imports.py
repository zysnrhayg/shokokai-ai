# Create missing app.dao / app.mapper / app.service / app.dto modules so Flask can import.
import importlib
import os
import sys
import traceback

from dotenv import load_dotenv

load_dotenv()
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


def camel(name):
    return "".join(part[:1].upper() + part[1:] for part in name.split("_") if part)


def write_file(path, body):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if os.path.isfile(path):
        return False
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(body)
    print("created", os.path.relpath(path, ROOT))
    return True


def stub_for(mod):
    parts = mod.split(".")
    if len(parts) < 3 or parts[0] != "app":
        raise RuntimeError("cannot stub " + mod)
    kind = parts[1]
    pkg = parts[2]
    pkg_dir = os.path.join(ROOT, "app", kind, pkg)
    init_path = os.path.join(pkg_dir, "__init__.py")
    write_file(init_path, "# placeholder package\n")
    if len(parts) == 3:
        return
    leaf = parts[3]
    path = os.path.join(pkg_dir, leaf + ".py")
    if kind == "dao":
        cls = camel(pkg) + "Dao"
        meth = pkg
        body = (
            "class %s:\n"
            "    def %s(self, dtoObj=None):\n"
            "        return []\n"
            "    def __getattr__(self, name):\n"
            "        def _missing(*args, **kwargs):\n"
            "            return []\n"
            "        return _missing\n"
        ) % (cls, meth)
    elif kind == "mapper":
        cls = pkg + "Mapper"
        body = (
            "class %s:\n"
            "    @staticmethod\n"
            "    def %s(*args, **kwargs):\n"
            "        return \"SELECT 1 WHERE 1 = 0\"\n"
        ) % (cls, pkg)
    elif kind == "service":
        cls = camel(pkg) + "Service"
        body = (
            "class %s:\n"
            "    def __getattr__(self, name):\n"
            "        def _missing(*args, **kwargs):\n"
            "            return args[-1] if args else None\n"
            "        return _missing\n"
        ) % cls
    elif kind == "dto":
        cls = camel(pkg) + "Dto"
        body = (
            "from utils.base_entity import BaseEntity\n\n"
            "class %s(BaseEntity):\n"
            "    def __init__(self, mode, actflg, triggerid, row):\n"
            "        super().__init__(mode, actflg, triggerid, row)\n\n"
            "    @staticmethod\n"
            "    def dict_to_json(d):\n"
            "        if d is None:\n"
            "            d = {}\n"
            "        return %s(d.get(\"mode\", \"\"), d.get(\"actflg\", \"\"), d.get(\"triggerid\", \"\"), d.get(\"row\", \"\"))\n"
        ) % (cls, cls)
    else:
        body = "# placeholder\n"
    write_file(path, body)


def main():
    for _ in range(30):
        for key in list(sys.modules):
            if key.startswith("app.controller.commonfunctioncontroller") or key.startswith("app.service.accounts"):
                sys.modules.pop(key, None)
        try:
            importlib.import_module("app.controller.commonfunctioncontroller")
            print("ok")
            return 0
        except ModuleNotFoundError as exc:
            name = exc.name or ""
            print("missing", name)
            if not name.startswith("app."):
                traceback.print_exc()
                return 1
            stub_for(name)
        except Exception:
            traceback.print_exc()
            return 1
    print("gave up")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
