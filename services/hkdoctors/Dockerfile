FROM python:3.6
COPY requirements.txt /
RUN pip install -r /requirements.txt
RUN touch /tmp/name_list.txt
COPY . /app
WORKDIR /app
CMD ["sh", "-c","scrapy crawl names; scrapy crawl doctors"]

