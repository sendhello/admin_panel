FROM python:3.11.1

ENV DJANGO_SETTINGS_MODULE='config.settings' \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \

    APP_PATH='/opt/app'

WORKDIR $APP_PATH
RUN mkdir -p $APP_PATH/static

RUN apt-get update && apt-get install -y --no-install-recommends gettext

COPY ./requirements.txt .
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' $APP_PATH/entrypoint.sh
RUN chmod +x $APP_PATH/entrypoint.sh

# install dependencies
RUN  pip install --upgrade pip && pip install  --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

ENTRYPOINT sh /opt/app/entrypoint.sh
