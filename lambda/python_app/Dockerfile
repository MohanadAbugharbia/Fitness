ARG ARCH
ARG PYTHON_VERSION=3.11
FROM ${ARCH}python:${PYTHON_VERSION}

SHELL [ "/bin/bash", "-c" ]

EXPOSE 8080

ENV VIRTUAL_ENV=/opt/fitness/venv
ENV PATH=$VIRTUAL_ENV/bin:$PATH

RUN /usr/sbin/addgroup fitness \
    && /usr/sbin/adduser --system --shell /bin/bash --home /var/lib/fitness fitness \
    && echo 'source /opt/fitness/venv/bin/activate' >> /var/lib/fitness/.bashrc \
    && mkdir -p /opt/fitness \
    && chown -R fitness:fitness /opt/fitness

USER fitness

ADD ./requirements.txt /tmp/requirements.txt
RUN python -m venv $VIRTUAL_ENV && pip install -r /tmp/requirements.txt


ADD ./run.py /opt/fitness/run.py
COPY ./Fitness $VIRTUAL_ENV/lib/python${PYTHON_VERSION}/site-packages/Fitness
COPY ./tools $VIRTUAL_ENV/lib/python${PYTHON_VERSION}/site-packages/tools




CMD [ "python", "/opt/fitness/run.py" ]