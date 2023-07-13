FROM python:3.10-slim

ENV PIP_DISABLE_PIP_VERSION_CHECK=1

COPY requirements.txt /tmp

RUN python -m pip install -U pip &&\
    python -m pip install -r /tmp/requirements.txt &&\
    /bin/rm -f /tmp/requirements.txt &&\
    useradd -ms /bin/bash bsky

USER bsky
WORKDIR /home/bsky/app
COPY ./lib ./lib
COPY ./scripts ./scripts

CMD ["/bin/bash"]
