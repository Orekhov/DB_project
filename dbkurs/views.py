#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.shortcuts import HttpResponseRedirect
from django.http import HttpResponse, HttpResponseBadRequest
from dbkurs import util
from dbkurs.forms import AddOrderForm, AddCustomerForm, AddOutputForm, AddDelpointForm, DelivOrderForm, CustomersForm

def mainp(request):
    return render_to_response('mainpage.html')
    
def mcss(request):
    return render_to_response('main.css')
    
def customers_old(request):
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
                query+= " FROM customers WHERE type=TRUE;"
            
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
            
        info=util.fetchall_from_sql(query)
    return render_to_response('customers.html',locals())

def customers(request):
    data=False
    if request.method == 'GET':
        data=True
        form = CustomersForm(request.GET)
        if form.is_valid():
            cd = form.cleaned_data
            type  = str(cd['type'])
            address  = cd['address']
            phone  = cd['phone']
            fax  = cd['fax']
            email  = cd['email']
            bank  = cd['bank']
            account  = cd['account']
            bik  = cd['bik']
            inn  = cd['inn']
            okonh  = cd['okonh']
            okpo  = cd['okpo']
            if type=='0' or type=='2': # if 'all' have chosen
                query = "SELECT customer_id, name, "
                infoheader=['Номер','Имя']
                if address: query+="address, ";infoheader.append('Адрес')
                if phone: query+="phone, ";infoheader.append('Телефон')
                if fax: query+="fax, ";infoheader.append('Факс')
                if email: query+="email, ";infoheader.append('Email')
                query = query[:-2]
                if type=='0':
                    query+= " FROM customers;"
                elif type=='2':
                    query+= " FROM customers WHERE type=TRUE;"
            elif type=='1':
                query = "SELECT customers.customer_id, customers.name, "
                infoheader=['Номер','Имя']
                if address: query+="customers.address, ";infoheader.append('Адрес')
                if phone: query+="customers.phone, ";infoheader.append('Телефон')
                if fax: query+="customers.fax, ";infoheader.append('Факс')
                if email: query+="customers.email, ";infoheader.append('Email')
                if bank: query+="customers_lp.bank, ";infoheader.append('Банк')
                if account: query+="customers_lp.account, ";infoheader.append('Счёт')
                if bik: query+="customers_lp.bik, ";infoheader.append('БИК')
                if inn: query+="customers_lp.inn, ";infoheader.append('ИНН')
                if okonh: query+="customers_lp.okonh, ";infoheader.append('ОКОНХ')
                if okpo: query+="customers_lp.okpo, ";infoheader.append('ОКПО')
                query = query[:-2]
                query+= " FROM customers RIGHT JOIN customers_lp "
                query+= " on(customers.customer_id=customers_lp.customer_id);"
            if type in ('0','1','2'):
                info=util.fetchall_from_sql(query)
            return render_to_response('customers.html',locals())
        return render_to_response('customers.html',locals())
    else:
        form = CustomersForm()
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
        info=util.fetchall_from_sql(query)
    return render_to_response('outputs.html',locals())
    
def notdelivered (request): 
    infoheader=['Номер','План. дата','Заказ','Ответственный','Транспортное средство','Агент']
    query = "select a.order_id, b.plan_date,(select string_agg(y.output_name||' - '||x.quantity||'шт.',',  ') as output "
    query+=" from orders_outputs x inner join outputs y on x.output_id=y.output_id where x.order_id=a.order_id "
    query+=" group by x.order_id), a.responsible, b.vehicle, b.agent from orders a "
    query+=" inner join delivery_diagrams b on a.diagram_id=b.diagram_id and b.status=false "
    query+=" order by b.plan_date asc;"
    info=util.fetchall_from_sql(query)
    return render_to_response('notdelivered.html',locals())

def orders(request):
    infoheader=['Заказ','Клиент','Ответственный','Дата заказа','Сумма','Итого (со скидкой)']
    query = "select order_id,customer_id,responsible,order_date,order_amount,order_total "
    query+= "from orders;"
    info=util.fetchall_from_sql(query)
    return render_to_response('orders.html',locals())

def addorder(request):
    if request.method == 'POST':
        form = AddOrderForm(request.POST)
        form.updateNonStaticFields()
        if form.is_valid():
            # getting data from forms
            cd = form.cleaned_data
            customer_id =str(cd['customer_id'])
            delpoint_id =str(cd['delpoint_id'])
            responsible =cd['responsible']
            vehicle =cd['vehicle']
            agent =cd['agent']
            plan_date =str(cd['plan_date'])
            output_id1 = str(cd['output_id1'])
            output_id1q = int(cd['output_id1q'])
            output_id1d = int(cd['output_id1d'])
    
            # calculating order_amount and order_total
            squery="SELECT output_price FROM outputs "
            squery+=" WHERE output_id="+output_id1+";"
            info=util.fetchone_from_sql(squery)
            order_amount=str(int(info[0])*output_id1q)
            order_total=str(int(order_amount)*(100-output_id1d)/100)
            
            # calculating current date
            info=util.fetchone_from_sql("SELECT CURRENT_DATE;")
            order_date=str(info[0])
            
            # inserting new delivery_diagram row
            query= " INSERT into delivery_diagrams (vehicle,agent,plan_date,status) "
            query+=" VALUES ('"+vehicle+"','"+agent+"','"+plan_date+"',False);" 
            if util.simpleSqlCheck(query):
                util.execute_sql(query)
            else:
                return HttpResponseBadRequest(content='<b>Error 400</b><br><br>Bad Request')
            
            # getting new diagram_id from delivery_diagrams
            dat=util.fetchone_from_sql("SELECT max(diagram_id) FROM delivery_diagrams;")
            diagram_id=str(dat[0])
            
            # inserting new order row
            query2="INSERT into orders(diagram_id,customer_id,delpoint_id,"
            query2+="responsible,order_date,order_amount,order_total) "
            query2+=" VALUES("+diagram_id+","+customer_id+","+delpoint_id
            query2+=",\'"+responsible+"\','"+order_date+"',"+order_amount+","+order_total+");"
            if util.simpleSqlCheck(query2):
                util.execute_sql(query2)
            else:
                return HttpResponseBadRequest(content='<b>Error 400</b><br><br>Bad Request')
            
            # getting new order_id from orders
            dat=util.fetchone_from_sql("SELECT max(order_id) FROM orders;")
            oid=dat[0]
            
            # inserting new order_output row
            discount=int(order_amount)-int(order_total)
            query3="INSERT into orders_outputs(order_id,output_id,quantity,discount) values"
            query3+=" ("+str(oid)+","+str(output_id1)+","+str(output_id1q)+","+str(discount)+");"
            if util.simpleSqlCheck(query3):
                util.execute_sql(query3)
            else:
                return HttpResponseBadRequest(content='<b>Error 400</b><br><br>Bad Request')
            return HttpResponseRedirect('thanks')
        return render_to_response('addorder.html',locals())
    else:
        form = AddOrderForm()
        form.updateNonStaticFields()
        return render_to_response('addorder.html',locals())    

def addcustomer(request):
    if request.method == 'POST':
        form = AddCustomerForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            name    = cd['name']
            address = cd['address']
            phone   = cd['phone']
            fax     = cd['fax']
            email   = cd['email']
            type    = int(cd['type'])
            if type ==2:
                bank    = cd['bank']
                account = str(cd['account'])
                bik     = str(cd['bik'])
                inn     = str(cd['inn'])
                okonh   = str(cd['okonh'])
                okpo    = str(cd['okpo'])
                type="False"
            elif type==1:
                type="True"
                
            query="INSERT INTO customers (name,address,phone,fax,email,type) "
            query+=" VALUES ('"+name+"','"+address+"','"+phone+"','"+fax+"','"+email+"',"+type+");"
            if util.simpleSqlCheck(query):
                util.execute_sql(query)
            else:
                return HttpResponseBadRequest(content='<b>Error 400</b><br><br>Bad Request')
            if type=="False":
                dat=util.fetchone_from_sql("SELECT max(customer_id) FROM customers;")
                new_customer_id=dat[0]
                query2 ="INSERT INTO customers_lp (customer_id,bank,account,bik,inn,okonh,okpo) "
                query2+=" VALUES ("+str(new_customer_id)+",'"+bank+"',"+account+","+bik+","+inn+","+okonh+","+okpo+");"
                if util.simpleSqlCheck(query2):
                    util.execute_sql(query2)
                else:
                    return HttpResponseBadRequest(content='<b>Error 400</b><br><br>Bad Request')
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
            output_name  = cd['output_name']
            output_price = str(cd['output_price'])
            query =" INSERT INTO outputs (output_name,output_price) "
            query+=" VALUES ('"+output_name+"',"+output_price+");"
            if util.simpleSqlCheck(query):
                util.execute_sql(query)
            else:
                return HttpResponseBadRequest(content='<b>Error 400</b><br><br>Bad Request')
            return HttpResponseRedirect('thanks')
        return render_to_response('addoutput.html',locals())
    else:
        form = AddOutputForm()
        return render_to_response('addoutput.html',locals())

def customer(request,customer_id):
    data=False
    data2=False
    try: # int or not
        customer_id=int(customer_id)
    except ValueError:
        raise Http404()
    data=True
    customer_id=str(customer_id)
    query="SELECT type FROM customers WHERE customer_id="+customer_id+";"
    dat=util.fetchone_from_sql(query)
    element=dat[0]
    infoheader1=['Номер','Имя/Название','Адрес','Телефон','Факс','Электронная почта']
    if element: # if it is natural person
        query2 ="SELECT customer_id,name,address,phone,fax,email "
        query2+=" FROM customers WHERE customer_id="+customer_id+";"
    else:
        data2=True
        infoheader2=['Название банка','Счёт','БИК','ИНН','ОКОНХ','ОКПО']
        query2 ="SELECT a.customer_id,a.name,a.address,a.phone,a.fax,a.email,"
        query2+="b.bank,b.account,b.bik,b.inn,b.okonh,b.okpo "
        query2+=" FROM customers a RIGHT JOIN customers_lp b"
        query2+=" on(a.customer_id=b.customer_id) "
        query2+=" WHERE a.customer_id="+customer_id+";"
    customerdata=util.fetchone_from_sql(query2)
    customerdata1=customerdata[0:6]
    customerdata2=customerdata[6:12]
    return render_to_response('customer.html',locals())

def order(request,order_id):
    data=False
    try: # int or not
        order_id=int(order_id)
    except ValueError:
        raise Http404()
    data=True
    order_id=str(order_id)
    query ="select a.order_id,a.customer_id,a.responsible,a.order_date,a.order_amount,a.order_total, "
    query+=" b.diagram_id,b.vehicle,b.agent,b.plan_date,b.status,b.fact_date, "
    query+=" c.delpoint_id,c.del_address,c.zone,c.floor,c.elevator,c.entrance,c.code "
    query+=" from orders a left join delivery_diagrams b on (a.diagram_id=b.diagram_id) "
    query+=" left join delpoints c on (a.delpoint_id=c.delpoint_id) "
    query+=" where order_id="+order_id+";"
    infoheader1=['Номер','Клиент','Ответственный менеджер','Дата заказа','Цена без скидки','Цена со скидкой']
    infoheader2=['Номер графика доставки','Транспортное средство','Агент','Планируемая дата доставки',
                'Статус доставки','Фактическая дата доставки']
    infoheader3=['Номер пункта доставки','Адрес','Зона','Этаж','Наличие лифта','Номер парадной','Входной код']
    orderdata=util.fetchone_from_sql(query)
    orderdata=list(orderdata)
    if orderdata[10] == True:
        orderdata[10]='Доставлен'
    elif orderdata[10] == False:
        orderdata[10]='Не доставлен'
    if orderdata[16] == True:
        orderdata[16]='Есть'
    elif orderdata[16] == False:
        orderdata[16]='Нет'
    orderdata1=orderdata[0:6]
    orderdata2=orderdata[6:12]
    orderdata3=orderdata[12:19]
    return render_to_response('order.html',locals())

def adddelpoint(request):
    if request.method == 'POST':
        form = AddDelpointForm(request.POST)
        if form.is_valid():
            # getting data from forms
            cd = form.cleaned_data
            del_address= cd['del_address']
            zone       = cd['zone']
            floor      = cd['floor']
            elevator   = int(cd['elevator'])
            entrance   = cd['entrance']
            code       = cd['code']
            if elevator ==2:
                elevator="False"
            elif elevator==1:
                elevator="True" 
            
            # calculating order_amount and order_total
            query="INSERT INTO delpoints (del_address,zone,floor,elevator,entrance,code) "
            query+=" VALUES ('"+del_address+"','"+zone+"','"+floor+"',"+elevator+",'"+entrance+"','"+code+"');"
            if util.simpleSqlCheck(query):
                util.execute_sql(query)
            else:
                return HttpResponseBadRequest(content='<b>Error 400</b><br><br>Bad Request')
            return HttpResponseRedirect('thanks')
        return render_to_response('adddelpoint.html',locals())
    else:
        form = AddDelpointForm()
        return render_to_response('adddelpoint.html',locals())
    
def delivorder(request):
    if request.method == 'POST':
        form = DelivOrderForm(request.POST)
        form.updateNonStaticForm()
        if form.is_valid():
            cd = form.cleaned_data
            delivering_order  = str(cd['delivering_order'])
            query =" UPDATE delivery_diagrams SET status=True, fact_date=CURRENT_TIMESTAMP "
            query+=" WHERE diagram_id=(SELECT diagram_id FROM orders WHERE order_id="+delivering_order+");"
            if util.simpleSqlCheck(query):
                util.execute_sql(query)
            else:
                return HttpResponseBadRequest(content='<b>Error 400</b><br><br>Bad Request')
            return HttpResponseRedirect('thanks')
        return render_to_response('delivorder.html',locals())
    else:
        form = DelivOrderForm()
        form.updateNonStaticForm()
        return render_to_response('delivorder.html',locals())
    
def delivorderdirectly(request):
    if 'order_to_deliver' in request.POST:
        otd=request.POST['order_to_deliver']
        otd=str(otd).strip()
        query =" UPDATE delivery_diagrams SET status=True, fact_date=CURRENT_TIMESTAMP "
        query+=" WHERE diagram_id=(SELECT diagram_id FROM orders WHERE order_id="+otd+");"
        if util.simpleSqlCheck(query):
            util.execute_sql(query)
            return HttpResponse('заказ '+otd+' доставлен')
    return HttpResponse('Не доставлено')

def thanks(request):
    return render_to_response('thanks.html')

def ocss(request):
    return render_to_response('other.css')

def jquery(request):
    return render_to_response('jquery.js')