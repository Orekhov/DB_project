from django.shortcuts import render_to_response
from dbkurs import util
import psycopg2

def mainp(request):
    return render_to_response('mainpage.html')
    
def mcss(request):
    return render_to_response('main.css')
    
def customers(request):
    data = False
    if 'ctype' in request.GET:
        data = True
        query = "SELECT customer_id, name, "
        infoheader=['id','Name']
        if 'showopt' in request.GET:
            so=request.GET.getlist('showopt')
            for h in so:
                query+=str(h)
                infoheader.append(str(h).capitalize())
                query+=", "
        query = query[:-2]
        ct=request.GET['ctype']
        if ct=='0':
            query+= " FROM customers;"
        elif ct=='1':
            query+= " FROM customers WHERE type=FALSE;"
        elif ct=='2':
            query+= " FROM customers WHERE type=TRUE;"
        conn=psycopg2.connect(util.pgset())
        cur=conn.cursor()
        cur.execute(query)
        info=cur.fetchall()        
        conn.commit()
        cur.close()
        conn.close()
    return render_to_response('customers.html',locals())

def outputs(request):
    data = False
    if 'ctype' in request.GET:
        data = True
        infoheader=['id','Name','Price']
        query = "SELECT output_id, output_name, output_price FROM outputs"
        ct=request.GET['ctype']
        if ct=='0':
            query += " ORDER BY output_id"
        elif ct=='1':
            query += " ORDER BY output_name"
        elif ct=='2':
            query += " ORDER BY output_price"
        ot=request.GET['ordertype']
        if ot=='0':
            query += " desc;"
        elif ot == '1':
            query += " asc;"
        conn=psycopg2.connect(util.pgset())
        cur=conn.cursor()
        cur.execute(query)
        info=cur.fetchall()
        conn.commit()
        cur.close()
        conn.close()
    return render_to_response('outputs.html',locals())
    
def notdelivered (request): 
    infoheader=['Order','Responsible','Vehicle','Agent','Plan date']
    query = "select a.order_id,a.responsible,b.vehicle,b.agent,b.plan_date "
    query+= "from orders a inner join delivery_diagrams b "
    query+= "on (a.diagram_id=b.diagram_id and b.status=false);"
    conn=psycopg2.connect(util.pgset())
    cur=conn.cursor()
    cur.execute(query)
    info=cur.fetchall() 
    conn.commit()
    cur.close()
    conn.close()
    return render_to_response('notdelivered.html',locals())

def orders(request):
    infoheader=['Order','Customer','Responsible','Order Date','Amount','Total']
    query = "select order_id,customer_id,responsible,order_date,order_amount,order_total "
    query+= "from orders;"
    conn=psycopg2.connect(util.pgset())
    cur=conn.cursor()
    cur.execute(query)
    info=cur.fetchall() 
    conn.commit()
    cur.close()
    conn.close()
    return render_to_response('orders.html',locals())

def ocss(request):
    return render_to_response('other.css')