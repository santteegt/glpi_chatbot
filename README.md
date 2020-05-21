# GLPI Helpdesk bot

Looked through the [Rasa NLU](http://rasa.com/docs/nlu/) and [Rasa Core](http://rasa.com/docs/core/) documentation and ready to build your first intelligent assistant? We have some resources to help you get started! This repository contains the foundations of your first custom assistant. This starter-pack also comes with a step-by-step video tutorial which you can find [here](https://youtu.be/lQZ_x0LRUbI).  

This starter-pack comes with a small amount of training data which lets you build a simple assistant. **You can find more training data here in the [forum](https://forum.rasa.com/t/grab-the-nlu-training-dataset-and-starter-packs/903) and use it to teach your assistant new skills and make it more engaging.**

We would recommend downloading this before getting started, although the tutorial will also work with just the data in this repo. 

The initial version of this starter-pack lets you build a simple assistant capable of cheering you up with Chuck Norris jokes.


<p align="center">
  <img src="./rasa-stack-mockup.gif">
</p>

## Supported features
* Login & Auth validation using Google OAuth (TODO) (login)
* Open an incident ticket on GLPI (open_incident)
* Get the current status of a ticket (TODO)
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
* [software](data/software-dtic.txt)

## Requirements

* Python 3.6.8+
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

## Caveat for using the Webchat client (DEPRECATED)

See this [issue](https://github.com/mrbot-ai/rasa-webchat/issues/28)

```bash
pip install git+git://github.com/RasaHQ/rasa.git

```

## Workaround to make Rasa work if AVX is not compatible with your CPU

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

## Development instructions

### Prepare dataset for training/testing

If you're (re-)generating data using Chatito, paste the related files under the `data/nlu_chatito` folder and then execute the following commands:

```bash
rasa data convert nlu --data data/nlu_chatito/train/ --out data/train/nlu.md -l es -f md
rasa data convert nlu --data data/nlu_chatito/test/ --out data/test/nlu.md -l es -f md
```

### Training Rasa Core & NLU models

The following command trains both the Core and NLU models

```bash
rasa train --data data/train
```

### NLU model evaluation

The following command performs a model evaluation of the latest trained NLU model under the `models` directory

```bash
rasa test nlu -u data/test/ --out nlu_metrics/
```

Finally, check the following files for results:
 
* [Intent Confusion Matrix](nlu_metrics/confmat.png) 
* [Intent Confidence Prediction][nlu_metrics/hist.png]
* [Misclassified Intents](nlu_metrics/intent_errors.json)
* [Other Intent/Entity Metrics Report](nlu_metrics/)

### Dialogue (CORE) model evaluation

The following command performs a model evaluation of the latest trained dialogue model under the `models` directory

```bash
rasa test core -s data/test/ --out core_metrics/
```

Finally, check the [results](core_metrics/) directory for a summary of the performed evaluation

### Visualizing stories

```bash
rasa visualize -d domain.yml -s data/train/stories.md -u data/train/nlu.md
```
## Chatbot Deployment

### Deploying custom actions

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

### Run Chatbot + Rasa X

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

### Deploy the chatbot without RasaX & enabled connection to a web channel through socketsio

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

* Install Rasa + RasaX using one-click docker

```
TODO
```

* Build Action Server Docker Image

```bash
export GLPI_DOCKER_IMAGE=santteegt/glpi-chatbot-actions:0.0.1
docker build -t $GLPI_DOCKER_IMAGE .
```

* Push the Docker action server image to DockerHub  (Optional for local testing)

```bash
docker login --username santteegt
docker push $GLPI_DOCKER_IMAGE
```

* Copy `socketio` settings from [credentials.yml](credentials.yml) to the `credentials.yml` file in the `RASA_HOME` directory

* Copy the contents from [.env.sample](.env.sample) to the `.env` file in the `RASA_HOME` directory

* Copy the [docker-compose.override.yml](docker-compose.override.yml) file to the `RASA_HOME` directory
