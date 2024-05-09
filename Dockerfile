FROM python:3.12-slim
MAINTAINER Kevin Coakley <kcoakley@sdsc.edu>

COPY . /winearth
WORKDIR /winearth

RUN pip install -r requirements.txt
RUN pip install .

RUN rm -rf /winearth

RUN groupadd -g 999 winearth && \
    useradd -r -u 999 -g winearth winearth

USER winearth

CMD winearth-download