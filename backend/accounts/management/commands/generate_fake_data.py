# from django.core.management.base import BaseCommand
# from accounts.models import Profile
# from accounts.models import CustomUser as User
# from home.models import Education
# from faker import Faker
# import random


# class Command(BaseCommand):
#     help = 'Generate fake data for testing'

#     def add_arguments(self, parser):
#         parser.add_argument(
#             'total', type=int, help='Indicates the number of fake profiles to be created')

#     def handle(self, *args, **kwargs):
#         total = kwargs['total']
#         fake = Faker()

#         for _ in range(total):
#             # Create a fake user
#             username = fake.user_name()
#             email = fake.email()
#             first_name = fake.first_name()
#             last_name = fake.last_name()
#             password = 'pass@123'
#             user = User.objects.create_user(
#                 username=username, email=email, first_name=first_name, last_name=last_name, password=password)

#             # Create a fake profile
#             name = fake.name()
#             locale = fake.locale()
#             headline = fake.sentence()
#             date_of_birth = fake.date_of_birth()
#             address = fake.address()
#             # Ensure phone number length doesn't exceed 15 characters
#             phone_number = fake.phone_number()[:15]
#             profile = Profile.objects.create(user=user, name=name, email=email, locale=locale, headline=headline,
#                                              date_of_birth=date_of_birth, address=address, phone_number=phone_number)

#             # Create fake education data
#             for _ in range(random.randint(1, 5)):
#                 level = random.choice(
#                     [choice[0] for choice in Education.EducationLevel.choices])
#                 marks_or_cgpa = round(random.uniform(50, 100), 2)
#                 year_of_passing = fake.date_between(
#                     start_date='-10y', end_date='today')
#                 board_or_university = fake.company()
#                 degree = fake.job()
#                 Education.objects.create(profile=profile, level=level, marks_or_cgpa=marks_or_cgpa,
#                                          year_of_passing=year_of_passing, board_or_university=board_or_university,
#                                          degree=degree)

#         self.stdout.write(self.style.SUCCESS(
#             f'{total} fake profiles created successfully'))
# from django.core.management.base import BaseCommand
# from accounts.models import Profile
# from accounts.models import CustomUser as User
# from home.models import Education
# from faker import Faker
# import random


# class Command(BaseCommand):
#     help = 'Generate fake data for testing'

#     def add_arguments(self, parser):
#         parser.add_argument(
#             'total', type=int, help='Indicates the number of fake profiles to be created')

#     def handle(self, *args, **kwargs):
#         total = kwargs['total']
#         fake = Faker()

#         for _ in range(total):
#             # Create a fake user
#             username = fake.user_name()
#             email = fake.email()
#             first_name = fake.first_name()
#             last_name = fake.last_name()
#             password = 'pass@123'
#             user = User.objects.create_user(
#                 username=username, email=email, first_name=first_name, last_name=last_name, password=password)

#             # Create a fake profile
#             name = fake.name()
#             locale = fake.locale()
#             headline = fake.sentence()
#             date_of_birth = fake.date_of_birth()
#             address = fake.address()
#             # Ensure phone number length doesn't exceed 15 characters
#             phone_number = fake.phone_number()[:15]
#             profile = Profile.objects.create(user=user, name=name, email=email, locale=locale, headline=headline,
#                                              date_of_birth=date_of_birth, address=address, phone_number=phone_number)

#             # Create fake education data
#             for _ in range(random.randint(1, 5)):
#                 level = random.choice(
#                     [choice[0] for choice in Education.EducationLevel.choices])
#                 marks_or_cgpa = round(random.uniform(50, 100), 2)
#                 year_of_passing = fake.date_between(
#                     start_date='-10y', end_date='today')
#                 board_or_university = fake.company()
#                 degree = fake.job()
#                 Education.objects.create(profile=profile, level=level, marks_or_cgpa=marks_or_cgpa,
#                                          year_of_passing=year_of_passing, board_or_university=board_or_university,
#                                          degree=degree)

#         self.stdout.write(self.style.SUCCESS(
#             f'{total} fake profiles created successfully'))
