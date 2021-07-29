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

def add_task(id,name,tag,deadline,time):
  con = sqlite3.connect("./contents/task.db")
  cur = con.cursor()
  cur.execute('insert into task (user_id, name, tag, deadline,day,time) values (?,?,?,?,?,?)', (id,name,tag,deadline,deadline[:10],time,))
  con.commit()
  con.close()
  return

def read_task(id):
  day_list = []
  for i in range(7):
    day_list.append((datetime.datetime.now()+datetime.timedelta(days=i+1)).strftime('%Y-%m-%d'))
  con = sqlite3.connect("./contents/task.db")
  cur = con.cursor()
  task = {"name":[],"tag":[],"deadline":[],"time":[],"day_list":day_list}
  for i in day_list:
    result =  cur.execute("SELECT * FROM task WHERE day = ? and user_id = ?;",(i,id,))
    for i in result:
      task["name"].append(i[2])
      task["tag"].append(i[3])
      task["deadline"].append(i[4])
      task["time"].append(i[6])
  con.close()
  return task

def add_setting(task):
  con = sqlite3.connect("./contents/db.db")
  cur = con.cursor()
  result =  cur.execute("SELECT * FROM setting WHERE user_id = ?;",(task[0],))
  if len(result.fetchall()) != 1:
    cur.execute('INSERT into setting (user_id, start_sleep, sleep_time, study_time, hoby_time,time_1,time_2,mornig_time,start_lunch,lunch_time,start_bath,bath_time,task_bt_time,add_tasktime,ve_1,ve_2) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',(task[0],task[1],task[2],task[3],task[4],task[5],task[6],task[7],task[8],task[9],task[10],task[11],task[12],task[13],task[14],task[15],))
  else:
    cur.execute('UPDATE setting SET user_id=?, start_sleep=?, sleep_time=?, study_time=?, hoby_time=?,time_1=?,time_2=?,mornig_time=?,start_lunch=?,lunch_time=?,start_bath=?,bath_time=?,task_bt_time=?,add_tasktime=?,ve_1=?,ve_2=? WHERE user_id = ?',(task[0],task[1],task[2],task[3],task[4],task[5],task[6],task[7],task[8],task[9],task[10],task[11],task[12],task[13],task[14],task[15],task[0],))
  con.commit()
  con.close()
  return task

def read_setting(id):
  con = sqlite3.connect("./contents/db.db")
  cur = con.cursor()
  result =  cur.execute("SELECT * FROM setting WHERE user_id = ?;",(id,))
  for i in result:
    return i