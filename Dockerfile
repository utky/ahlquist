FROM python:2.7

ENV AHLQUIST_PORT 8080
ENV AHLQUIST_PLAYBOOKS /playbooks

RUN apt-get -y update && apt-get -y install sshpass
RUN curl https://bootstrap.pypa.io/get-pip.py | python
RUN git clone https://github.com/utky/ahlquist.git /var/lib/ahlquist
RUN pip install -r /var/lib/ahlquist/requirements.txt

VOLUME /playbooks
VOLUME /inventory

ENTRYPOINT /var/lib/ahlquist/main
