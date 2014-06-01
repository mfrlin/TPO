# -*- coding: utf-8 -*-
import os, sys
import datetime, random
from dateutil.relativedelta import relativedelta
from django.conf import settings

from django.core.management import execute_from_command_line

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "enarocanje.settings")

from django.contrib.sites.models import Site
from enarocanje.service.models import Service, Discount, Category
from enarocanje.accountext.models import User, ServiceProvider, Category as ProvCat
from enarocanje.workinghours.models import WorkingHours, EmployeeWorkingHours
from enarocanje.customers.models import Customer
from enarocanje.employees.models import Employee


def fillDatabase():
    # Users
    # Password is defined as: admin

    password = 'pbkdf2_sha256$10000$2SnkDp4Ao8iu$Y3bGOt1yByqmNcKgNPhk/aTB2AfGQSSy12ur/j6nx7k='
    name = 'admin'
    obj = User(id=666, password=password, is_superuser=1, username=name, first_name='Admin',
               email=name + '@gmail.com', is_staff=1, is_active=1,
               phone='435345', language='en')
    obj.save()

    password = 'pbkdf2_sha256$10000$2SnkDp4Ao8iu$Y3bGOt1yByqmNcKgNPhk/aTB2AfGQSSy12ur/j6nx7k='
    name = 'user'
    for i in range(1, 11):
        obj = User(id=i, password=password, is_superuser=0, username=name + str(i), first_name='John',
                   last_name='Doe ' + str(i), email=name + str(i) + '@gmail.com', is_staff=0, is_active=1,
                   phone='435345', language='en', notification_type=1)
        obj.save()


    # Provider categories
    #cat = ["Nega obraza", "Nega telesa", "Frizerski salon", "Kozmeticni salon"]
    #generic = ["", "massage_salon", "hairdresser_salon", "cosmetic_salon"]
    cat = ["Nega telesa", "Frizerski salon", "Kozmetični salon"]
    generic = ["massage_salon", "hairdresser_salon", "cosmetic_salon"]
    for i in range(1, len(cat) + 1):
        obj = ProvCat(id=i, name=cat[i - 1], generic_gallery=generic[i - 1])
        obj.save()

    # Service categories
    cat = ["Negovalni salon", "Masažni salon", "Manikura, nega rok", "Pedikura, nega nog", "Depilacija", "Solarij",
           "Ličenje", "Masaža", "Frizerske storitve", "Fotografske storitve"]
    for i in range(1, len(cat) + 1):
        obj = Category(id=i, name=cat[i - 1], show_in_gallery=False)
        if obj.name == "Fotografske storitve":
            obj.show_in_gallery = True
        obj.save()

    # Service Providers
    int_list = "1,2,3,4,5"
    for i in range(2, 10):
        obj = ServiceProvider(id=i, name="Provider" + str(i - 1), street="Strasse" + str(i - 1),
                              zipcode='100' + str(i - 1),
                              city="City" + str(i - 1), country="Country" + str(i - 1),
                              category_id=random.randint(1, len(ProvCat.objects.all())), subscription_mail_sent=0,
                              reservation_confirmation_needed=0, display_generic_gallery=True,
                              userpage_link="Provider" + str(i - 1))
        obj.save()
        user = User.objects.get(id=i)
        user.service_provider_id = i
        user.save()

        #Add working hours on weekdays (9h-21h)
        h = WorkingHours()
        h.service_provider = obj
        h.time_from = datetime.time(9)
        h.time_to = datetime.time(21)
        h.week_days = int_list
        h.save()

    # Services
    # 10 services for each provider
    durations = [15, 30, 45, 60, 75, 90, 105, 120]
    discounts = [10, 15, 30, 50, 70, 90, 100]
    gender = ['m', 'f']
    id = 1
    for p in ServiceProvider.objects.all():
        for s in range(1, 11):
            obj = Service(id=id, service_provider_id=p.id, name="Service" + str(s),
                          duration=durations[random.randint(0, len(durations) - 1)],
                          price=round(random.uniform(10, 250), 2), sex=gender[random.randint(0, len(gender) - 1)],
                          category_id=random.randint(1, len(Category.objects.all())))
            obj.description = str(Category.objects.get(id=obj.category_id))
            if random.uniform(1, 100):
                disc = Discount(discount=discounts[random.randint(0, len(discounts) - 1)], service=obj,
                                valid_from=datetime.date.today(),
                                valid_to=datetime.date.today() + relativedelta(months=1))
                disc.save()
            obj.save()
            id += 1

    #some employees
    for p in ServiceProvider.objects.all():
        for s in range(1, 11):
            e = Employee(name="Name" + str(s), surname="Surname" + str(s), phone=random.randint(100000, 999999),
                         employer=p)
            e.save()
            h = EmployeeWorkingHours()
            h.employee = e
            h.time_from = datetime.time(9)
            h.time_to = datetime.time(21)
            h.week_days = "1,2,3,4,5"
            h.save()
            name = "Customer_"+str(s)
            c = Customer(name=name, service=p,
                         phone=random.randint(100000, 999999), email=name + '@gmail.com',
                         last_reservation=datetime.datetime.now())
            c.save()


#fillDatabase()
# user1 is a customer
# users 2-9 are service providers
# admin is staff and superuser
# pass is admin

# default site, for password reset
site = Site.objects.all()[0]
name = settings.PRODUCTION_URL.split('//')[1]
site.domain = name
site.name = name
site.save()

from allauth.socialaccount.models import SocialApp

fb = SocialApp()
fb.provider = "facebook"
fb.name = "Facebook"
fb.client_id = "207371922661306"
fb.key = ''
fb.secret = "67e595cb85d9836c305fe4b9985180df"
fb.save()

g = SocialApp()
g.provider = "google"
g.name = "Google"
g.client_id = "236816371004-c46h64qimvsqffbrdt8k5o5hq90iigjh.apps.googleusercontent.com"
g.key = ''
g.secret = "n6NuvZ1_jAqKq_r6V6pWQ8Ii"
g.save()


#execute_from_command_line(sys.argv)




