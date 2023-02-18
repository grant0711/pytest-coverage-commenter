FROM alpine:3.11 as base

FROM base as builder

RUN mkdir /install
WORKDIR /install

RUN apk add --no-cache python3 py3-pip
#      gcc \
#      libffi-dev \
#      linux-headers \
#      musl-dev \
#      postgresql-client

ENV PYTHONDONTWRITEBYTECODE=1
#ENV PYTHONUNBUFFERED=1

RUN python -m pip install --upgrade pip
RUN pip install pipenv --user
ENV PATH="/root/.local/bin:$PATH"

FROM builder as venv

COPY Pipfile /Pipfile
COPY Pipfile.lock /Pipfile.lock
RUN PIPENV_VENV_IN_PROJECT=1 pipenv sync

FROM base

COPY --from=builder /root/.local /usr/local
COPY --from=venv /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

COPY . /app
WORKDIR /app


#COPY . /app
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]

