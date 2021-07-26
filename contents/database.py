import sqlite3

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
  # cur.execute("select id from user;")
  # id_num = []
  # for i in cur:
  #   id_num.append(i[0])
  # id = max(id_num) +1
  # cur.execute('insert into user (id,name, pass) values (?,?,?)', (id,name,password,))
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