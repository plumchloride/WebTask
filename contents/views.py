from flask import request, redirect, url_for, render_template, flash, session, jsonify
from contents import app
from contents import auth
from contents import database
import random
import string
import datetime

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
    tasks = database.read_task(session["user_id"])
    nums = []
    for i in range(len(tasks["name"])):
      nums.append(i)
    return render_template("/auth/task.html",task_names = tasks["name"],tags=tasks["tag"],deadline_days = tasks["deadline"],deadline_times = tasks["deadline"],time=tasks["time"],index = nums)

@app.route("/task", methods=["GET","POST"])
def task_get():
  if not(auth.check()[0]):
    return auth.check()[1]
  else:
    if request.method == "GET":
      return redirect(url_for("task"))
    database.add_task(session["user_id"],request.form["Name"],request.form["Tag"],request.form["Deadline"],request.form["time"])
    return redirect(url_for("task"))
@app.route("/user", methods=["GET","POST"])
def user():
  if not(auth.check()[0]):
    return auth.check()[1]
  else:
    if request.method == "POST":
      if request.form["cut_time_1"] == request.form["cut_time_2"]:
        f_text = "削るカテゴリーについては1と2で別の物を選択してください"
      if request.form["sleep_time"] +request.form["study_time"]+request.form["hoby_time"]+request.form["cut_time_1"]+request.form["cut_time_1"]+request.form["morning_time"]+request.form["lunch_time"]+request.form["bath_time"] > 1440:
        f_text = "一日の睡眠・自習・娯楽・昼休憩・夜飯の時間の和は1440分(24時間)未満にしてください"
      setting = []
    if request.method == "GET":
      f_text = ""
    return render_template("/auth/user.html",name=session["user_name"],flash_hand=f_text)