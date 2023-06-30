FROM python:3.11.4-slim-bullseye
WORKDIR /srv/fuel
ADD ./flask/requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
ADD ./flask ./

COPY entrypoint.sh ./entrypoint.sh

RUN groupadd -g 1000 fuel && \
useradd -u 1000 -g fuel -s /bin/sh --home-dir /srv/fuel -m fuel && \
chown -R fuel:fuel /srv/fuel

ENTRYPOINT ["/srv/fuel/entrypoint.sh"]

CMD ["python", "/srv/fuel/main.py"]
