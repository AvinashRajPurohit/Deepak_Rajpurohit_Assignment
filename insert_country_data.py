import pandas as pd
import os

from project import settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

from django import setup as django_setup
django_setup()
from users.models import Country, City

FILE_PATH = settings.BASE_DIR / '100_country.csv'

df = pd.read_csv(FILE_PATH)
CITY = list(df["1"])
COUNTRY = list(df["2"])

def insert_data_in_country(country_list):
  """
  This function will insert data in country
  country_list: list
  """
  for c in country_list:
    Country.objects.get_or_create(name=c)

  print("country data has been inserted")
  

def insert_data_in_city(city_list, country_list):
  """
  This function will insert data in city
  city_list: list
  country_list: list
  """
  for country, city in zip(country_list, city_list):
    country_obj = Country.objects.get(name=country)
    City.objects.get_or_create(country=country_obj, name=city)

  print("city data has been inserted")


insert_data_in_country(COUNTRY)

insert_data_in_city(CITY, COUNTRY)


