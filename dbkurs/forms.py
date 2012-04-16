#!/usr/bin/python
# -*- coding: utf-8 -*-
from django import forms
from dbkurs import util
import psycopg2

class OrderForm(forms.Form):
    conn=psycopg2.connect(util.pgset())
    cur=conn.cursor()
    reqmes='Поле не должно быть пустым'
    maxmes='Значение выше допустимого'
    minmes='Значение ниже допустимого'
    nummes='Это поле заполнено неверно'
    
    query = "SELECT diagram_id,vehicle,agent,plan_date FROM delivery_diagrams "
    query+= " WHERE status=false ORDER BY plan_date asc;"
    cur.execute(query)
    info=cur.fetchall()
    info_ok= [(0,'Выберите график доставки'),]
    for el in info:
        v=str(el[3])+" - "+el[1]+" - "+el[2]
        info_ok.append((el[0],v),)
    diagram_id = forms.ChoiceField(label='График доставки',choices=info_ok)
    
    query = "SELECT customer_id,name FROM customers ORDER BY name asc;"
    cur.execute(query)
    info=cur.fetchall()
    info_ok= [(0,'Выберите клиента'),]
    for el in info:
        info_ok.append((el[0],el[1]),)
    customer_id = forms.ChoiceField(label='Клиент',choices=info_ok)

    query = "SELECT delpoint_id,del_address FROM delpoints ORDER BY del_address asc;"
    cur.execute(query)
    info=cur.fetchall()
    info_ok= [(0,'Выберите пункт доставки'),]
    for el in info:
        info_ok.append((el[0],el[1]),)
    delpoint_id = forms.ChoiceField(label='Пункт доставки',choices=info_ok)
    
    responsible = forms.CharField(label='Ответственный менеджер',error_messages={'required': reqmes})
    
    query = "SELECT output_id,output_name FROM outputs ORDER BY output_name asc;"
    cur.execute(query)
    outputs=cur.fetchall()
    outputs_ok = [(0,'Выберите товар'),]
    for el in outputs:
        outputs_ok.append((el[0],el[1]),)
    #ch=[('M','Male'),('F','Female')]
    output_id1 = forms.ChoiceField(label='Товар 1',choices=outputs_ok)
    output_id1q= forms.IntegerField(label='Количество, шт',
                                    error_messages={'required':reqmes,'min_value':minmes,'max_value':maxmes,'invalid': nummes},
                                    min_value=1,max_value=51)
    output_id1d= forms.IntegerField(label='Скидка, %',
                                    error_messages={'required': reqmes,'min_value':minmes,'max_value':maxmes,'invalid': nummes},
                                    min_value=0,max_value=90)
    
    conn.commit()
    cur.close()
    conn.close()
    
    # is invoked automatically by Django because of it starts with clean_
    # when form.is_valid() is invoked
    def clean_diagram_id(self):
        di=self.cleaned_data['diagram_id']
        if di=='0':
            raise forms.ValidationError("График не выбран")
        return di
    
    def clean_customer_id(self):
        ci=self.cleaned_data['customer_id']
        if ci=='0':
            raise forms.ValidationError("Клиент не выбран")
        return ci
        
    def clean_delpoint_id(self):
        di=self.cleaned_data['delpoint_id']
        if di=='0':
            raise forms.ValidationError("Пункт не выбран")
        return di
    
    def clean_output_id1(self):
        oi=self.cleaned_data['output_id1']
        if oi=='0':
            raise forms.ValidationError("Товар не выбран")
        return oi
    
    def clean_responsible(self):
        ri=self.cleaned_data['responsible']
        if (';' in ri)or(')' in ri)or(',' in ri):
            raise forms.ValidationError("Недопустимые символы")
        return ri
        
        
class AddCustomerForm(forms.Form):
    conn=psycopg2.connect(util.pgset())
    cur=conn.cursor()
    reqmes='Поле не должно быть пустым'
    nummes='Это поле заполнено неверно'
    name = forms.CharField(label='Имя',error_messages={'required':reqmes })
    address = forms.CharField(label='Адрес',error_messages={'required': reqmes})
    phone = forms.CharField(label='Телефон',error_messages={'required': reqmes})
    fax = forms.CharField(label='Факс',error_messages={'required': reqmes})
    email = forms.CharField(label='E-mail',error_messages={'required': reqmes})
    type = forms.ChoiceField(label='Тип',choices=[('1','Физическое лицо'),('2','Юридическое лицо')])

    bank = forms.CharField(label='Банк',required=False)
    account = forms.IntegerField(label='Аккаунт',required=False,error_messages={'invalid': nummes})
    bik = forms.IntegerField(label='БИК',required=False,error_messages={'invalid': nummes})
    inn = forms.IntegerField(label='ИНН',required=False,error_messages={'invalid': nummes})
    okonh = forms.IntegerField(label='ОКОНХ',required=False,error_messages={'invalid': nummes})
    okpo = forms.IntegerField(label='ОКПО',required=False,error_messages={'invalid': nummes})
    
    
class AddOutputForm(forms.Form):
    conn=psycopg2.connect(util.pgset())
    cur=conn.cursor()
    reqmes='Поле не должно быть пустым'
    output_name = forms.CharField(label='Название',error_messages={'required':reqmes })
    output_price = forms.IntegerField(label='Стоимость',error_messages={'required': reqmes})