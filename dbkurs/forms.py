#!/usr/bin/python
# -*- coding: utf-8 -*-
from django import forms
from dbkurs import util
import psycopg2

class OrderForm(forms.Form):
    reqmes='Поле не должно быть пустым'
    maxmes='Значение выше допустимого'
    minmes='Значение ниже допустимого'
    nummes='Это поле заполнено неверно'
    datmes='ММ/ЧЧ/ГГГГ или ММ/ЧЧ/ГГ'
    # these forms would not be changed
    responsible = forms.CharField(label='Ответственный менеджер',error_messages={'required': reqmes})
    vehicle = forms.CharField(label='Транспортное средство',error_messages={'required': reqmes})
    agent = forms.CharField(label='Агент',error_messages={'required': reqmes})
    plan_date = forms.DateField(label='Дата доставки',error_messages={'required': reqmes,'invalid': datmes})
    output_id1q= forms.IntegerField(label='Количество, шт',
                                    error_messages={'required':reqmes,'min_value':minmes,'max_value':maxmes,'invalid':nummes},
                                    min_value=1,max_value=51)
    output_id1d= forms.IntegerField(label='Скидка, %',
                                    error_messages={'required':reqmes,'min_value':minmes,'max_value':maxmes,'invalid':nummes},
                                    min_value=0,max_value=90)
    
    # these forms would be changed
    customer_id = forms.ChoiceField(label='Клиент',choices=[(0,'Выберите клиента'),])
    delpoint_id = forms.ChoiceField(label='Пункт доставки',choices=[(0,'Выберите пункт доставки'),])
    output_id1 = forms.ChoiceField(label='Товар 1',choices=[(0,'Выберите товар'),])
    
    def updateNonStaticForms(self):
        reqmes='Поле не должно быть пустым'
        maxmes='Значение выше допустимого'
        minmes='Значение ниже допустимого'
        nummes='Это поле заполнено неверно'
        datmes='ММ/ЧЧ/ГГГГ или ММ/ЧЧ/ГГ'
        conn=psycopg2.connect(util.pgset())
        cur=conn.cursor()
        
        # adding Form with customers
        query = "SELECT customer_id,name FROM customers ORDER BY name asc;"
        cur.execute(query)
        info=cur.fetchall()
        info_ok= [(0,'Выберите клиента'),]
        for el in info:
            info_ok.append((el[0],el[1]),)
        self.fields['customer_id'] = forms.ChoiceField(label='Клиент',choices=info_ok)
        
        # adding Form with delpoint_id-es
        query = "SELECT delpoint_id,del_address FROM delpoints ORDER BY del_address asc;"
        cur.execute(query)
        info=cur.fetchall()
        info_ok= [(0,'Выберите пункт доставки'),]
        for el in info:
            info_ok.append((el[0],el[1]),)
        self.fields['delpoint_id'] = forms.ChoiceField(label='Пункт доставки',choices=info_ok)
        
        # adding Output 1
        query = "SELECT output_id,output_name FROM outputs ORDER BY output_name asc;"
        cur.execute(query)
        outputs=cur.fetchall()
        outputs_ok = [(0,'Выберите товар'),]
        for el in outputs:
            outputs_ok.append((el[0],el[1]),)
        #ch=[('M','Male'),('F','Female')]
        self.fields['output_id1'] = forms.ChoiceField(label='Товар 1',choices=outputs_ok)
 
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
    
    def clean_vehicle(self):
        ri=self.cleaned_data['vehicle']
        if (';' in ri)or(')' in ri)or(',' in ri):
            raise forms.ValidationError("Недопустимые символы")
        return ri
        
    def clean_agent(self):
        ri=self.cleaned_data['agent']
        if (';' in ri)or(')' in ri)or(',' in ri):
            raise forms.ValidationError("Недопустимые символы")
        return ri
        
        
class AddCustomerForm(forms.Form):
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
    
    def clean_name(self):
        ri=self.cleaned_data['name']
        if (';' in ri)or(')' in ri):
            raise forms.ValidationError("Недопустимые символы")
        return ri
    
    def clean_address(self):
        ri=self.cleaned_data['address']
        if (';' in ri)or(')' in ri):
            raise forms.ValidationError("Недопустимые символы")
        return ri
    
    def clean_phone(self):
        ri=self.cleaned_data['phone']
        if (';' in ri)or(')' in ri):
            raise forms.ValidationError("Недопустимые символы")
        return ri    
    
    def clean_fax(self):
        ri=self.cleaned_data['fax']
        if (';' in ri)or(')' in ri):
            raise forms.ValidationError("Недопустимые символы")
        return ri    
    
    def clean_email(self):
        ri=self.cleaned_data['email']
        if (';' in ri)or(')' in ri):
            raise forms.ValidationError("Недопустимые символы")
        return ri    
    
    def clean_bank(self):
        ri=self.cleaned_data['bank']
        if (';' in ri)or(')' in ri):
            raise forms.ValidationError("Недопустимые символы")
        return ri
    
    
class AddOutputForm(forms.Form):
    reqmes='Поле не должно быть пустым'
    nummes='Это поле заполнено неверно'
    maxmes='Значение выше допустимого'
    minmes='Значение ниже допустимого'
    output_name = forms.CharField(label='Название',error_messages={'required':reqmes })
    output_price = forms.IntegerField(label='Стоимость',
                                      error_messages={'required': reqmes,'invalid': nummes,'min_value':minmes,'max_value':maxmes},
                                      min_value=50,max_value=100000)
    
    def clean_output_name(self):
        ri=self.cleaned_data['output_name']
        if (';' in ri)or(')' in ri):
            raise forms.ValidationError("Недопустимые символы")
        return ri
    
    
class AddDelpointForm(forms.Form):
    reqmes='Поле не должно быть пустым'
    del_address = forms.CharField(label='Адрес',error_messages={'required':reqmes })
    zone = forms.CharField(label='Зона',error_messages={'required': reqmes})
    floor= forms.CharField(label='Этаж',error_messages={'required': reqmes})
    elevator = forms.ChoiceField(label='Лифт',choices=[('1','Есть'),('2','Нет')])
    entrance= forms.CharField(label='Номер парадной',error_messages={'required': reqmes})
    code= forms.CharField(label='Входной код',error_messages={'required': reqmes})
    
    def clean_del_address(self):
        ri=self.cleaned_data['del_address']
        if (';' in ri)or(')' in ri):
            raise forms.ValidationError("Недопустимые символы")
        return ri
    
    def clean_zone(self):
        ri=self.cleaned_data['zone']
        if (';' in ri)or(')' in ri):
            raise forms.ValidationError("Недопустимые символы")
        return ri
    
    def clean_floor(self):
        ri=self.cleaned_data['floor']
        if (';' in ri)or(')' in ri):
            raise forms.ValidationError("Недопустимые символы")
        return ri
    
    def clean_entrance(self):
        ri=self.cleaned_data['entrance']
        if (';' in ri)or(')' in ri):
            raise forms.ValidationError("Недопустимые символы")
        return ri
    
    def clean_code(self):
        ri=self.cleaned_data['code']
        if (';' in ri)or(')' in ri):
            raise forms.ValidationError("Недопустимые символы")
        return ri
    
class DelivOrderForm(forms.Form):
    # this form would be changed
    delivering_order = forms.ChoiceField(label='Заказ',choices=[(0,'Выберите заказ'),])
    def updateNonStaticForm(self):
        conn=psycopg2.connect(util.pgset())
        cur=conn.cursor()
        
        # adding orders to delivering_order Form
        query = "select a.order_id,b.plan_date "
        query+= "from orders a inner join delivery_diagrams b "
        query+= "on (a.diagram_id=b.diagram_id and b.status=false);"
        cur.execute(query)
        outputs=cur.fetchall()
        ord_ok = [(0,'Выберите заказ'),]
        for el in outputs:
            ord_ok.append((el[0],"№"+str(el[0])+", план - "+str(el[1])),)
        self.fields['delivering_order'] = forms.ChoiceField(label='Заказ',choices=ord_ok)
        
        conn.commit()
        cur.close()
        conn.close()
        
    def clean_delivering_order(self):
        oi=self.cleaned_data['delivering_order']
        if oi=='0':
            raise forms.ValidationError("Заказ не выбран")
        return oi