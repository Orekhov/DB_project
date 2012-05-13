import psycopg2

def pgset():
    return "dbname=kurs user=manager password=123456 port=5432"

def fetchall_from_sql(query):
    conn=psycopg2.connect(pgset())
    cur=conn.cursor()
    cur.execute(query)
    info=cur.fetchall() 
    conn.commit()
    cur.close()
    conn.close()
    return info

def fetchone_from_sql(query):
    conn=psycopg2.connect(pgset())
    cur=conn.cursor()
    cur.execute(query)
    info=cur.fetchone() 
    conn.commit()
    cur.close()
    conn.close()
    return info

def execute_sql(query):
    conn=psycopg2.connect(pgset())
    cur=conn.cursor()
    cur.execute(query)
    conn.commit()
    cur.close()
    conn.close()

def simpleSqlCheck(query):
    if query.count(';') == 1:
        return True
    else:
        return False