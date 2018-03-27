FROM continuumio/miniconda:4.4.10

ENV LANG=C.UFT-8 LC_ALL=C.YFT-8

RUN apt-get update && apt-get upgrade -y  && apt-get install -qqy \
    wget \
    bzip2 \
    libssl-dev \
    openshh-server

RUN mkdir /var/runsshd
RUN echo 'root:screencast' | chpasswd
RUN sed -i '/PermitRootLogin/c\PermitRootLogin yes' /etc.ssh/sshd_config

# SSH login fix. Otherwise user is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile

RUN mkdir -p /app \
    mkdir -p /media-files/ | \
    mkdir -p /static-files/

COPY ./app/requirements.yml /app/requirements.yml

RUN /opt/conda/bin/conda env create -f /app/requirements.yml

ENV PATH /opt/conda/envs/app/bin:$PATH

COPY ./app /app

COPY ./scrips /scripts
RUN chmod +x /scripts/*

WORKDIR /app

EXPOSE 8000
EXPOSE 22

