FROM python:3.11.1

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \

    APP_PATH='/opt/app'

WORKDIR $APP_PATH

COPY ./requirements.txt .
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' $APP_PATH/entrypoint.sh
RUN chmod +x $APP_PATH/entrypoint.sh

# install dependencies
RUN  pip install --upgrade pip && pip install  --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT sh /opt/app/entrypoint.sh
