FROM debian:latest

#install python 3
#ENV PYTHONUNBUFFERED=1
#RUN apk add --update --no-cache python3:3.10 && ln -sf python3 /usr/bin/python
#RUN python3 -m venv ~/.local --system-site-packages
#RUN ~/.local/bin/pip3 install --no-cache --upgrade pip setuptools

RUN apt update && apt -y upgrade

#install python 3 and pip
RUN apt install -y python3
RUN apt install -y python3-pip
RUN apt install -y python3-venv
#RUN python3 -m ensurepip
#RUN python3 -m venv myvenv --without-pip --system-site-packages

RUN python3 -m venv ~/.local --system-site-packages --without-pip
RUN ~/.local/bin/python3 -m pip install --no-cache --upgrade pip setuptools

#install git
RUN apt install -y git

#install chrome?
#RUN apt install wget
#RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
#RUN apt install -y ./google-chrome-stable_current_amd64.deb

#install chromedriver
RUN apt install -y chromium-driver


#git clone the project
RUN git clone https://github.com/WeldFire/Brute-Force-Casino.git

#install requirements of project
#RUN ~/.local/bin/pip3 install -r Brute-Force-Casino/requirements.txt
WORKDIR "/Brute-Force-Casino"
RUN ~/.local/bin/python3 -m pip install -r requirements.txt