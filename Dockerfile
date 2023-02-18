FROM python:3.11-slim AS builder
ADD . /app
WORKDIR /app

# We are installing a dependency here directly into our app source dir
RUN pip install --target=/app requests

# A distroless container image with Python and some basics like SSL certificates
# https://github.com/GoogleContainerTools/distroless
FROM gcr.io/distroless/python3-debian10
COPY --from=builder /app /app
WORKDIR /app
ENV PYTHONPATH /app
CMD ["/app/main.py"]



#FROM python:3.11-alpine as builder
#ADD . /app
#WORKDIR /app
#FROM base as builder

#RUN mkdir /install
#WORKDIR /install

#RUN apk add --no-cache \ 
#      gcc \
#      libffi-dev \
#      linux-headers \
#      musl-dev
#      postgresql-client

#ENV PYTHONDONTWRITEBYTECODE=1
#ENV PYTHONUNBUFFERED=1

#RUN python -m pip install --upgrade pip
#RUN pip install pipenv --user
#ENV PATH="/root/.local/bin:$PATH"

#FROM builder as venv

#COPY Pipfile /Pipfile
#COPY Pipfile.lock /Pipfile.lock
#RUN PIPENV_VENV_IN_PROJECT=1 pipenv sync

#FROM base

#COPY --from=builder /root/.local /usr/local
#COPY --from=venv /.venv /.venv
#ENV PATH="/.venv/bin:$PATH"

#COPY . /app/coverage_commenter
#WORKDIR /app
#ADD . /app
#WORKDIR /app
#ADD main.py /main.py
#COPY --from=builder /app /app
#ENV PYTHONPATH /app
#CMD ["/app/main.py"]
#ENTRYPOINT [ "python main.py" ]

#COPY . /app
#RUN chmod +x /app/coverage_commenter/entrypoint.sh
#ENTRYPOINT ["/app/coverage_commenter/entrypoint.sh"]

