import os, sys
import datetime, random

from django.core.management import execute_from_command_line
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "enarocanje.local_settings")

from enarocanje.service.models import Service, Discount, Category
from enarocanje.accountext.models import User, ServiceProvider, Category as ProvCat


# Users
# Password is defined as: admin
'''password = 'pbkdf2_sha256$10000$2SnkDp4Ao8iu$Y3bGOt1yByqmNcKgNPhk/aTB2AfGQSSy12ur/j6nx7k='
name = 'user'
for i in range(2,51):
    obj = User(id=i, password=password, is_superuser=0, username=name+str(i), first_name='User'+str(i), last_name='Cruiser'+str(i), email=name+str(i)+'@gmail.com', is_staff=0, is_active=1, phone='435345',language='en')
    obj.save()
'''

# Provider categories
cat = ["Nega obraza","Nega telesa","Frizerski salon","Kozmeticni salon"]
for i in range(1,len(cat)+1):
    obj = ProvCat(id=i,name=cat[i-1]); obj.save()

# Service categories
cat = ["Negovalni salon","Masazni salon","Manikura, nega rok","Pedikura, nega nog","Depilacija","Solarij","Licenje","Masaza","Frizerske storitve"]
for i in range(1,len(cat)+1):
    obj = Category(id=i,name=cat[i-1]); obj.save()

# Service Providers
'''for i in range(2,51):
    obj = ServiceProvider(id=i, name="Provider"+str(i), street="Strasse"+str(i),zipcode='100'+str(i),city="Cidade"+str(i),country="Cunt-ri"+str(i),category_id=random.randint(1,len(ProvCat.objects.all())));
    obj.save()
    user = User.objects.get(id=i)
    user.service_provider_id = i
    user.save()'''

# Services
# 50 services for each provider
'''durations = [15,30,45,60,75,90,105,120]
description = "Lorem ipsum, brown fox has just had a lift off..."
gender = ['m','f']
id = 1;
for p in ServiceProvider.objects.all():
    for s in range(1,101):
        obj = Service(id=id, service_provider_id=p.id, name="Servisio"+str(s), duration=durations[random.randint(0,len(durations)-1)], description=description, price=round(random.uniform(10, 250),2), sex=gender[random.randint(0,len(gender)-1)], category_id=random.randint(1,len(Category.objects.all())));obj.save()
        id+=1;'''

execute_from_command_line(sys.argv)
