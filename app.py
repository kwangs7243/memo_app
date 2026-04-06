from flask import Flask, request, render_template, redirect
from memo import MemoManager
from auth import check_id_duplication, sign_up, sign_in, get_user_id
app = Flask(__name__)
mm = MemoManager()
@app.route("/")
def index():
    memos = mm.get_final_memos()
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
@app.route("/toggle-important-filter", methods=["POST"])
def toggle_important_filter():
    mm.set_status_important()
    return redirect("/")
@app.route("/sort", methods=["POST"])
def sort_memos():
    sort_by = request.form.get("sort_by")
    mm.set_sort_by(sort_by)
    return redirect("/")
@app.route("/reset", methods=["POST"])
def reset():
    mm.reset_status()
    return redirect("/")
@app.route("/toggle-important", methods=["POST"])
def toggle_important():
    id = int(request.form.get("id"))
    mm.set_important(id)
    return redirect("/")
@app.route("/delete", methods=["POST"])
def delete_memo():
    id = int(request.form.get("id"))
    mm.delete_memo(id)
    return redirect("/")
@app.route("/reset-all", methods=["POST"])
def reset_memos():
    mm.reset_memos()
    mm.reset_status()
    return redirect("/")
@app.route("/signup", methods=["POST"])
def signup():
    user_id = request.form.get("user_id")
    if check_id_duplication(user_id):
        return
    password = request.form.get("password")
    sign_up(user_id, password)
    return redirect("/login")
@app.route("/login", methods=["POST"])
def login():
    user_id = request.form.get("user_id")
    password = request.form.get("password")
    if sign_in(user_id, password):
        user_id = get_user_id(user_id)
        mm.set_user_id(user_id)
        return redirect("/")
    else:
        return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True)