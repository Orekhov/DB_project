from django.shortcuts import render_to_response
import psycopg2

def mainp(request):
    return render_to_response('mainpage.html')
    
def mcss(request):
    return render_to_response('main.css')
    
def customers(request):
    data = False
    conn=psycopg2.connect("dbname=kurs user=postgres password=abc678 port=5432")
    cur=conn.cursor()
    
    if 'ctype' in request.GET:
        ct=request.GET['ctype']
        if ct=='0':
            # if 'ALL' chosen
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
            query+= " FROM customers;"
            #query = "SELECT * FROM customers;" # use this if trouble
            cur.execute(query)
            info=cur.fetchall()
            #infoheader=info[0]
        elif ct=='1':
            # if 'legal persons' have been chosen
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
            query+= " FROM customers WHERE type=FALSE;"
            #query="SELECT * FROM customers WHERE type=FALSE;"
            cur.execute(query)
            info=cur.fetchall()
        elif ct=='2':
            # if 'natural persons' have been chosen
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
            query+= " FROM customers WHERE type=TRUE;"
            #query="SELECT * FROM customers WHERE type=TRUE;"
            cur.execute(query)
            info=cur.fetchall()          
    conn.commit()
    cur.close()
    conn.close()
    return render_to_response('customers.html',locals())

def outputs(request):
    data = False
    infoheader=['id','Name','Price']
    conn=psycopg2.connect("dbname=kurs user=postgres password=abc678 port=5432")
    cur=conn.cursor()
    
    if 'ctype' in request.GET:
        data = True
        ct=request.GET['ctype']
        if ct=='0':
            query = "SELECT output_id, output_name, output_price FROM outputs;"
            cur.execute(query)
            info=cur.fetchall() 
        elif ct=='1':
            query = "SELECT output_id, output_name, output_price FROM outputs ORDER BY output_name;"
            cur.execute(query)
            info=cur.fetchall() 
        elif ct=='2':
            query = "SELECT output_id, output_name, output_price FROM outputs ORDER BY output_price;"
            cur.execute(query)
            info=cur.fetchall() 
    
    conn.commit()
    cur.close()
    conn.close()
    return render_to_response('outputs.html',locals())
    
def ocss(request):
    return render_to_response('other.css')