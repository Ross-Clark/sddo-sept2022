FROM python:3.10-buster as backend

ARG POETRY_HOME=/opt/poetry
ARG POETRY_VERSION=1.2.0

RUN useradd sddo -m && mkdir /app && chown sddo /app && mkdir /app/media && chown sddo /app/media

WORKDIR /app

# default environment variables. Used at build time and runtime.
# environment variables on Heroku will override the ones set here.
ENV PATH=$PATH:${POETRY_HOME}/bin \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    DJANGO_SETTINGS_MODULE=core.settings.base \
    PORT=8000 

ARG BUILD_ENV

# Make $BUILD_ENV available at runtime
ENV BUILD_ENV=${BUILD_ENV}

# Port exposed bycontainer. (should match port in path)
EXPOSE 8000

# Install poetry using the installer (keeps Poetry's dependencies isolated from the app's)
RUN wget https://raw.githubusercontent.com/python-poetry/poetry/${POETRY_VERSION}/install-poetry.py && \
    python install-poetry.py && \
    rm install-poetry.py && \
    poetry config virtualenvs.create false

# Install Python requirements

COPY --chown=sddo ./poetry ./poetry

RUN cd ./poetry && if [ "$BUILD_ENV" = "dev" ]; then poetry install --extras gunicorn; else poetry install --no-dev --extras gunicorn; fi; cd ../

# Copy application code.
COPY --chown=sddo ./src ./
COPY --chown=sddo ./media ./media
COPY --chown=sddo ./docker-entrypoint.sh ./initializer-entrypoint.sh  gunicorn-conf.py ./

# Load docker alias'
COPY ./docker/bashrc.sh /home/sddo/.bashrc

USER sddo

RUN python manage.py collectstatic --noinput --clear

CMD gunicorn core.wsgi:application
