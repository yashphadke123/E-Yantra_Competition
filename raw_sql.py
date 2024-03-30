import pymysql 
import time
from fastapi import HTTPException,status


def connect(host,name,pss,db):
    while(True):
        try:
            my_conn = pymysql.connect(host=host,user=name,password=pss,database=db)
            print("Database Connection Successful")
            return my_conn
            break
        except Exception as e:
            print("Database Connection Failed")
            print("Error:",e)
            time.sleep(2)

class get():
    def get_all_posts(lst,table):
        conn = lst.cursor(pymysql.cursors.DictCursor)
        query = "SELECT * FROM {}".format(table)
        conn.execute(query)
        rows = conn.fetchall()
        return rows

    
    def get_one_post(lst,table,id,user):
        conn = lst.cursor(pymysql.cursors.DictCursor)
        query = "SELECT * FROM {} WHERE id ={};".format(table,id)
        conn.execute(query)
        post = conn.fetchone()
        lst.commit() 
        if type(post) == dict:
            email = post.get("user_email")
        elif post == None:
            return []
        if user != email: 
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Unauthorised")
        return post

class post():
    def single_element(lst,cols,vals,table):
        i = 1
        val_s = str(vals[0])
        col_s = cols[0]
        while i < len(vals):
         if type(vals[i] == str):
             val_curr = "'" + str(vals[i]) +"'"
         elif type(vals[i] == int):
             val_curr = str(vals[i])
         val_s += "," + val_curr
         col_s += "," + cols[i]
         i += 1
        conn = lst.cursor(pymysql.cursors.DictCursor)
        query ="INSERT INTO {}({}) VALUES({});".format(table,col_s,val_s)
        conn.execute(query)
        lst.commit()
        return "successfully uploaded"

class delete():
    def delete_id(lst,table,id,email):
        conn = lst.cursor(pymysql.cursors.DictCursor)
        get_quer = "SELECT * FROM {} WHERE id ={};".format(table,id)
        conn.execute(get_quer)
        dic = conn.fetchone()
        if dic.get("user_email") == email:
            del_query = "DELETE FROM {} WHERE id = {};".format(table,id)
            conn.execute(del_query)
            post = conn.fetchall()
            lst.commit() 
            return post
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Incorrect Email")

class update:
    def updating(lst,inputs,table,email):
        temp = []
        conn = lst.cursor(pymysql.cursors.DictCursor)
        for ins in inputs:
            if type(ins) == str:
                ins = "'"+ins+"'"
            elif type(ins) == int:
                ins = ins
            temp.append(ins)
        get_quer = "SELECT * FROM {} WHERE id ={};".format(table,temp[2])
        conn.execute(get_quer)
        dic = conn.fetchone()
        if dic.get("user_email") == email:
            up_query = "UPDATE {} SET title={},content={} WHERE id={}".format(table,temp[0],temp[1],temp[2])
            conn.execute(up_query)
            post = conn.fetchall()
            lst.commit() 
            return post
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Incorrect Email")


class verify:
    def login_check(lst,id):
        email = "'"+id+"'"
        conn = lst.cursor(pymysql.cursors.DictCursor)
        query = "SELECT password FROM users WHERE email={};".format(email)
        conn.execute(query)
        code = conn.fetchone()
        if code == None:
            code = "teri maa ki chut"
        return code

def like(lst,id,email):
    email = "'" + email + "'"
    conn = lst.cursor(pymysql.cursors.DictCursor)
    print(email)
    query = "INSERT INTO likes (email,post_id) VALUES({},{})".format(email,id)
    conn.execute(query)
    seach_query = "SELECT * FROM likes"
    conn.execute(seach_query)
    code = conn.fetchall()
    return code