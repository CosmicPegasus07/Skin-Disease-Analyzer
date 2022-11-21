FROM python:3.10-slim

RUN useradd management

WORKDIR /home/management

COPY requirements.txt requirements.txt

RUN python -m venv env
RUN env/bin/pip install -r requirements.txt

COPY  Examples Examples
COPY  Models Models
COPY  static static
COPY  templates templates
COPY app.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP app.py
ENV ASSETS_ROOT /static/assets

RUN chown -R management:management ./
USER management

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]