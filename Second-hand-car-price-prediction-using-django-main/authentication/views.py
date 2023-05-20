from django.shortcuts import render, redirect
# from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
# from django.contrib.auth.decorators import login_required
from authentication.models import PredictCarModel
from django.conf import settings
from django.core.mail import EmailMessage, send_mail
from django.core.mail import  send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str # changed force_text to force_str
from . tokens import generate_token
from django.core.exceptions import ValidationError
import pickle
import numpy as np 
import requests
import datetime


CAR_MODELS = {
    'Fiat Siena': 1,
    'Maruti 800': 2,
    'Maruti Esteem': 3,
    'Fiat Petra': 4,
    'Maruti 1000': 5,
    'Maruti Zen': 6,
    'Maruti Versa': 7,
    'Chevrolet Aveo': 8,
    'Ambassador Classic': 9,
    'Ford Ikon': 10,
    'Chevrolet Spark': 11,
    'Tata Nano': 12,
    'Hyundai Santro': 13,
    'Mahindra Logan': 14,
    'Maruti Estilo': 15,
    'Hyundai Getz': 16,
    'Hyundai Accent': 17,
    'Tata Indica': 18,
    'Mitsubishi Lancer': 19,
    'Fiat Grande': 20,
    'Maruti A-Star': 21,
    'Skoda Fabia': 22,
    'Tata Indigo': 23,
    'Mahindra Renault': 24,
    'Maruti Omni': 25,
    'Chevrolet Beat': 26,
    'Ford Fiesta': 27,
    'Chevrolet Optra': 28,
    'Tata Venture': 29,
    'Fiat Linea': 30,
    'Maruti Alto': 31,
    'Fiat Punto': 32,
    'Tata Manza': 33,
    'Maruti Wagon': 34,
    'Hyundai i10': 35,
    'Hyundai EON': 36,
    'Nissan Micra': 37,
    'Honda Civic': 38,
    'Smart Fortwo': 39,
    'Ford Classic': 40,
    'Ford Fusion': 41,
    'Datsun redi-GO': 42,
    'Datsun GO': 43,
    'Datsun Redi': 44,
    'Chevrolet Sail': 45,
    'Mahindra Verito': 46,
    'Maruti SX4': 47,
    'Ford Figo': 48,
    'Renault KWID': 49,
    'Mitsubishi Cedia': 50,
    'Mahindra Quanto': 51,
    'Toyota Qualis': 52,
    'Tata New': 53,
    'Honda Brio': 54,
    'Maruti Ritz': 55,
    'Chevrolet Captiva': 56,
    'Maruti Eeco': 57,
    'Nissan Evalia': 58,
    'Renault Scala': 59,
    'Renault Fluence': 60,
    'Nissan Sunny': 61,
    'Maruti Celerio': 62,
    'Toyota Etios': 63,
    'Renault Pulse': 64,
    'Chevrolet Enjoy': 65,
    'Mahindra Jeep': 66,
    'Volkswagen Polo': 67,
    'Mahindra Xylo': 68,
    'Tata Zest': 69,
    'Tata Bolt': 70,
    'Maruti Swift': 71,
    'Honda Amaze': 72,
    'Hyundai Xcent': 73,
    'Skoda Laura': 74,
    'Tata Sumo': 75,
    'Volkswagen Vento': 76,
    'Hyundai i20': 77,
    'Tata Tiago': 78,
    'Hyundai Grand': 79,
    'Honda Accord': 80,
    'Chevrolet Tavera': 81,
    'Mahindra KUV': 82,
    'Honda CR-V': 83,
    'Mahindra Bolero': 84,
    'Honda City': 85,
    'Honda Mobilio': 86,
    'Hyundai Sonata': 87,
    'Volkswagen CrossPolo': 88,
    'Hyundai Verna': 89,
    'Nissan Teana': 90,
    'Volkswagen Ameo': 91,
    'Maruti Dzire': 92,
    'Skoda Rapid': 93,
    'Tata Xenon': 94,
    'Maruti Ignis': 95,
    'Toyota Platinum': 96,
    'Fiat Avventura': 97,
    'Toyota Corolla': 98,
    'Honda Jazz': 99,
    'Nissan Terrano': 100,
    'Chevrolet Cruze': 101,
    'Mahindra Scorpio': 102,
    'Volkswagen Passat': 103,
    'Renault Duster': 104,
    'Ford Ecosport': 105,
    'Tata Tigor': 106,
    'Ford Aspire': 107,
    'Volkswagen Jetta': 108,
    'Maruti Ertiga': 109,
    'Maruti Baleno': 110,
    'Ford Freestyle': 111,
    'Skoda Yeti': 112,
    'Maruti Grand': 113,
    'Mahindra XUV300': 114,
    'Mahindra NuvoSport': 115,
    'Mitsubishi Outlander': 116,
    'Hyundai Elite': 117,
    'Maruti Ciaz': 118,
    'Skoda Superb': 119,
    'Mitsubishi Montero': 120,
    'Renault Lodgy': 121,
    'Nissan X-Trail': 122,
    'Maruti S': 123,
    'Maruti S-Cross': 124,
    'Ford EcoSport': 125,
    'Renault Koleos': 126,
    'Force One': 127,
    'Tata Safari': 128,
    'Mahindra TUV': 129,
    'Honda WR-V': 130,
    'Hyundai Elantra': 131,
    'Honda BR-V': 132,
    'Maruti Vitara': 133,
    'Honda WRV': 134,
    'Volvo S80': 135,
    'Mahindra Thar': 136,
    'Honda BRV': 137,
    'Mahindra XUV500': 138,
    'Tata Nexon': 139,
    'Mahindra Ssangyong': 140,
    'Skoda Octavia': 141,
    'Mercedes-Benz S-Class': 142,
    'Hyundai Tucson': 143,
    'Toyota Innova': 144,
    'Mitsubishi Pajero': 145,
    'Mercedes-Benz B': 146,
    'ISUZU D-MAX': 147,
    'Hyundai Creta': 148,
    'Toyota Prius': 149,
    'Hyundai Santa': 150,
    'Mahindra E': 151,
    'Renault Captur': 152,
    'Tata Hexa': 153,
    'BMW 3': 154,
    'Volkswagen Beetle': 155,
    'Mercedes-Benz A': 156,
    'Toyota Fortuner': 157,
    'BMW 1': 158,
    'Mercedes-Benz New': 159,
    'Volvo XC60': 160,
    'BMW X1': 161,
    'Audi A4': 162,
    'Jeep Compass': 163,
    'Audi A3': 164,
    'Toyota Camry': 165,
    'Volvo S60': 166,
    'Isuzu MUX': 167,
    'Mercedes-Benz R-Class': 168,
    'Volvo V40': 169,
    'Mercedes-Benz S': 170,
    'Audi A6': 171,
    'Audi Q3': 172,
    'BMW 5': 173,
    'Mercedes-Benz E-Class': 174,
    'Mini Countryman': 175,
    'Volvo XC90': 176,
    'Mercedes-Benz GLA': 177,
    'Ford Endeavour': 178,
    'Mini Cooper': 179,
    'Volkswagen Tiguan': 180,
    'Mercedes-Benz CLA': 181,
    'Audi A7': 182,
    'Jaguar XF': 183,
    'Audi A8': 184,
    'Audi TT': 185,
    'Mercedes-Benz SL-Class': 186,
    'Mercedes-Benz M-Class': 187,
    'BMW X3': 188,
    'Mercedes-Benz CLS-Class': 189,
    'Audi Q5': 190,
    'BMW 7': 191,
    'Land Rover': 192,
    'Mini Clubman': 193,
    'Mercedes-Benz C-Class': 194,
    'Jaguar XE': 195,
    'Audi RS5': 196,
    'Porsche Cayenne': 197,
    'Audi Q7': 198,
    'Mercedes-Benz GL-Class': 199,
    'Porsche Cayman': 200,
    'BMW X5': 201,
    'BMW Z4': 202,
    'BMW 6': 203,
    'BMW X6': 204,
    'Mercedes-Benz GLC': 205,
    'Mercedes-Benz SLK-Class': 206,
    'Porsche Panamera': 207,
    'Ford Mustang': 208,
    'Bentley Continental': 209,
    'Mercedes-Benz GLE': 210,
    'Porsche Boxster': 211,
    'Jaguar XJ': 212,
    'Mercedes-Benz GLS': 213,
    'Mercedes-Benz SLC': 214,
    'Jaguar F': 215,
    'Lamborghini Gallardo': 216
    }


def home(request):
   
   return render(request, "authentication/index.html")

def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        email = request.POST.get("email")
        pass1 = request.POST.get("pass1")
        pass2 = request.POST.get("pass2")

        error_message = None

        if User.objects.filter(username__iexact=username).exists():
            error_message = f"Username already exists"
        
        if User.objects.filter(email=email).exists():
            error_message = f"Email address already exists" if not error_message else error_message
        
        if len(username)>20:
            error_message = f"Username must be under 20 characters!" if not error_message else error_message

        if len(pass1)<8:
            error_message = f"Password must be above 8 characters!" if not error_message else error_message
            
        if pass1 != pass2:
            error_message = f"Passwords didn't matched!" if not error_message else error_message
        
        if not username.isalnum():
            error_message = f"Username must be Alpha-Numeric!" if not error_message else error_message
        
        if error_message:
            return render(request, 'authentication/signup.html', {'error_message': error_message, 'request': request})

        myuser = User.objects.create_user(username,email,pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_active = False

        myuser.save()
        # messages.success(request, "Your Account has been succesfully created !! Please check your email to confirm your email address in order to activate your account.")

                # Welcome Email
        subject = "Welcome to Carcompanion!!!"
        message = "Hello " + myuser.first_name + "!! \n" + "Welcome to Carcompanion!!! \nThank you for visiting our website\n. We have also sent you a confirmation email, please confirm your email address. \n\nThanking You\nTeam Carcompanion"        
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(
            subject,
            message,
            from_email,
            to_list,
            fail_silently=False,
        )
        # Email Address Confirmation Email
        current_site = get_current_site(request)
        email_subject = "Confirm your Email @ Carcompanion!!"
        message2 = render_to_string('email_confirmation.html',{
            
            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
        })
        email = EmailMessage(
        email_subject,
        message2,
        settings.EMAIL_HOST_USER,
        [myuser.email],
        )
        email.fail_silently = True
        email.send()

        return redirect('signin')



    return render(request, "authentication/signup.html")

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
        
        user = authenticate(username=username, password=pass1)
        
        if user is not None:
            login(request, user)
            fname = user.first_name
            # messages.success(request, "Logged In Sucessfully!!")
            return render(request, "authentication/index.html",{"fname":fname})
        else:
            print("SASDS")
            error_message = f"Invalid Credentials"
            return render(request, "authentication/signin.html",{"error_message":error_message})
    
    return render(request, "authentication/signin.html")

def getPrediction(name, year, kilometer, mileage, engine, owner, transmission, fuel, power, seats):
    rfmodel = pickle.load(open("ml_model.sav", "rb"))
    brmodel = pickle.load(open("bl_model.sav", "rb"))
    lrmodel = pickle.load(open("ll_model.sav", "rb"))
    with open('scaler.sav', 'rb') as f:
        scaled = pickle.load(f)
    encoded = pickle.load(open("oencoder.sav", "rb"))
    modelname = pickle.load(open("carmodel.sav", "rb"))
    
    with open('yscaler.sav', 'rb') as f:
        y_scaler = pickle.load(f)
    
    transformed = scaled.transform(np.array([name, year, kilometer, mileage, engine, owner, transmission, fuel, power, seats]).reshape(1, -1))
    
    prediction1 = y_scaler.inverse_transform(rfmodel.predict(transformed).reshape(-1, 1))[0][0]
    prediction2 = y_scaler.inverse_transform(brmodel.predict(transformed).reshape(-1, 1))[0][0]
    prediction3 = y_scaler.inverse_transform(lrmodel.predict(transformed).reshape(-1, 1))[0][0]
    
    return round(prediction1, 2), round(prediction2, 2), round(prediction3, 2)
    

MIN_MILEAGE = 0
MAX_MILEAGE = 40
MIN_ENGINE = 600
MAX_ENGINE = 6500
MIN_POWER = 40
MAX_POWER = 2000
MIN_SEATS = 2
MAX_SEATS = 10
MIN_YEAR=1
MAX_YEAR=25




def result(request):
    if request.method == 'GET':
        return render(request, "authentication/index.html")
    else:
        name = CAR_MODELS.get(request.POST.get('model'), None)
        if not name:
            error_message = f"{request.POST.get('model')} Model does not exist. Please enter a valid model."
            return render(request, 'authentication/index.html', {'error_message': error_message})
        
        year = request.POST.get('year')
        try:
            year = float(year)
           
            if year < MIN_YEAR or year > MAX_YEAR:
                raise ValidationError("Invalid Year. Year must be between {} and {}.".format(MIN_YEAR, MAX_YEAR))

            kilometer = float(request.POST.get('kilometer'))
            mileage = float(request.POST.get('mileage'))
            engine = float(request.POST.get('engine'))
            owner = request.POST.get('owner')
            transmission = request.POST.get('transmission')
            fuel = request.POST.get('fuel')
            power = float(request.POST.get('power'))
            seats = int(request.POST.get('seats'))
            
            if kilometer < 0 or mileage < MIN_MILEAGE or mileage > MAX_MILEAGE:
                raise ValidationError("Invalid mileage. Mileage must be between {} and {}.".format(MIN_MILEAGE, MAX_MILEAGE))

            if engine < MIN_ENGINE or engine > MAX_ENGINE:
                raise ValidationError("Invalid engine size. Engine size must be between {} and {}.".format(MIN_ENGINE, MAX_ENGINE))

            if power < MIN_POWER or power > MAX_POWER:
                raise ValidationError("Invalid power. Power must be between {} and {}.".format(MIN_POWER, MAX_POWER))

            if seats < MIN_SEATS or seats > MAX_SEATS:
                raise ValidationError("Invalid number of seats. Number of seats must be between {} and {}.".format(MIN_SEATS, MAX_SEATS))

        except ValueError:
            error_message = "Invalid input. Please enter valid values."
            return render(request, 'authentication/index.html', {'error_message': error_message})
        except ValidationError as e:
            error_message = str(e)
            return render(request, 'authentication/index.html', {'error_message': error_message})
        
        data = {
            "model": request.POST.get('model'),
            "year": int(year),
            "kilometer_driven": kilometer,
            "mileage": mileage,
            "engine": engine,
            "owner_type": owner,
            "transmission_type": transmission,
            "fuel_type": fuel,
            "power": power,
            "seat": seats
        }
        
        predictions = getPrediction(int(name), int(year), kilometer, mileage, engine, owner, transmission, fuel, power, seats)
        data["predicted_price1"] = predictions[0]
        data["predicted_price2"] = predictions[1]
        data["predicted_price3"] = predictions[2]
        
        PredictCarModel.objects.create(**data)
        latest_entry = PredictCarModel.objects.latest('id')
        
        predicted_price1 = round(latest_entry.predicted_price1 * 130, 2) if request.POST.get('model') else None
        predicted_price2 = round(latest_entry.predicted_price2 * 130, 2) if request.POST.get('model') else None
        predicted_price3 = round(latest_entry.predicted_price3 * 130, 2) if request.POST.get('model') else None

        return render(request, 'authentication/index.html', {'predicted_price1': predicted_price1, 'predicted_price2': predicted_price2, 'predicted_price3': predicted_price3, 'car_model': latest_entry})


def cars(request):
    if request.method == 'GET' and 'search' in request.GET:
        search = request.GET.get('search')
        predict = PredictCarModel.objects.filter(model__icontains=search).order_by('model')
    else:
        predict = PredictCarModel.objects.all().order_by('model')
        for car in predict:
         car.predicted_price1 *= 130
        for car in predict:
         car.predicted_price2 *= 130
        for car in predict:
         car.predicted_price3 *= 130
    return render(request, 'authentication/cars.html', {'predict': predict})

def searchbar(request):
    if request.method == 'GET' and 'search' in request.GET:
        search = request.GET.get('search')
        post = PredictCarModel.objects.filter(model__icontains=search)
        
        for car in post:
         car.predicted_price *= 130
        return render(request, 'authentication/searchbar.html', {'post': post})
    else:
        return redirect('cars')

def signout(request):
    logout(request)
    messages.success(request,"Logged Out successfully")
    return redirect('home')

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None
    
    if myuser is not None and default_token_generator.check_token(myuser, token):
        myuser.is_active = True
        # user.profile.signup_confirmation = True
        myuser.save()
        login(request, myuser)
        messages.success(request, "Your account has been activated!")
        return redirect('signin')
    else:
        return render(request, 'activation_failed.html')


