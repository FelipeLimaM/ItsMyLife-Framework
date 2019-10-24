FROM ubuntu

WORKDIR /code/

RUN \
  sed -i 's/# \(.*multiverse$\)/\1/g' /etc/apt/sources.list && \
  apt-get update && \
  apt-get -y upgrade && \
  apt-get install -y build-essential

RUN apt-get install -y python3 python python-pip python3-pip


RUN pip install --upgrade pip
RUN pip3 install --upgrade pip

COPY requirements.txt ./
RUN pip2 install --no-cache-dir -r requirements.txt
#
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y locales

RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales && \
    update-locale LANG=en_US.UTF-8

ENV LANG en_US.UTF-8

RUN pip3 install pyrebase

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y r-base
