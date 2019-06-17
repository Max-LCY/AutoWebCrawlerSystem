# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst, MapCompose, Join

class HkdoctorsItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    medical_procedures_and_operations = scrapy.Field(output_processor=Join())
    url = scrapy.Field()
    gender = scrapy.Field()
    qualifications = scrapy.Field()
    specialty= scrapy.Field()
    registered_address= scrapy.Field(output_processor=Join())
    district= scrapy.Field()
    type_of_practice= scrapy.Field()
    consultation_hours= scrapy.Field(output_processor=Join())
    emergency_service_available= scrapy.Field()
    consultation_fee = scrapy.Field()
    languages_or_dialects_spoken = scrapy.Field()
    medical_services_available = scrapy.Field(output_processor=Join())
    medical_services_provided_other_than_in_the_office = scrapy.Field(output_processor=Join())
    affiliated_hospitals = scrapy.Field()
    telephone = scrapy.Field()
    fax = scrapy.Field()
    pager = scrapy.Field()
    mobile_phone = scrapy.Field()
    email = scrapy.Field()
