FROM python:3.11-alpine

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

ADD main.py /main.py
ENV PYTHONPATH /
CMD ["python main.py"]
#ENTRYPOINT [ "python main.py" ]

#COPY . /app
#RUN chmod +x /app/coverage_commenter/entrypoint.sh
#ENTRYPOINT ["/app/coverage_commenter/entrypoint.sh"]

