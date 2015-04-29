##
# Dockerfile to add self defense to  a Django application
##

FROM ubuntu

MAINTAINER Delta-Force

# Add the application resources URL
RUN echo "deb http://archive.ubuntu.com/ubuntu/ $(lsb_release -sc) main universe" >> /etc/apt/sources.list

# Update the sources list
RUN apt-get update

# Add essitial build tools
RUN apt-get install -y git

# Install Python and Basic Python Tools
RUN apt-get install -y python python-dev python-distribute python-pip

# Install web framework
RUN pip install django

#
#
# CHANGE THIS REPO TO YOUR REPO YOU WANT TO ADD DEFENSE TOO!
# If you project has dependencies place requirements.txt 
# in root of your project, see the following repo as an example
#
#
RUN git clone https://github.com/delta-3/demo-webapp /app
RUN pip install -r /app/requirements.txt

#Inject the depencencies
ADD inject_middleware.py /app/inject_middleware.py
RUN python /app/inject_middleware.py /app


# Install the secure app with middle ware
RUN git clone https://github.com/delta-3/django-auto-repair /defense
RUN pip install -r /defense/requirements.txt
RUN ln -s /defense/secure_app/ /app/

#Build the database for secure app
RUN cd /app
RUN python manage.py syncdb

# Port to expose
EXPOSE 8000

# Set dir where CMD will execute
WORKDIR /app

CMD python manage.py runserver 0.0.0.0:8000


