from django.db import models

# Create your models here.

class basic_staff(models.Model):
    id=models.IntegerField(primary_key=True,max_length=7)
    name=models.CharField(max_length=20)
    sex=models.CharField(max_length=1,choices=(('M', 'Male'), ('F', 'Female')))
    mail=models.EmailField()
    tel=models.BigIntegerField(max_length=13)
    data=models.DateField()
    passwd=models.CharField(max_length=30)
    if_delete=models.IntegerField(max_length=1)
     
    def __unicode__(self):
        return u' %s' % self.id


class work_staff(models.Model):
    id=models.OneToOneField(basic_staff,primary_key=True,db_column='id')
#     id=models.IntegerField(primary_key=True,max_length=7)
    level=models.IntegerField(max_length=1)
    superior=models.ForeignKey(basic_staff,related_name='bbb')
    department=models.CharField(max_length=10)
    trains=models.TextField(blank=True)
    skills=models.TextField(blank=True)
    
    def __unicode__(self):
        return u' %s' % self.id
    
class pay(models.Model):
    id=models.IntegerField(primary_key=True,max_length=7)
    basic=models.IntegerField()
    bonus=models.IntegerField(blank=True)
    
    def __unicode__(self):
        return u' %s' % self.id
    
    
class time(models.Model):
    level=models.IntegerField(primary_key=True,max_length=1)
    morning_sign_in=models.TimeField()
    morning_sign_off=models.TimeField()
    afternonn_sign_in=models.TimeField()
    afternoon_sign_off=models.TimeField()
    
class exit_staff(models.Model):
    id=models.IntegerField(primary_key=True,max_length=7)
    name=models.CharField(max_length=20)
    sex=models.CharField(max_length=1,choices=(('M', 'Male'), ('F', 'Female')))
    mail=models.EmailField()
    tel=models.IntegerField(max_length=13)
    data=models.DateField()
    trains=models.TextField(blank=True)
    skills=models.TextField(blank=True)
    if_delete=models.IntegerField(max_length=1)
    
class sign_note(models.Model):
    id=models.IntegerField(primary_key=True,max_length=7)
    num_sign_in=models.IntegerField(0)
    num_late=models.IntegerField(0)
    num_out=models.IntegerField(0)


class application():
    applicants=models.ForeignKey(basic_staff)
    superior=models.ForeignKey(basic_staff)
    reason=models.TextField()
    if_allow=models.IntegerField(0,max_length=1)
    start_time=models.DateTimeField()
    end_time=models.DateTimeField()
       
    