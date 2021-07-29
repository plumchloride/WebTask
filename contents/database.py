import sqlite3
import datetime

def serch_user(name,password):
  con = sqlite3.connect("./contents/db.db")
  cur = con.cursor()
  result =  cur.execute("SELECT * FROM user WHERE name = ?;",(name,))
  if len(result.fetchall()) == 0:
    con.close()
    return (0,"ユーザー名が違います",None)
  elif len(result.fetchall()) > 1:
    con.close()
    return (1,"予期しないエラー,error:1",None)
  result =  cur.execute("SELECT * FROM user WHERE name = ?;",(name,))
  for i in result:
    if i[2] == password:
      con.close()
      return (2,i[0],i[1])

def add_user(name,password):
  con = sqlite3.connect("./contents/db.db")
  cur = con.cursor()
  result =  cur.execute("SELECT * FROM user WHERE name = ?;",(name,))
  if len(result.fetchall()) != 0:
    con.close()
    return (0,"すでに登録されたユーザー名です",None)
  cur.execute('insert into user (name, pass) values (?,?)', (name,password,))
  con.commit()
  result =  cur.execute("SELECT * FROM user WHERE name = ?;",(name,))
  if len(result.fetchall()) != 1:
    con.close()
    return (0,"予期しないエラー,error:2",None)
  result =  cur.execute("SELECT * FROM user WHERE name = ?;",(name,))
  for i in result:
    if i[2] == password:
      con.close()
      return (2,i[0],i[1])

def add_task(id,name,tag,deadline):
  con = sqlite3.connect("./contents/task.db")
  cur = con.cursor()
  cur.execute('insert into task (user_id, name, tag, deadline,day) values (?,?,?,?,?)', (id,name,tag,deadline,deadline[:10]))
  con.commit()
  con.close()
  return

def read_task(id):
  day_list = []
  for i in range(7):
    day_list.append((datetime.datetime.now()+datetime.timedelta(days=i+1)).strftime('%Y-%m-%d'))
  print(day_list)
  con = sqlite3.connect("./contents/task.db")
  cur = con.cursor()
  task = {"name":[],"tag":[],"deadline":[]}
  for i in day_list:
    result =  cur.execute("SELECT * FROM task WHERE day = ? and user_id = ?;",(i,id,))
    for i in result:
      task["name"].append(i[2])
      task["tag"].append(i[3])
      task["deadline"].append(i[4])
  con.close()
  print(task)
  return task