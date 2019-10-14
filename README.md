# Rasa Stack starter-pack

Looked through the [Rasa NLU](http://rasa.com/docs/nlu/) and [Rasa Core](http://rasa.com/docs/core/) documentation and ready to build your first intelligent assistant? We have some resources to help you get started! This repository contains the foundations of your first custom assistant. This starter-pack also comes with a step-by-step video tutorial which you can find [here](https://youtu.be/lQZ_x0LRUbI).  

This starter-pack comes with a small amount of training data which lets you build a simple assistant. **You can find more training data here in the [forum](https://forum.rasa.com/t/grab-the-nlu-training-dataset-and-starter-packs/903) and use it to teach your assistant new skills and make it more engaging.**

We would recommend downloading this before getting started, although the tutorial will also work with just the data in this repo. 

The initial version of this starter-pack lets you build a simple assistant capable of cheering you up with Chuck Norris jokes.


<p align="center">
  <img src="./rasa-stack-mockup.gif">
</p>

## Requirements

* Python 3.6.8+
* Pip3
* Conda (Recommended for isolated env creation)

## Setup and installation

If you haven’t installed Rasa NLU and Rasa Core yet, you can do it by navigating to the project directory and running:  

```
pip install -r alt_requirements/requirements_full.txt --extra-index-url https://pypi.rasa.com/simple
```

You also need to install a spaCy English language model. You can install it by running:

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
conda install -c anaconda tensorflow==1.13.1
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
rasa test nlu -u data/test/ --report report_metrics/
```

Finally, check the following files for results:
 
* [Intent Confusion Matrix](confmat.png) 
* [Intent Confidence Prediction][hist.png]
* [Misclassified Intents](errors.json)
* [Intent/Entity Metrics Report](report_metrics/)

### Dialogue (CORE) model evaluation

The following command performs a model evaluation of the latest trained dialogue model under the `models` directory

```bash
rasa test core -s data/test/
```

Finally, check the [results](results/) directory for a summary of the performed evaluation

### Visualizing stories

```bash
rasa visualize -d domain.yml -s data/train/stories.md -u data/train/nlu.md
```

### Deploying custom actions

```bash
rasa run actions --actions actions -p 5055
```

### Test your chatbot locally

```bash
rasa shell --endpoints endpoints.yml
```

### Run Rasa X (Optional)

Rasa X is a tool designed to make it easier to deploy and improve Rasa-powered assistants by learning from real conversations

```bash
rasa x --data data/train/ --endpoints endpoints.yml --cors '*' --enable-api --port 5005 --rasa-x-port 5002
```

Update admin password

```bash
python scripts/manage_users.py create me $RASA_X_PASSWORD admin --update
```

### Deploy DucklingHTTPExtractor (Optional if Enabled on the NLU pipeline)

```bash
docker run -p 8000:8000 rasa/duckling
```

### Deploy the chatbot with enabled connection to a web channel through socketsio

```bash
rasa run --endpoints endpoints.yml --credentials credentials.yml --enable-api --cors "*" --port 5005
```

### Deploy the web client

```bash
cd client
npm install
npm start
```