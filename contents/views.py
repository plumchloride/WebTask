from flask import request, redirect, url_for, render_template, flash, session, jsonify
from contents import app
from contents import auth
from contents import database
import random
import string

# flash用定義
app.config['JSON_AS_ASCII'] = False
app.secret_key = "".join([random.choice(string.ascii_letters + string.digits + '_' + '-' + '!' + '#' + '&')for i in range(64)])

# メイン画面での挙動
@app.route("/")
def show_entries():
  if not(auth.check()[0]):
    return auth.check()[1]
  else:
    return render_template("/auth/task.html")

# ログイン画面での挙動
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
      print(request.form["username"],"is login")
      x,y,z = database.serch_user(request.form["username"],request.form["password"])
      if x == 0:
        flash(y)
        return render_template("login.html",num=0)
      elif x == 1: #仮に同じuser_nameが2個合った場合
        flash(y)
        return render_template("login.html",num=0)
      session["logged_in"] = True # logged_inにTrueを代入
      session["user_id"] = y # user_id保存
      session["user_name"] = z # user_name保存
      return redirect(url_for("task"))
    return render_template("login.html")

# ログアウト画面での挙動
@app.route("/logout")
def logout():
  session.pop("logged_in", None) # logged_inを空にする
  session.pop("user_id", None) # user_idを空にする
  session.pop("user_name", None) # user_nameを空にする
  flash("ログアウトしました")
  return redirect(url_for("show_entries"))

@app.route("/sign-in", methods=["GET", "POST"])
def sign_in():
  if request.method == "POST":
    if request.form["password"] != request.form["password2"]:
      flash("入力したパスワードが異なります")
      return render_template("sign-in.html",num=0)
    if len(request.form["username"]) < 5:
      flash("ユーザー名は5文字以上でお願いします")
      return render_template("sign-in.html",num=0)
    if len(request.form["password"]) < 5:
      flash("パスワードは5文字以上でお願いします")
      return render_template("sign-in.html",num=0)
    x,y,z = database.add_user(request.form["username"],request.form["password"])
    if x == 0:
      flash(y)
      return render_template("sign-in.html",num=0)
    session["logged_in"] = True # logged_inにTrueを代入
    session["user_id"] = y # user_id保存
    session["user_name"] = z # user_name保存
    return redirect(url_for("task"))
  return render_template("sign-in.html")

@app.route("/auth/task")
def task():
  if not(auth.check()[0]):
    return auth.check()[1]
  else:
    return render_template("/auth/task.html",name=session["user_name"])