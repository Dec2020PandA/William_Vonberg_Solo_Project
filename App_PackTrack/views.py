from django.shortcuts import render, redirect
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse as parse_date
from .models import *
from django.contrib import messages
from .Packcalculator import *
import bcrypt

# main page defs


def to_landing(request):
    return redirect('/landing')


def landing(request):
    return render(request, 'landing_page.html')


def log_page(request):
    return render(request, 'log_reg.html')


def reg_page(request):
    return render(request, 'reg_log.html')

def support(request):
    if "user_id" not in request.session:
        return redirect('/')
    return render(request,"support.html")

def add_dog(request):
    if "user_id" not in request.session:
        return redirect('/')
    context={
        'dogs': Pet.objects.filter(owner=request.session['user_id']),
        'validate':1
    }
    return render(request,"pet_profile.html",context)

def summary(request):
    if "user_id" not in request.session:
        return redirect('/')
    user_data=Body.objects.get(user=request.session['user_id'])
    context = {
        'user': User.objects.get(id=request.session['user_id']),
        'data': Body.objects.get(user=request.session['user_id']),
        'bmi': BMIcalc(user_data.current_weight,user_data.height),
        'bmr': BMRcalc(user_data.current_weight,user_data.height,request.session['user_age'],user_data.gender),
        'cal': CalDay(BMRcalc(user_data.current_weight,user_data.height,request.session['user_age'],user_data.gender),user_data.activity_lvl,user_data.rate),
    }
    return render(request, "summary.html", context)


def profile(request):
    if "user_id" not in request.session:
        return redirect('/')
    user_data=Body.objects.get(user=request.session['user_id'])
    context = {
        'dogs': Pet.objects.filter(owner=request.session['user_id']),
        'user': User.objects.get(id=request.session['user_id']),
        'data': Body.objects.get(user=request.session['user_id']),
        'bmi': BMIcalc(user_data.current_weight,user_data.height),
        'bmr': BMRcalc(user_data.current_weight,user_data.height,request.session['user_age'],user_data.gender),
        'cal': CalDay(BMRcalc(user_data.current_weight,user_data.height,request.session['user_age'],user_data.gender),user_data.activity_lvl,user_data.rate),
        
    }
    return render(request, "profile.html", context)

def pet_profile(request,dog_tag):
    if "user_id" not in request.session:
        return redirect('/')
    pet_data=Pet.objects.get(id=dog_tag)
    context={
        'rer': RERcalc(pet_data.pet_weight),
        'mer':CalDayDog(RERcalc(pet_data.pet_weight),pet_data.pet_gender,pet_data.pet_act_lvl,pet_data.pet_rate),
        'pets':Pet.objects.get(id=dog_tag),
        'dogs': Pet.objects.filter(owner=request.session['user_id']),
        'exists': dog_tag,
    }
    return render(request,"pet_profile.html",context)

# page redirects to prevent conifrm submission msg


def login(request):
    if request.method == "POST":
        return redirect("/log_page")
    return redirect("/")


def register(request):
    if request.method == "POST":
        return redirect("/reg_page")
    return redirect("/")

# user login and validation


def user_login(request):
    # logging in a user
    # queery for logged user
    logged_user = User.objects.filter(email=request.POST['email'])
    if logged_user:
        logged_user = logged_user[0]
        print(logged_user.first_name)
        # compare passwords
        if bcrypt.checkpw(request.POST['p_w'].encode(), logged_user.password.encode()):
            request.session['user_id'] = logged_user.id
            request.session['user_name'] = f"{logged_user.first_name}"
            dateA = parse_date(str(logged_user.birthday))
            dateB = date.today()
            difference_years = relativedelta(dateB, dateA).years
            request.session['user_age']=difference_years
            return redirect('/summary')
        errors = {}
        errors['inv_pwd'] = "Invalid password."
        if errors:
            for error in errors:
                messages.error(request, errors[error])
            return redirect('/log_page')
    return redirect('/log_page')

# create user and validations


def create_user(request):
    # create user
    if request.method == 'POST':
        # validate data
        errors = User.objects.validator(request.POST)
        if errors:
            for error in errors:
                messages.error(request, errors[error])
            return redirect('/reg_page')
        # encrypting pw
        # store plaintext pw into var
        user_pw = request.POST['pw']
        # now hash it
        hash_pw = bcrypt.hashpw(user_pw.encode(), bcrypt.gensalt()).decode()
        new_user = User.objects.create(
            first_name=request.POST['f_n'],
            last_name=request.POST['l_n'],
            birthday=request.POST['b_d'],
            email=request.POST['email'],
            password=hash_pw
        )
        request.session['user_id'] = new_user.id
        request.session['user_name'] = f"{new_user.first_name}"
        dateA = parse_date(str(request.POST['b_d']))
        dateB = date.today()
        difference_years = relativedelta(dateB, dateA).years
        request.session['user_age']=difference_years
        body_data = Body.objects.create(
            user=User.objects.get(id=request.session['user_id']),
            current_weight=1,
            height=1,
            gender="X",
            activity_lvl=1.2,
            goal=1,
            rate=0,
            carb_percent=45,
            fat_percent=25,
            protein_percent=30,
        )
        return redirect('/profile')
    return redirect('/reg_page')

# edit profile

def user_update(request):
    if request.method == "POST":
        edit_user = User.objects.get(id=request.session['user_id'])
        edit_pw = edit_user.password
        body_data = Body.objects.get(user=edit_user.id)
        errors = User.objects.edit_validator(request.POST)
        if errors:
            for error in errors:
                messages.error(request, errors[error])
            return redirect('/profile')
        if edit_user.first_name != request.POST['f_n']:
            edit_user.first_name = request.POST['f_n']
            edit_user.save()
        if edit_user.last_name != request.POST['l_n']:
            edit_user.last_name = request.POST['l_n']
            edit_user.save()
        if edit_user.birthday != request.POST['b_d']:
            edit_user.birthday = request.POST['b_d']
            edit_user.save()
        if edit_user.email != request.POST['email']:
            edit_user.email = request.POST['email']
            edit_user.save()
        if bcrypt.checkpw(request.POST['old_pw'].encode(), edit_pw.encode()):
            user_pw = request.POST['pw']
            hash_pw = bcrypt.hashpw(user_pw.encode(), bcrypt.gensalt()).decode()
            edit_user.password = hash_pw
            edit_user.save()
        if body_data.current_weight != request.POST['current_weight']:
            body_data.current_weight = request.POST['current_weight']
            body_data.save()
        if body_data.rate != request.POST['rate']:
            body_data.rate = request.POST['rate']
            body_data.save()
        if body_data.height != request.POST['height']:
            body_data.height = request.POST['height']
            body_data.save()
        if body_data.gender != request.POST['gender']:
            body_data.gender = request.POST['gender']
            body_data.save()
        if body_data.activity_lvl != request.POST['activity_lvl']:
            body_data.activity_lvl = request.POST['activity_lvl']
            body_data.save()
        if body_data.goal != request.POST['goal']:
            body_data.goal = request.POST['goal']
            body_data.save()
        if body_data.carb_percent != request.POST['carb_percent']:
            body_data.carb_percent = request.POST['carb_percent']
            body_data.save()
        if body_data.fat_percent != request.POST['fat_percent']:
            body_data.fat_percent = request.POST['fat_percent']
            body_data.save()
        if body_data.protein_percent != request.POST['protein_percent']:
            body_data.protein_percent = request.POST['protein_percent']
            body_data.save()
        request.session['user_id'] = edit_user.id
        request.session['user_name'] = f"{edit_user.first_name}"
        return redirect("/profile")
    return redirect("/profile")

# per profile update and add

def pet_update(request,dog_id):
    if request.method=="POST":
        if dog_id==0:
            new_dog=Pet.objects.create(
                owner=User.objects.get(id=request.session['user_id']),
                pet_name=request.POST['pet_name'],
                pet_bday=request.POST['pet_bday'],
                pet_bodycond=request.POST['pet_bodycond'],
                pet_weight=request.POST['pet_weight'],
                pet_act_lvl=request.POST['pet_act_lvl'],
                pet_gender=request.POST['pet_gender'],
                pet_goal=request.POST['pet_goal'],
                pet_carb=request.POST['pet_carb'],
                pet_fat=request.POST['pet_fat'],
                pet_protein=request.POST['pet_protein'],
                pet_rate=request.POST['pet_rate'],
            )
            return redirect(f"/pet_profile/{new_dog.id}")
        else:
            dog_info=Pet.objects.get(id=dog_id)
            if dog_info.pet_name != request.POST['pet_name']:
                dog_info.pet_name = request.POST['pet_name']
                dog_info.save()
            if dog_info.pet_bday != request.POST['pet_bday']:
                dog_info.pet_bday = request.POST['pet_bday']
                dog_info.save()
            if dog_info.pet_bodycond != request.POST['pet_bodycond']:
                dog_info.pet_bodycond = request.POST['pet_bodycond']
                dog_info.save()
            if dog_info.pet_weight != request.POST['pet_weight']:
                dog_info.pet_weight = request.POST['pet_weight']
                dog_info.save()  
            if dog_info.pet_act_lvl != request.POST['pet_act_lvl']:
                dog_info.pet_act_lvl = request.POST['pet_act_lvl']
                dog_info.save()
            if dog_info.pet_gender != request.POST['pet_gender']:
                dog_info.pet_gender = request.POST['pet_gender']
                dog_info.save()
            if dog_info.pet_goal != request.POST['pet_goal']:
                dog_info.pet_goal = request.POST['pet_goal']
                dog_info.save()
            if dog_info.pet_carb != request.POST['pet_carb']:
                dog_info.pet_carb = request.POST['pet_carb']
                dog_info.save()
            if dog_info.pet_fat != request.POST['pet_fat']:
                dog_info.pet_fat = request.POST['pet_fat']
                dog_info.save()
            if dog_info.pet_protein != request.POST['pet_protein']:
                dog_info.pet_protein = request.POST['pet_protein']
                dog_info.save()
            if dog_info.pet_rate != request.POST['pet_rate']:
                dog_info.pet_rate = request.POST['pet_rate']
                dog_info.save()
        return redirect(f"/pet_profile/{dog_id}")        
    return redirect("/profile")

# delete pet profile

def delete(request,dog_tag):
    Pet.objects.get(id=dog_tag).delete()
    return redirect("/profile")

#process bug reports

def process_issue(request):
    if request.method=="POST":
        new_report=Bug.objects.create(
            user=User.objects.get(id=request.session['user_id']),
            issue_location=request.POST['issue_location'],
            issue_date=request.POST['issue_date'],
            issue_comp=request.POST['issue_comp'],
            issue_desc=request.POST['issue_description'],
            issue_status=request.POST['issue_status']
        )
        return redirect("/support")
    return redirect("/support")

#process comments ( will change to outside source later)
def support_comment(request):
    if request.method=="POST":
        new_comment=Comment.objects.create(
            poster=User.objects.get(id=request.session['user_id']),
            name=request.POST['name'],
            email=request.POST['email'],
            message=request.POST['comment']
        )
        return redirect("/support")
    return redirect("/")

def landing_comment(request):
    if request.method=="POST":
        new_comment=Comment.objects.create(
            poster=User.objects.get(id=request.session['user_id']),
            name=request.POST['name'],
            email=request.POST['email'],
            message=request.POST['comment']
        )
        return redirect("/landing")
    return redirect("/")


def logout(request):
    request.session.flush()
    return redirect("/")
