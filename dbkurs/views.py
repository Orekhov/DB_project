from django.shortcuts import render_to_response
import psycopg2

def mainp(request):
    return render_to_response('mainpage.html')
    
def mcss(request):
    return render_to_response('main.css')
    
def clients(request):
    data = False
    conn=psycopg2.connect("dbname=kurs user=postgres password=abc678 port=5432")
    cur=conn.cursor()
    
    if 'ctype' in request.GET:
        ct=request.GET['ctype']
        if ct=='0':
            data = True
            #query = "SELECT * FROM customers;"
            query = "SELECT customer_id, name, "
            if 'showopt' in request.GET:
                so=request.GET.getlist('showopt')
                for h in so:
                    query+=str(h)
                    query+=", "
            query = query[:-2]
            query+= " FROM customers;"
            cur.execute(query)
            info=cur.fetchall()
        elif ct=='1':
            data = True
            cur.execute("SELECT * FROM customers WHERE type=FALSE;")
            info=cur.fetchall()
        elif ct=='2':
            data = True
            cur.execute("SELECT * FROM customers WHERE type=TRUE;")
            info=cur.fetchall()          
    conn.commit()
    cur.close()
    conn.close()
    return render_to_response('clients.html',locals())
    
def ocss(request):
    return render_to_response('other.css')