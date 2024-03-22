FROM python:3.12-slim
RUN apt-get update -y && apt-get install --no-install-recommends -y gcc libpq-dev python3-dev

ENV APP_HOME=/app
WORKDIR ${APP_HOME}
ADD requirements.txt .

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

CMD bash -c "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"
