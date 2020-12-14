from django.db import models
from datetime import date,datetime
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse as parse_date
from .Packcalculator import *
import re

## Validators

class UserManager(models.Manager):
    def validator(self,postdata):
        errors={}
        email_check=re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        date1 = parse_date(postdata['b_d'])
        date2 = date.today()
        difference_in_years = relativedelta(date2, date1).years
        unique_email = User.objects.filter(email= postdata['email'])             
        if unique_email:
            errors['duplicate'] = "That email already exists. Try a different email."
        if len(postdata['f_n'])<2:
            errors['f_n']="Name must be longer than 2 characters"
        if len(postdata['l_n'])<2:
             errors['l_n']="Name must be longer than 2 characters"
        if (postdata['b_d'])>= str(date.today()):
            errors['b_d']='Birthday must be earlier than today!'
        if difference_in_years < 13 and difference_in_years>0:
            errors['age']="You are too young to register."
        if not email_check.match(postdata['email']):            
            errors['email'] = ("Invalid email address!")
        if len (postdata['pw'])<8:
            errors['pw']="Password must be at least 8 characters long"
        if postdata['pw'] != postdata['conf_pw']:
            errors['conf_pw']='Passwords do not match!'
        return errors

    def edit_validator(self,postdata):
            errors={}
            email_check=re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
            unique_email = User.objects.filter(email= postdata['email'])
            if postdata['email']!=postdata['conf_email']:
                if unique_email:
                    errors['duplicate'] = "That email already exists. Try a different email."
            if len(postdata['f_n'])<2:
                errors['f_n']="Name must be longer than 2 characters"
            if len(postdata['l_n'])<2:
                errors['l_n']="Name must be longer than 2 characters"
            if not email_check.match(postdata['email']) and unique_email!=postdata['email']:            
                errors['email'] = ("Invalid email address!")
            if len (postdata['pw'])<8 and len (postdata['pw'])=='':
                errors['pw']="Password must be at least 8 characters long"
            if postdata['pw'] != postdata['conf_pw']:
                errors['conf_pw']='Passwords do not match!'
            return errors

## User and Pet data

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    birthday = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects= UserManager()

    def total_cals_day(self, _date = None):
        if _date == None: _date = date.today()
        entries = self.users_diaries.filter(user_entry =_date)
        return sum((entry.calories for entry in entries))-sum((entry.calories_burned for entry in entries))

    def total_fat_day(self, _date = None):
        if _date == None: _date = date.today()
        entries = self.users_diaries.filter(user_entry =_date)
        return sum((entry.fat for entry in entries))
    
    def total_carbs_day(self, _date = None):
        if _date == None: _date = date.today()
        entries = self.users_diaries.filter(user_entry =_date)
        return sum((entry.carbs for entry in entries))

    def total_protein_day(self, _date = None):
        if _date == None: _date = date.today()
        entries = self.users_diaries.filter(user_entry =_date)
        return sum((entry.protein for entry in entries))

class Pet(models.Model):
    owner=models.ForeignKey(User, related_name='pet_owner',on_delete=models.CASCADE)
    pet_name= models.CharField(default="Spot",max_length=255)
    pet_bday= models.DateField(default="1901-01-01")
    pet_bodycond= models.IntegerField()
    pet_weight=models.IntegerField(default=0)
    pet_act_lvl=models.FloatField(max_length=48)
    pet_gender=models.CharField(max_length=10)
    pet_goal=models.IntegerField(default=0)
    pet_carb=models.IntegerField(default=60)
    pet_fat=models.IntegerField(default=15)
    pet_protein=models.IntegerField(default=25)
    pet_rate=models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def total_petcals_day(self, _date = None):
        if _date == None: _date = date.today()
        pet_entries = self.pets_diaries.filter(pet_entry =_date)
        return sum((pet_entry.pet_cals for pet_entry in pet_entries))-sum((pet_entry.pet_calburned for pet_entry in pet_entries))

    def total_petfat_day(self, _date = None):
        if _date == None: _date = date.today()
        pet_entries = self.pets_diaries.filter(pet_entry =_date)
        return sum((pet_entry.pet_fat for pet_entry in pet_entries))

    def total_petcarb_day(self, _date = None):
        if _date == None: _date = date.today()
        pet_entries = self.pets_diaries.filter(pet_entry =_date)
        return sum((pet_entry.pet_carbs for pet_entry in pet_entries))

    def total_petprot_day(self, _date = None):
        if _date == None: _date = date.today()
        pet_entries = self.pets_diaries.filter(pet_entry =_date)
        return sum((pet_entry.pet_protein for pet_entry in pet_entries))

    @property
    def rer(self):
        return RERcalc(self.pet_weight)

    @property
    def mer(self):
        return CalDayDog(RERcalc(self.pet_weight),self.pet_gender,self.pet_act_lvl,self.pet_rate)

    @property
    def petFat(self):
        return round((CalDayDog(RERcalc(self.pet_weight),self.pet_gender,self.pet_act_lvl,self.pet_rate))*(self.pet_fat/100)/9)

    @property
    def petCarb(self):
        return round((CalDayDog(RERcalc(self.pet_weight),self.pet_gender,self.pet_act_lvl,self.pet_rate))*(self.pet_carb/100)/4)

    @property
    def petProt(self):
        return round((CalDayDog(RERcalc(self.pet_weight),self.pet_gender,self.pet_act_lvl,self.pet_rate))*(self.pet_protein/100)/4)    

class Body(models.Model):
    user=models.ForeignKey(User, related_name='bodies',on_delete=models.CASCADE)
    current_weight=models.IntegerField()
    height=models.IntegerField()
    gender=models.CharField(max_length=2)
    activity_lvl=models.FloatField()
    goal=models.IntegerField()
    rate=models.IntegerField()
    carb_percent=models.IntegerField()
    fat_percent=models.IntegerField()
    protein_percent=models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class User_diary(models.Model):
    user=models.ForeignKey(User, related_name='users_diaries',on_delete=models.CASCADE)
    user_entry=models.DateField(blank=False, default=datetime.now)
    calories=models.IntegerField()
    fat=models.IntegerField()
    carbs=models.IntegerField()
    protein= models.IntegerField()
    activity= models.CharField(max_length=48)
    calories_burned=models.IntegerField()
    food_item=models.CharField(max_length=48)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
        

class Pet_diary(models.Model):
    pet=models.ForeignKey(Pet, related_name='pets_diaries',on_delete=models.CASCADE)
    owner=models.ForeignKey(User,related_name = "pet_owners", on_delete = models.CASCADE)
    pet_entry=models.DateField(blank=False, default=datetime.now)
    pet_cals=models.IntegerField()
    pet_fat=models.IntegerField()
    pet_carbs=models.IntegerField()
    pet_protein= models.IntegerField()
    pet_activity= models.CharField(max_length=48)
    pet_calburned=models.IntegerField()
    pet_food=models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Bug(models.Model):
    user=models.ForeignKey(User,related_name="user_bugs", on_delete=models.CASCADE)
    issue_location=models.CharField(max_length=255)
    issue_date=models.DateField()
    issue_comp=models.CharField(max_length=255)
    issue_desc=models.TextField()
    issue_status=models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    name=models.CharField(max_length=255)
    email=models.EmailField()
    message=models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)