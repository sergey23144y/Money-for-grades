FROM ubuntu:latest
ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt update \
&& apt install -y python3-pip libjpeg8-dev  nano
RUN pip install --upgrade pip
EXPOSE 7400
COPY ./parsers/ ./
RUN pip install -r req.txt

