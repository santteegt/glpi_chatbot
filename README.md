# GLPI Helpdesk bot

AI assistant for the GLPI IT Helpdesk. It includes an integration with its API to open incident reports.

## Supported features
* Login & Auth validation using Google OAuth (TODO) (login)
* Open an incident ticket on GLPI (open_incident)
* Get the current status of a ticket (get_incident_status)
* Reset my password (password_reset)
* Issues with email (problem_email)
* Request biometrics report (request_biometrics_report)
* Request a VM (request_vm)
* FAQ: How to connect to the WiFi? (connect_wifi)
* FAQ: How to create a user? (create_user)

## MISC Intents
* greet
* goodbye
* thank
* bot_challenge
* help
* show_menu
* inform
* confirm
* deny
* out_of_scope

## Lookup Tables
* [Software](data/software-dtic.txt)
* [Faculties](data/faculties.txt)
* [Departments](data/departments.txt)

## Requirements

* Python 3.7+
* Pip3
* Virtualenv or Conda (Recommended for isolated env creation)

## Setup and installation

If you haven’t installed Rasa NLU and Rasa Core yet, you can do it by navigating to the project directory and running:  

```
pip install -r requirements.txt
```

You also need to install the spaCy Spanish language model. You can install it by running:

```
python -m spacy download es_core_news_md
python -m spacy link es_core_news_md es
```

## Development instructions

### Validate training data

```bash
rasa data validate
```

### Training Rasa Core & NLU models

The following command trains both the Core and NLU models

```bash
rasa train
```

### NLU model evaluation

The following command performs a model evaluation of the latest trained NLU model under the `models` directory

```bash
rasa data split nlu
rasa test nlu -u train_test_split/test_data.md --out nlu_metrics/
# or 5 (default -f) cross validation
rasa test nlu -u data/nlu.md --cross-validation --out nlu_metrics/
```

Finally, check the following files for results:
 
* [Intent Confusion Matrix](nlu_metrics/confmat.png) 
* [Intent Confidence Prediction][nlu_metrics/hist.png]
* [Intent/Entity Metrics Report](nlu_metrics/intent_report.json)

Within the [nlu_metrics](nlu_metrics) folder there are also other reportes for each the NLU pipeline components (e.g. DIETClassifier report and errors)

### Dialogue (CORE) model evaluation

The following command performs a model evaluation of the latest trained dialogue model under the `models` directory

```bash
rasa test core --stories tests/e2e-stories.md --out core_metrics/
```

Finally, check the [results](core_metrics/) directory for a summary of the performed evaluation

### Visualizing stories

```bash
rasa visualize -d domain.yml --stories data/stories.md -u data/nlu.md --out core_metrics/graph.html
```
## Chatbot Deployment

### Deploying custom actions locally

```bash
rasa run actions --actions actions -p 5055
```

or as a Docker container

```bash
docker build . --tag glpi-action-server
docker run -p 5055:5055 glpi-action-server
```

or as a background process

```bash
sh scripts/startActions.sh
```

### Deploy DucklingHTTPExtractor (Optional if Enabled on the NLU pipeline)

```bash
docker run -p 8000:8000 rasa/duckling
```

### Test your chatbot locally

```bash
rasa shell --endpoints endpoints.yml
```

### Run Chatbot + Rasa X Locally (*DEPRECATED*)

Rasa X is a tool designed to make it easier to deploy and improve Rasa-powered assistants by learning from real conversations

```bash
rasa x --data data/train/ --endpoints endpoints.yml --cors '*' --enable-api --port 5005 --rasa-x-port 5002
```

or as a background process

```bash
sh scripts/startRasaX.sh
```

Update admin password

```bash
python scripts/manage_user.py create me $RASA_X_PASSWORD admin --update
```

### Deploy the chatbot without RasaX & enabled connection to a web channel through `sockets.io`

```bash
rasa run --endpoints endpoints.yml --credentials credentials.yml --enable-api --cors "*" --port 5005
```

### Deploy the web client

```bash
cd client
npm install
npm start
```

or as a background process

```bash
sh scripts/startClient.sh
```

### Deployment on server

* Install Rasa + RasaX using [Docker Compose Quick Start Guide](https://rasa.com/docs/rasa-x/installation-and-setup/docker-compose-script/#)

* To upgrade the components to their latest release, follow this [instructions](https://rasa.com/docs/rasa-x/installation-and-setup/updating/#docker-compose-quick-install)

* To update the admin password run the following command within `RASA_HOME`

```bash
python rasa_x_commands.py create --update admin me glpi@dmin
```

* Build the Action Server Docker Image (in case you want to build your own locally)

```bash
export GLPI_DOCKER_IMAGE=santteegt/glpi-chatbot-actions:latest
docker build -t $GLPI_DOCKER_IMAGE .
```

* Each time a commit is pushed to the `develop` branch, the DockerHub registry deploys a new image with the latest changes 

* To do a manual push to DockerHub (Optional)

```bash
docker login --username santteegt
docker push $GLPI_DOCKER_IMAGE
```

* Copy `socketio` settings from [credentials.yml](credentials.yml) to the `credentials.yml` file in the `RASA_HOME` directory

* Copy the [docker-compose.override.yml](docker-compose.override.yml) file to the `RASA_HOME` directory

* Set the following environment variables on the `.env` file within the `RASA_HOME` directory

    - GLPI_API_URI: (Setup > General > API) <- where you can find the info on your GLPI instance
    - GLPI_APP_TOKEN: (Setup > General > API)
    - GLPI_AUTH_TOKEN: (User Preferences > API Token)
    - GLPI_LOCALMODE: false (true if you don't want )
    - USERS_API_BASE_URI: e.g. https://cdsdesarrollo.ucuenca.edu.ec:8500/api
    - USERS_API_CLIENT_ID: OAuth Client ID
    - USERS_API_CLIENT_SECRET: OAuth Client Secret

* Start Docker Compose:

```bash
docker-compose up -d
```

* If you started the service for the first time or just updated it, you need to install the ES Spacy language model in both `rasa-production` and `rasa-worker` containers:

```
docker-compose exec -u 0 rasa-production bash -c "python -m spacy download es_core_news_md && python -m spacy link es_core_news_md es"
docker-compose exec -u 0 rasa-worker bash -c "python -m spacy download es_core_news_md && python -m spacy link es_core_news_md es"
```

#### Workaround with connection timeout error when trying to add your Git project to RasaX

1. Access the `rasa-x` container shell

```
docker exec -u 0 -it <rasa-x-container-id> bash
```

1. Add an SSH config file in `/app/.ssh/config` with the following:

```
Host github.com
 Hostname ssh.github.com
 Port 443
```

1. Add `-F /app/.ssh/config` as parameter on the ssh executable script `/usr/local/lib/python3.7/site-packages/rasax/community/services/integrated_version_control/git_service.py`:

```
SSH_SCRIPT f"""#!/bin/sh
ID_RSA={path_to_key}
# Kubernetes tends to reset file permissions on restart. Hence, re-apply the required
# permissions whenever using the key.
chmod 600 $ID_RSA
exec /usr/bin/ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -i $ID_RSA -F /app/.ssh/config "$@"
"""
```

1. Restart the compose environment

## MISC Suggestions / Instructions

### Caveat for using the Webchat client (DEPRECATED)

See this [issue](https://github.com/mrbot-ai/rasa-webchat/issues/28)

```bash
pip install git+git://github.com/RasaHQ/rasa.git

```

### Workaround to make Rasa work if AVX is not compatible with your CPU (DEPRECATED)

You may experience the following error on an on-premise and/or cloud server (deployed with Kubernetes): `The TensorFlow library was compiled to use AVX instructions`

In order to fix this issue, execute the following commands after installing rasa dependencies as shown above:

```bash
pip uninstall tensorflow -y
conda create --name glpi-rasax python=3.6.8
conda activate glpi-rasax
conda install -c anaconda -n glpi-rasax tensorflow==1.15.0
conda deactivate glpi-rasax
export PYTHONPATH='${HOME}/anaconda3/envs/glpi-rasax/lib/python3.6/site-packages'
```

### Prepare dataset for training/testing (DEPRECATED)

If you're (re-)generating data using Chatito, paste the related files under the `data/nlu_chatito` folder and then execute the following commands:

```bash
rasa data convert nlu --data data/nlu_chatito/train/ --out data/train/nlu.md -l es -f md
rasa data convert nlu --data data/nlu_chatito/test/ --out data/test/nlu.md -l es -f md
```