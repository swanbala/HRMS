from django.shortcuts import render_to_response
from django.http import HttpResponse,Http404
from HRM import forms
from HRM import models
from judge import level
import time
from datetime import * 
from django.db.transaction import Transaction
from django.db import transaction
from HRM.models import basic_staff
# Create your views here.



def login(request):
    if request.method=='POST':
        form=forms.LoginForm(request.POST)
        if not form.is_valid():
            return render_to_response('login.html',{'error':form.errors})
        try:
            m = models.basic_staff.objects.get(id=request.POST['username'])     
            if request.POST['username']=='2014000':
                request.session['member_id'] = m.id
                return render_to_response('manager.html')
            elif m.passwd == request.POST['password']:
                request.session['member_id'] = m.id              
                temp_b=models.basic_staff.objects.get(id=m.id)
                temp_w=models.work_staff.objects.get(id=m.id)
                contract={'name':temp_b.name,'id':temp_b.id,'email':temp_b.mail,'tel':temp_b.tel,
                          'level':level(temp_w.level),'superior':level(temp_w.superior),'data':temp_b.data,'department':temp_w.department}
                
                return render_to_response('basic_information.html',contract)   
        except models.basic_staff.DoesNotExist:
                return render_to_response('login.html',{'error':"Your username and password didn't match."})       
    return render_to_response('login.html')



def logout(request):
    try:
        #delete member_id in request.session
        del request.session['member_id']
        del request.session['time_']
    except KeyError:
        pass
    return render_to_response('not_login.html')
 
        
#def main(request):
 #   if 'username' in request.session:
  #      return render_to_response('main.html')
   # else:
    #    return render_to_response('login.html',{'error':"Please login in first!"})

def change_passwd(request):
#    print request.session
    #check if you log in successfully
    if 'member_id' in request.session:
        if request.session['member_id']==2014000:
            if_admin=True
        else:
            if_admin=False
        if request.method=='POST':
            f=forms.change_passwd_Form(request.POST)
            temp=models.basic_staff.objects.get(id=request.session['member_id'])
            if not f.is_valid():
  #              if request.POST['username']=='201400':
   #                 return render_to_response('information.html',{'reason':f.errors})
                return render_to_response('change_passwd.html',{'if_admin':if_admin,'error':f.errors})
            elif  request.POST['old_passwd']==temp.passwd:
                #change database
                models.basic_staff.objects.filter(id=request.session['member_id']).update(passwd=request.POST['new_passwd'])
   #             if request.POST['username']=='201400':
    #                return render_to_response('information.html',{'reason':'password has changed!'})
                return render_to_response('success.html',{'reason':'password has changed!'})  
            return render_to_response('change_passwd.html',{'if_admin':if_admin,'error':"old password is wrong!"})
        return render_to_response('change_passwd.html',{'if_admin':if_admin})
 #       return render_to_response('change_passwd',{'error':"old passeord is wrong!"})                 
    else:
        return render_to_response('not_login.html',{'error':"Please login in first!"}) 



def basic_information(request):
    if 'member_id' in request.session:
        temp_b=models.basic_staff.objects.get(id=request.session['member_id'])
        temp_w=models.work_staff.objects.get(id=request.session['member_id'])
        
        contract={'name':temp_b.name,'id':temp_b.id,'email':temp_b.mail,'tel':temp_b.tel,
                  'level':level(temp_w.level),'superior':level(temp_w.superior),'data':temp_b.data,'department':temp_w.department}
        return render_to_response('basic_information.html',contract)
    else:
        return render_to_response('not_login.html',{'error':"Please login in first!"})   

def ability_work(request):
    if 'member_id' in request.session:
        temp_w=models.work_staff.objects.get(id=request.session['member_id'])
        contract={'train':temp_w.trains,'ability':temp_w.skills}
        return render_to_response('ability_work.html',contract)    
    else:
        return render_to_response('not_login.html',{'error':"Please login in first!"})  
    
    
    
def success(request):
    if 'member_id' in request.session:
        return render_to_response('success.html')
    else:
        return render_to_response('not_login.html',{'error':"Please login in first!"})
    
temp_num=0
def sign_in(request):    
    if 'member_id' in request.session:
        if 'time_' in request.POST :
            if temp_num==0:
                temp=models.work_staff.objects.get(id=request.session['member_id'])
                standard_time=models.time.objects.get(level=temp.level).morning_sign_in
                time_now = datetime.now()
                top_time=(time_now + timedelta(hours = +2)).time()
                bottom_time=(time_now +timedelta(hours = -2)).time()

                if time_now.time()>=standard_time:
                    if bottom_time>=standard_time:
                        temp_num+=1
                        return render_to_response('sign_in.html',{'happen':"Sorry,time signed in is out!"})
                    else:
                        temp_num+=1
                        change_one=models.sign_note.objects.get(id=request.session['member_id']).num_late
                        change_one+=1
                        models.sign_note.objects.filter(id=request.session['member_id']).update(num_late=change_one)
                        return render_to_response('success.html',{'reason':"success,but you late!"})
                else:
                    if top_time>=standard_time:
                        temp_num+=1
                        change=models.sign_note.objects.get(id=request.session['member_id']).num_sign_in
                        change+=1
                        models.sign_note.objects.filter(id=request.session['member_id']).update(num_sign_in=change)
                        return render_to_response('success.html',{'reason':'success'})
                    else:
                        return render_to_response('sign_in.html',{'happen':"Sorry,time has not arrived yet!"})
            else:
                return render_to_response('success.html',{'reason':'you have been signed in!'})               
        return render_to_response('sign_in.html',{'happen':"Sorry,time signed in is out!"})
    else:
        return render_to_response('not_login.html',{'error':"Please login in first!"})
    
    
def salary(request):    
    if 'member_id' in request.session:
        temp=models.pay.objects.get(id=request.session['member_id'])
        contract={'basic':temp.basic,'bonus':temp.bonus}
        return render_to_response('salary.html',contract)
    else:
        return render_to_response('not_login.html',{'error':"Please login in first!"})
    

def former(request):
    if 'member_id' in request.session:
        exit_staff=models.exit_staff.objects.all()
        return render_to_response('former.html',{'exit_staff':exit_staff})
    else:
        return render_to_response('not_login.html',{'error':"Please login in first!"})
 
def all_information(request):
    if 'member_id' in request.session:
        staff=models.basic_staff.objects.all()
        return render_to_response('all_information.html',{'staff':staff})
    else:
        return render_to_response('not_login.html',{'error':"Please login in first!"})

def recorvery_former(request,get_id):
    if 'member_id' in request.session:
        #change the value in basic_staff
        models.basic_staff.objects.filter(id=get_id).update(if_delete=0)
        #delete the tuple in table exit_staff
        models.exit_staff.objects.get(id=get_id).delete()
        exit_staff=models.exit_staff.objects.all()
        return render_to_response('former.html',{'exit_staff':exit_staff})
    else:
        return render_to_response('not_login.html',{'error':"Please login in first!"})
    return render_to_response('former.html')  

@transaction.commit_manually
def sure_former(request):
    if 'member_id' in request.session:
        exit_staff=models.exit_staff.objects.all()
        delete_staff=models.basic_staff.objects.all()
        for staff in delete_staff:
            if staff.if_delete==1:
                get_id=staff.id
                try:
                    models.basic_staff.objects.get(id=get_id).delete()
                    models.pay.objects.get(id=get_id).delete()
                    models.sign_note.objects.get(id=get_id).delete()
                    models.work_staff.objects.get(id=get_id).delete()
                except:
                    transaction.rollback()
                    reason="Failed!"
                else:
                    transaction.commit()
                    reason="Successful !"
                return render_to_response('former.html',{'exit_staff':exit_staff,'result':reason})    
            else:
                pass
        return render_to_response('former.html',{'exit_staff':exit_staff})
    else:
        return render_to_response('not_login.html',{'error':"Please login in first!"})


@transaction.commit_manually
def add(request):
    print request.session['member_id']
    if 'member_id' in request.session:
        if request.method=='POST':
            form=forms.LoginForm(request.POST)
            q=request.POST
            if not form.is_valid():
                return render_to_response('add.html',{'reason':form.errors})
            else:
                time_now = datetime.now()
                print q['Sex']
                try:
                    staff = basic_staff(id=q['username'],name=q['name'],passwd=q['password'],sex=q['Sex'],mail=q['mail'],tel=q['tel'],data=time_now,if_delete=0)
                    staff.save()
                    superior = models.basic_staff.objects.get(id=q['superior'])
                    models.work_staff.objects.create(id=staff,level=q['level'],department=q['department'],superior=superior)
                    models.pay.objects.create(id=q['username'],basic=q['basic'],bonus=0)
                    models.sign_note.objects.create(id=q['username'],num_sign_in=0,num_late=0,num_out=0)
                except:
                    transaction.rollback()
                    reason="Registration Failed!"
                else:
                    transaction.commit()
                    reason="Successful registeration!"
                return render_to_response('add.html',{'reason':reason})
        return render_to_response('add.html')
    else:
        return render_to_response('not_login.html',{'error':"Please login in first!"})
 

 
 
def salary_all(request):
    if 'member_id' in request.session:
        salary=models.pay.objects.all()
        return render_to_response('salary_all.html',{'pay':salary})
    else:
        return render_to_response('not_login.html',{'error':"Please login in first!"})
     
def sign_information(request):
    if 'member_id' in request.session:
        sign=models.sign_note.objects.all()
        return render_to_response('sign_information.html',{'sign':sign})
    else:
        return render_to_response('not_login.html',{'error':"Please login in first!"})
     
def bonus(request):
    if 'member_id' in request.session:
        if request.method=='POST':
            f=forms.bonusFrom(request.POST)
            if not f.is_valid():
                return render_to_response('bonus.html',{'result':f.errors})
            else:
                change=models.pay.objects.filter(id=request.POST['id'])
                change.update(bonus=request.POST['bonus'])
                return render_to_response('bonus.html',{'result':"success"})               
        return render_to_response('bonus.html')
    else:
        return render_to_response('not_login.html',{'error':"Please login in first!"})     
    
    
@transaction.commit_manually    
def change_time(request):
    if 'member_id' in request.session:
        time_t=models.time.objects.all()
        if request.method=='POST':
            f=forms.timeForm(request.POST)
            if not f.is_valid():
                return render_to_response('time.html',{'result':f.errors})
            else:
                try:
                    change=models.time.objects.filter(level=request.POST['level'])
                    change.update(morning_sign_in=request.POST['mor_in'])
                    change.update(morning_sign_in=request.POST['mor_off'])
                    change.update(morning_sign_in=request.POST['aft_in'])
                    change.update(morning_sign_in=request.POST['aft_off'])
                except:
                    transaction.rollback()
                    result="Failed !"
                else:
                    transaction.commit()
                    result="Successful !"
                return render_to_response('time.html',{'result': result})
        return render_to_response('time.html')
    else:
        return render_to_response('not_login.html',{'error':"Please login in first!"})  
   
@transaction.commit_manually    
def delete_staff(request,id_get):
    if 'member_id' in request.session:
        try:
            id_=int(id_get)
        except ValueError:
            raise Http404()
        change_b=models.basic_staff.objects.get(id=id_)
        change_w=models.work_staff.objects.get(id=id_)
        try:
            models.exit_staff.objects.create(id=id_,name=change_b.name,sex=change_b.sex,mail=change_b.mail,
                                             tel=change_b.tel,data=change_b.data,trains=change_w.trains,skills=change_w.skills,if_delete=0)
            models.basic_staff.objects.filter(id=id_).update(if_delete=1)
        except:
            transaction.rollback()
            result="Failed !"
        else:
            transaction.commit()
            result="Successful !"
        return render_to_response('all_information.html',{'result':result})
    else:
        return render_to_response('not_login.html',{'error':"Please login in first!"})
    
def not_login(request):
    return render_to_response('not_login.html')
 

def change_information(request,get_id):
    if 'member_id' in request.session:
        try:
            id_=int(get_id)
        except ValueError:
            raise Http404()
        
        if request.method=='POST':
            f=forms.changeForm(request.POST)
            if not f.is_valid():
                return render_to_response('manager.html',{'reason':f.errors})
            else:
                models.basic_staff.objects.filter(id=get_id).update(name=request.POST['name'],tel=request.POST['tel'],
                                                                    mail=request.POST['mail'],passwd=request.POST['password'])
                return render_to_response('all_information.html')
        else:
            staff=models.basic_staff.objects.all()
            return render_to_response('change_information.html',{'staff':staff,'get_id':id_})                   
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         