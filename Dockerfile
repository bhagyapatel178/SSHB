FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    python3-dev \
    python3-pip \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libportmidi-dev \
    libswscale-dev \
    libavformat-dev \
    libavcodec-dev \
    zlib1g-dev \
    libgstreamer1.0-dev \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-bad \
    gstreamer1.0-plugins-ugly \
    gstreamer1.0-libav \
    gstreamer1.0-tools \
    libmtdev-dev \
    libgl1-mesa-dev \
    x11-xserver-utils \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

ENV DISPLAY=:0
ENV KIVY_NO_CONFIG=1
ENV KIVY_NO_CONSOLELOG=1

WORKDIR /app

COPY . /app

COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip 
RUN pip install -r /app/requirements.txt 

EXPOSE 65432

CMD ["sh", "-c", "python3 SSH_backend1.py & python3 SSHB_frontend.py"]