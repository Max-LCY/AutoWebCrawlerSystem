# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import boto3
import os
from elasticsearch import Elasticsearch, RequestsHttpConnection, helpers
from requests_aws4auth import AWS4Auth
from elasticsearch_dsl import Document, Date, Integer, Keyword, Text, connections
#from importlib import reload
#import sys

class HkdoctorsPipeline(object):
    
    es_host = os.environ['ES']
    db_table = os.environ['HKTABLE']
    region = os.environ['REGION']
    
    boto3Session = boto3.Session()
    credentials = boto3Session.get_credentials()

    awsauth = AWS4Auth(
        credentials.access_key, 
        credentials.secret_key, 
        'us-east-1', 
        'es', 
        session_token=credentials.token)
        
    es = connections.create_connection(
        hosts= es_host,
        port = 443,
        http_auth=awsauth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection
        )
    
    count = 0
    
    def open_spider(self, spider):
        self.dynamodb = boto3.client('dynamodb', region_name='us-east-1')
    
    def process_item(self, item, spider):
        self.spider2db(item, self.db_table)
        self.spider2es(item)
        self.count+=1
        return item
    
    def spider2db(self,item, table):
        Itm={}
        for key in item:
            Itm[key]= {}
            Itm[key]['S'] = item[key]
            
        # Table="test"
        self.dynamodb.put_item(TableName=table, Item=Itm)
        
    def spider2es(self,item):
        Itm={}
        for key in item:
            Itm[key]= item[key]
        
        class Hkdoctor(Document):
            name = Text(fields={'raw': Keyword()})
            medical_procedures_and_operations = Text(fields={'raw': Keyword()})
            url = Text(fields={'raw': Keyword()})
            gender = Text(fields={'raw': Keyword()})
            qualifications = Text(fields={'raw': Keyword()})
            specialty= Text(fields={'raw': Keyword()})
            registered_address= Text(fields={'raw': Keyword()})
            district= Text(fields={'raw': Keyword()})
            type_of_practice= Text(fields={'raw': Keyword()})
            consultation_hours= Text(fields={'raw': Keyword()})
            emergency_service_available= Text(fields={'raw': Keyword()})
            consultation_fee = Text(fields={'raw': Keyword()})
            languages_or_dialects_spoken = Text(fields={'raw': Keyword()})
            medical_services_available = Text(fields={'raw': Keyword()})
            medical_services_provided_other_than_in_the_office = Text(fields={'raw': Keyword()})
            affiliated_hospitals = Text(fields={'raw': Keyword()})
            telephone = Text(fields={'raw': Keyword()})
            fax = Text(fields={'raw': Keyword()})
            pager = Text(fields={'raw': Keyword()})
            mobile_phone = Text(fields={'raw': Keyword()})
            email = Text(fields={'raw': Keyword()})
            create_time = Date()    
            class Index:
                name = 'hkdoctor-index'
        
        Hkdoctor.init()
        hkdoctor = Hkdoctor(meta={'id': self.count}, Body = Itm)
        hkdoctor.save()
    