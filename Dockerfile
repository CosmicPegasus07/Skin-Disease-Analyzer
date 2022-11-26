FROM python:3.10

RUN useradd skin

WORKDIR /home/skin

RUN apt-get update
RUN python -m pip install --upgrade pip
RUN apt install -y libgl1 

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY Models/vgg19byzeeza.h5 Models/vgg19byzeeza.h5
COPY static static
COPY templates templates
COPY app.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP app.py
ENV ASSETS_ROOT /static/assets

RUN chown -R skin:skin ./
USER skin

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]