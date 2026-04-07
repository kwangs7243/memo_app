from flask import Flask, request, render_template, redirect, session
import memo
from auth import check_id_duplication, sign_up, sign_in, get_user_id
app = Flask(__name__)
app.secret_key = "memo-app-secret-key"
@app.route("/")
def index():
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/login")
    keyword = session.get("keyword")
    sort_by = session.get("sort_by", "all")
    sort_order = session.get("sort_order", "asc")
    important = session.get("important", False)
    memos = memo.get_final_memos(user_id, keyword, sort_by, sort_order, important)
    return render_template("index.html", memos = memos)
@app.route("/add", methods=["POST"])
def add_memo():
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/login")
    content = request.form.get("content")
    important = request.form.get("important") == "on"
    memo.add_memo(content, user_id, important)
    return redirect("/")
@app.route("/search", methods=["POST"])
def search_memo():
    keyword = request.form.get("keyword")
    session["keyword"] = keyword
    return redirect("/")
@app.route("/toggle-important-filter", methods=["POST"])
def toggle_important_filter():
    session["important"] = not session.get("important", False)
    return redirect("/")
@app.route("/sort", methods=["POST"])
def sort_memos():
    sort_by = request.form.get("sort_by")
    memo.set_sort_by(sort_by)
    return redirect("/")
@app.route("/reset", methods=["POST"])
def reset():
    memo.reset_status()
    return redirect("/")
@app.route("/toggle-important", methods=["POST"])
def toggle_important():
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/login")
    id = int(request.form.get("id"))
    memo.set_important(id, user_id)
    return redirect("/")
@app.route("/delete", methods=["POST"])
def delete_memo():
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/login")
    id = int(request.form.get("id"))
    memo.delete_memo(id, user_id)
    return redirect("/")
@app.route("/signup")
def signup_page():
    return render_template("signup.html")
@app.route("/signup", methods=["POST"])
def signup():
    user_id = request.form.get("user_id")
    if check_id_duplication(user_id):
        return render_template("signup.html", id_msg="이미 존재하는 아이디입니다." , user_id=user_id)
    password = request.form.get("passwd")
    sign_up(user_id, password)
    return redirect("/login")
@app.route("/login")
def login_page():
    if session.get("user_id"):
        return redirect("/")
    return render_template("login.html")
@app.route("/login", methods=["POST"])
def login():
    user_id = request.form.get("user_id")
    user_id = get_user_id(user_id)
    if not user_id:
        return render_template("login.html", login_msg="존재하지 않는 아이디입니다.", user_id=request.form.get("user_id"))
    password = request.form.get("passwd")
    if sign_in(user_id, password):
        session["user_id"] = user_id
        return redirect("/")
    else:
        return render_template("login.html", login_msg="비밀번호가 일치하지 않습니다.", user_id=request.form.get("user_id"))
@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    memo.reset_status()
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)