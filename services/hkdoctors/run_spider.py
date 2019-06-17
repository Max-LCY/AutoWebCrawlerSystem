import subprocess

subprocess.call('scrapy crawl names', cwd = './FYP/services/hkdoctors/', shell = True) 
subprocess.call('scrapy crawl doctors', cwd = './FYP/services/hkdoctors/', shell = True) 
