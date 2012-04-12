#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.shortcuts import HttpResponseRedirect
from dbkurs import util
from dbkurs.forms import OrderForm, AddCustomerForm, AddOutputForm
import psycopg2

def mainp(request):
    return render_to_response('mainpage.html')
    
def mcss(request):
    return render_to_response('main.css')
    
def customers(request):
    data = False
    if 'ctype' in request.GET: # equals if request was
        data = True
        ct=request.GET['ctype'] # what is chosen?
        if ct=='0' or ct=='2': # if 'all' have chosen
            query = "SELECT customer_id, name, "
            infoheader=['id','Name']
            if 'showopt' in request.GET: #if any checkbox is selected
                so=request.GET.getlist('showopt')
                for h in so: # for each selected checkbox
                    str_h=str(h)
                    if str_h not in('bank','account','bik','inn','okonh','okpo'):
                        query+=str_h+", "
                        infoheader.append(str(h).capitalize())
            query = query[:-2]
            if ct=='0':
                query+= " FROM customers;"
            elif ct=='2':
                query+= " FROM customers WHERE type=FALSE;"
            
        elif ct=='1':
            query = "SELECT customers.customer_id, customers.name, "
            infoheader=['id','Name']
            if 'showopt' in request.GET: #if any checkbox is selected
                so=request.GET.getlist('showopt')
                for h in so: # for each selected checkbox
                    str_h=str(h)
                    infoheader.append(str(h).capitalize())
                    if str_h not in('bank','account','bik','inn','okonh','okpo'):
                        query+="customers."+str_h+", "
                    else:
                        query+="customers_lp."+str_h+", "
            query = query[:-2]
            query+= " FROM customers RIGHT JOIN customers_lp "
            query+= " on(customers.customer_id=customers_lp.customer_id);"
            
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

def addorder(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            diagram_id = str(cd['diagram_id'])
            customer_id =str(cd['customer_id'])
            delpoint_id =str(cd['delpoint_id'])
            responsible =cd['responsible']
            output_id1 = str(cd['output_id1'])
            output_id1q = int(cd['output_id1q'])
            output_id1d = int(cd['output_id1d'])
            conn=psycopg2.connect(util.pgset())
            cur=conn.cursor()  
            
            # calculating order_amount and order_total
            squery="SELECT output_price FROM outputs "
            squery+=" WHERE output_id="+output_id1+";"
            cur.execute(squery)
            info=cur.fetchone()
            order_amount=str(int(info[0])*output_id1q)
            order_total=str(int(order_amount)*(100-output_id1d)/100)
            cur.execute("SELECT CURRENT_DATE;")
            info=cur.fetchone()
            order_date=str(info[0])
            
            query="INSERT into orders(diagram_id,customer_id,delpoint_id,"
            query+="responsible,order_date,order_amount,order_total) "
            query+=" VALUES("+diagram_id+","+customer_id+","+delpoint_id
            query+=",\'"+responsible+"\','"+order_date+"',"+order_amount+","+order_total+");"
            cur.execute(query)
            conn.commit()
            
            cur.execute("SELECT max(order_id) FROM orders")
            oid=(cur.fetchone())[0]
            
            # works only for 1 output in order
            discount=int(order_amount)-int(order_total)
            query2="INSERT into orders_outputs(order_id,output_id,quantity,discount) values"
            query2+=" ("+str(oid)+","+str(output_id1)+","+str(output_id1q)+","+str(discount)+");"
            cur.execute(query2)
            conn.commit()
            
            
            cur.close()
            conn.close()
            
            return render_to_response('thanks.html',locals())
            # use this below after DEBUD
            #return HttpResponseRedirect('thanks')
        return render_to_response('addorder.html',locals())
    else:
        form = OrderForm()
        return render_to_response('addorder.html',locals())

def addcustomer(request):
    if request.method == 'POST':
        form = AddCustomerForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            return HttpResponseRedirect('thanks')
        return render_to_response('addcustomer.html',locals())
    else:
        form = AddCustomerForm()
        return render_to_response('addcustomer.html',locals())
    
def addoutput(request):
    if request.method == 'POST':
        form = AddOutputForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            return HttpResponseRedirect('thanks')
        return render_to_response('addoutput.html',locals())
    else:
        form = AddOutputForm()
        return render_to_response('addoutput.html',locals())

def thanks(request):
    return render_to_response('thanks.html')

def ocss(request):
    return render_to_response('other.css')