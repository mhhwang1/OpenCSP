ARG BASE_IMAGE_ARG=registry.access.redhat.com/ubi8:latest
FROM ${BASE_IMAGE_ARG}

RUN yum -y install python3.11 \
    python3.11-pip \
    mesa-libGL \
    python3.11-tkinter \
    python3-xvfbwrapper \
    xz

# Installing ffmpeg via relies on the rpmfusion repo and SDL2
# The SDL2 yum package is not currently available in ubi8
# Consequently, we download and install ffmpeg as a statically
# linked binary below.
WORKDIR /code
RUN curl -O https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz
RUN tar -xf ffmpeg-*-amd64-static.tar.xz && \
    cp /code/ffmpeg-*-amd64-static/ffmpeg /usr/local/bin && \
    cp /code/ffmpeg-*-amd64-static/ffprobe /usr/local/bin    

ENV PYTHONPATH=/code

COPY requirements.txt /code/
RUN python3 -m pip install -r requirements.txt