# -*- coding: utf-8 -*-
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

from flask import Flask, render_template

app = Flask(
    __name__,
    template_folder=os.path.join(ROOT, "templates"),
    static_folder=os.path.join(ROOT, "static"),
)

@app.route("/logout")
def logout():
    return "ok"

monthly_path = os.path.join(ROOT, "static", "mockup", "data", "monthly-data.json")
with open(monthly_path, encoding="utf-8") as fh:
    monthly_data = fh.read()
json.loads(monthly_data)

css_path = os.path.join(ROOT, "static", "mockup", "css", "mockup.css")
router_path = os.path.join(ROOT, "static", "mockup", "js", "router.js")
assert os.path.isfile(css_path), "missing mockup.css"
assert os.path.isfile(router_path), "missing router.js"

with app.test_request_context("/"):
    html = render_template("app.html", monthly_data=monthly_data, logged_in=False)

assert "商工会AIシステム" in html
assert "/static/mockup/css/mockup.css" in html
assert "/static/mockup/js/router.js" in html
assert 'id="login-form"' in html
assert 'id="view-home"' in html
assert "url_for(" not in html
assert "\\\\'" not in html
assert "__IS_LOGGED_IN = false" in html
print("template ok, length", len(html))
print("monthly json keys", list(json.loads(monthly_data).keys())[:5])
