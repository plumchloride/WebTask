from flask import session , render_template

from contents import app


def check():
  if not session.get("logged_in"): # ログインしてない場合ログイン画面に誘導
    print("auth false")
    return (False,render_template("login.html"))
  else:
    print("auth true")
    return (True,None)