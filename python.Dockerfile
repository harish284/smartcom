#parent of the official image
FROM python:3.9

#working directory
WORKDIR  /python-app

#copy
COPY . .

#run
RUN pip install -r requirement.txt


#port
EXPOSE 5000

#cmd
CMD ["python", "app.py"]
