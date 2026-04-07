from flask import Flask, request, render_template, redirect, session
from memo import MemoManager
from auth import check_id_duplication, sign_up, sign_in, get_user_id
app = Flask(__name__)
app.secret_key = "memo-app-secret-key"
mm = MemoManager()
@app.route("/")
def index():
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/login")
    mm.set_user_id(user_id)
    memos = mm.get_final_memos()
    return render_template("index.html", memos = memos)
@app.route("/add", methods=["POST"])
def add_memo():
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/login")
    mm.set_user_id(user_id)
    content = request.form.get("content")
    important = request.form.get("important") == "on"
    mm.add_memo(content, important)
    return redirect("/")
@app.route("/search", methods=["POST"])
def search_memo():
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/login")
    mm.set_user_id(user_id)
    keyword = request.form.get("keyword")
    mm.set_keyword(keyword)
    return redirect("/")
@app.route("/toggle-important-filter", methods=["POST"])
def toggle_important_filter():
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/login")
    mm.set_user_id(user_id)
    mm.set_status_important()
    return redirect("/")
@app.route("/sort", methods=["POST"])
def sort_memos():
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/login")
    mm.set_user_id(user_id)
    sort_by = request.form.get("sort_by")
    mm.set_sort_by(sort_by)
    return redirect("/")
@app.route("/reset", methods=["POST"])
def reset():
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/login")
    mm.set_user_id(user_id)
    mm.reset_status()
    return redirect("/")
@app.route("/toggle-important", methods=["POST"])
def toggle_important():
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/login")
    mm.set_user_id(user_id)
    id = int(request.form.get("id"))
    mm.set_important(id)
    return redirect("/")
@app.route("/delete", methods=["POST"])
def delete_memo():
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/login")
    mm.set_user_id(user_id)
    id = int(request.form.get("id"))
    mm.delete_memo(id)
    return redirect("/")
@app.route("/reset-all", methods=["POST"])
def reset_view():
    user_id = session.get("user_id")
    if not user_id:     
        return redirect("/login")
    mm.set_user_id(user_id)
    mm.reset_status()
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
    mm.reset_status()
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)