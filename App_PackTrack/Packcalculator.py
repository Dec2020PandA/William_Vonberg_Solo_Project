def BMIcalc(weight,height):
    bmi=(weight * 0.453592) / (height * 0.0254)**2
    return round(bmi)

def BMRcalc(weight,height,age,gender):
    if gender == "F":
        bmr=(447.6 + (9.25 * (weight * 0.453592))+(3.10 * (height * 2.54))-(4.33 * age))
    else: 
        bmr=(88.4 + (13.4 * (weight * 0.453592))+(4.8 * (height * 2.54))-(5.68 * age))
    return round(bmr)

def CalDay(bmr,act_lvl,rate):
    calgoal= (bmr*act_lvl)+rate
    return round(calgoal)

def RERcalc(weight):
    rer=70*((weight*0.453592)**.75)
    return round(rer)

def CalDayDog():
    pass
