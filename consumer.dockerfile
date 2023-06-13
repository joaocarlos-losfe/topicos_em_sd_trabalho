FROM ubuntu:22.04
RUN apt update
RUN apt install python3 -y
RUN apt install python3-pip -y
WORKDIR /user/app/src
COPY consumer ./