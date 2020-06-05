FROM rasa/rasa-sdk:1.10.0

WORKDIR /app

COPY actions ./actions
COPY requirements-actions.txt ./

USER root

RUN pip install -U pip && \
    pip install --no-cache-dir -r requirements-actions.txt

RUN echo "172.16.0.44 srvpruebas.ucuenca.edu.ec" >> /etc/hosts

USER 1001

CMD ["start", "--actions", "actions", "--debug"]