import os, sys
import datetime, random
from dateutil.relativedelta import relativedelta

from django.core.management import execute_from_command_line

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "enarocanje.settings")

from enarocanje.service.models import Service, Discount, Category
from enarocanje.accountext.models import User, ServiceProvider, Category as ProvCat
from enarocanje.workinghours.models import WorkingHours


def fillDatabase():
    # Users
    # Password is defined as: admin

    password = 'pbkdf2_sha256$10000$2SnkDp4Ao8iu$Y3bGOt1yByqmNcKgNPhk/aTB2AfGQSSy12ur/j6nx7k='
    name = 'user'
    for i in range(1, 11):
        obj = User(id=i, password=password, is_superuser=0, username=name + str(i), first_name='John',
                   last_name='Doe ' + str(i), email=name + str(i) + '@gmail.com', is_staff=0, is_active=1,
                   phone='435345', language='en')
        obj.save()


    # Provider categories
    #cat = ["Nega obraza", "Nega telesa", "Frizerski salon", "Kozmeticni salon"]
    #generic = ["", "massage_salon", "hairdresser_salon", "cosmetic_salon"]
    cat = ["Nega telesa", "Frizerski salon", "Kozmeticni salon"]
    generic = ["massage_salon", "hairdresser_salon", "cosmetic_salon"]
    for i in range(1, len(cat) + 1):
        obj = ProvCat(id=i, name=cat[i - 1], generic_gallery=generic[i - 1])
        obj.save()

    # Service categories
    cat = ["Negovalni salon", "Masazni salon", "Manikura, nega rok", "Pedikura, nega nog", "Depilacija", "Solarij",
           "Licenje", "Masaza", "Frizerske storitve"]
    for i in range(1, len(cat) + 1):
        obj = Category(id=i, name=cat[i - 1], show_in_gallery=True)
        obj.save()

    # Service Providers
    int_list = "1,2,3,4,5"
    for i in range(2, 10):
        obj = ServiceProvider(id=i, name="Provider" + str(i - 1), street="Strasse" + str(i-1), zipcode='100' + str(i-1),
                              city="City" + str(i-1), country="Country" + str(i-1),
                              category_id=random.randint(1, len(ProvCat.objects.all())), subscription_mail_sent=0,
                              reservation_confirmation_needed=0, display_generic_gallery=True)
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
    # 50 services for each provider
    durations = [15, 30, 45, 60, 75, 90, 105, 120]
    discounts = [10, 15, 30, 50, 70, 90, 100]
    description = "Lorem ipsum, brown fox has just had a lift off..."
    gender = ['m', 'f']
    id = 1
    for p in ServiceProvider.objects.all():
        for s in range(1, 11):
            obj = Service(id=id, service_provider_id=p.id, name="Service" + str(s),
                          duration=durations[random.randint(0, len(durations) - 1)], description=description,
                          price=round(random.uniform(10, 250), 2), sex=gender[random.randint(0, len(gender) - 1)],
                          category_id=random.randint(1, len(Category.objects.all())))
            if random.uniform(1, 100):
                disc = Discount(discount=discounts[random.randint(0, len(discounts) - 1)], service=obj,
                                valid_from=datetime.date.today(),
                                valid_to=datetime.date.today() + relativedelta(months=1))
                disc.save()
            obj.save()
            id += 1


fillDatabase()
# user1 is a customer
# users 2-9 are service providers

execute_from_command_line(sys.argv)




