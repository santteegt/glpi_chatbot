FROM rasa/rasa-sdk:2.0.0

WORKDIR /app

COPY actions ./actions
COPY requirements-actions.txt ./

USER root

RUN pip install -U pip && \
    pip install --no-cache-dir -r requirements-actions.txt

USER 1001

CMD ["start", "--actions", "actions", "--debug"]