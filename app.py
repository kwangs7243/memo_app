from flask import Flask, request, render_template, redirect
from memo import MemoManager
app = Flask(__name__)
mm = MemoManager()
@app.route("/")
def index():
    memos = mm.view_memos()
    return render_template("index.html", memos = memos)
@app.route("/add", methods=["POST"])
def add_memo():
    content = request.form.get("content")
    important = request.form.get("important") == "on"
    mm.add_memo(content, important)
    return redirect("/")
@app.route("/search", methods=["POST"])
def search_memo():
    keyword = request.form.get("keyword")
    mm.set_keyword(keyword)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)