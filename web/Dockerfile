FROM python
COPY requirements.txt /home
RUN pip install -r /home/requirements.txt
COPY  ./static /home/myapp/static/
COPY  ./templates /home/myapp/templates/
COPY  app.py /home/myapp/
EXPOSE 8080
CMD python /home/myapp/app.py
