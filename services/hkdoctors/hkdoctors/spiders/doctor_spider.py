import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose
from hkdoctors.items import HkdoctorsItem
from lxml import html
from w3lib.html import remove_tags, replace_escape_chars


class DoctorSpider(scrapy.Spider):
    name = "doctors"

    def start_requests(self):
        with open('/tmp/name_list.txt', 'r') as f:
            links = f.readlines()
        urls = list(map(lambda x: "http://www.hkdoctor.org/english/" + x, links))
        for url in urls:
            yield scrapy.FormRequest(url=url, callback=self.parse,
                                     headers={'Referer': 'http://www.hkdoctor.org/english/docsearch1.asp"'})

    def parse(self, response):
        # Removing HTML tags from the data
        doctor = ItemLoader(item=HkdoctorsItem(), response=response)
        doctor.default_input_processor = MapCompose(remove_tags, replace_escape_chars)
        doctor.default_output_processor = TakeFirst()
        
        doctor.add_value("url", response.url)
        doctor.add_xpath("name", "normalize-space(/html/body/form/table/tr[2]/td/font/text())")

        
        confirm = False
        
        for i in range(0,24):
            xpath = "/html/body/form/table/tr[%s]/td[1]/b/text()" % (i)
            value = doctor.get_xpath(xpath, TakeFirst())
            
            if value == "Gender:":
                doctor.add_xpath('gender', "/html/body/form/table/tr[%s]/td[2]/text()" % (i))
            
            elif value == "Qualifications:":
                doctor.add_xpath('qualifications', "/html/body/form/table/tr[%s]/td[2]/text()" % (i))
                if i == 5:
                    confirm = True
                    
            elif value == "Registered Address:":
                doctor.add_xpath('registered_address', "/html/body/form/table/tr[%s]/td[2]/text()" % (i))
                if i == 7 and confirm:
                    doctor.add_xpath('specialty', "/html/body/form/table/tr[6]/td[2]/font/a/text()")
                    
            elif value == "District:":
                doctor.add_xpath('district', "/html/body/form/table/tr[%s]/td[2]/text()" % (i))
            
            elif value == "Type of Practice:":
                doctor.add_xpath('type_of_practice', "/html/body/form/table/tr[%s]/td[2]/text()" % (i))
            
            elif value == "Consultation Hours:":
                doctor.add_xpath('consultation_hours', "/html/body/form/table/tr[%s]/td[2]/table//text()[normalize-space()]" % (i))

            elif value == "Emergency Service Available:":
                doctor.add_xpath('emergency_service_available', "/html/body/form/table/tr[%s]/td[2]/text()" % (i))
                
            elif value == "Consultation Fee:":
                doctor.add_xpath('consultation_fee', "/html/body/form/table/tr[%s]/td[2]/text()" % (i))
                
            elif value == "Language(s) / Dialect(s) Spoken:":
                doctor.add_xpath('languages_or_dialects_spoken', "normalize-space(/html/body/form/table/tr[%s]/td[2]/text())" % i)
                
            elif value == "Medical Services Available:":
                doctor.add_xpath('medical_services_available', "/html/body/form/table/tr[%s]/td[2]/text()" % i)
                
            elif value == "Medical Services Provided Other Than in the Office:":
                doctor.add_xpath('medical_services_provided_other_than_in_the_office', "/html/body/form/table/tr[%s]/td[2]/text()" % i)
                
            elif value == "Medical Procedures and Operations:":
                doctor.add_xpath('medical_procedures_and_operations', "/html/body/form/table//tr[%s]/td[2]/text()" % i)
                
            elif value == "Affiliated Hospitals:":
                doctor.add_xpath('affiliated_hospitals', "/html/body/form/table/tr[%s]/td[2]/text()" %  i)
                
            elif value == "Telephone:":
                doctor.add_xpath('telephone', "/html/body/form/table/tr[%s]/td[2]/text()" %  i)
                
            elif value == "Fax:":
                doctor.add_xpath('fax', "/html/body/form/table/tr[%s]/td[2]/text()" %  i)
                
            elif value == "Pager:":
                doctor.add_xpath('pager', "/html/body/form/table/tr[%s]/td[2]/text()" %  i)
                
            elif value == "Mobile Phone:":
                doctor.add_xpath('mobile_phone', "/html/body/form/table/tr[%s]/td[2]/text()" %  i)
                
            elif value == "Email:":
                doctor.add_xpath('email', "/html/body/form/table/tr[%s]/td[2]/a/text()" %  i)
                
        yield doctor.load_item()
