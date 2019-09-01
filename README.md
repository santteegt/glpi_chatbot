﻿# Rasa Stack starter-pack

Looked through the [Rasa NLU](http://rasa.com/docs/nlu/) and [Rasa Core](http://rasa.com/docs/core/) documentation and ready to build your first intelligent assistant? We have some resources to help you get started! This repository contains the foundations of your first custom assistant. This starter-pack also comes with a step-by-step video tutorial which you can find [here](https://youtu.be/lQZ_x0LRUbI).  

This starter-pack comes with a small amount of training data which lets you build a simple assistant. **You can find more training data here in the [forum](https://forum.rasa.com/t/grab-the-nlu-training-dataset-and-starter-packs/903) and use it to teach your assistant new skills and make it more engaging.**

We would recommend downloading this before getting started, although the tutorial will also work with just the data in this repo. 

The initial version of this starter-pack lets you build a simple assistant capable of cheering you up with Chuck Norris jokes.


<p align="center">
  <img src="./rasa-stack-mockup.gif">
</p>


Clone this repo to get started:

```
git clone https://github.com/RasaHQ/starter-pack-rasa-stack.git
```

After you clone the repository, a directory called starter-pack-rasa-stack will be downloaded to your local machine. It contains all the files of this repo and you should refer to this directory as your 'project directory'.


## Setup and installation

If you haven’t installed Rasa NLU and Rasa Core yet, you can do it by navigating to the project directory and running:  

```
pip install -r alt_requirements/requirements_full.txt
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

## Prepare dataset for training/testing

If you're (re-)generating data using Chatito, paste the related files under the `data/nlu_chatito` folder and then execute the following commands:

```bash
rasa data convert nlu --data data/nlu_chatito/train/ --out data/train/nlu.md -l es -f md
rasa data convert nlu --data data/nlu_chatito/test/ --out data/test/nlu.md -l es -f md
```

## Training Rasa Core & NLU models

The following command trains both the Core and NLU models

```bash
rasa train --data data/train
```

## NLU model evaluation

The following command performs a model evaluation of the latest trained NLU model under the `models` directory

```bash
rasa test nlu -u data/test/ --report report_metrics/
```

Finally, check the following files for results:
 
* [Intent Confusion Matrix](confmat.png) 
* [Intent Confidence Prediction][hist.png]
* [Misclassified Intents](errors.json)
* [Intent/Entity Metrics Report](report_metrics/)

## Dialogue (CORE) model evaluation

The following command performs a model evaluation of the latest trained dialogue model under the `models` directory

```bash
rasa test core -s data/test/
```

Finally, check the [results](results/) directory for a summary of the performed evaluation

## Visualizing stories

```bash
rasa visualize -d domain.yml -s data/train/stories.md -u data/train/nlu.md
```

## Deploying custom actions

```bash
rasa run actions --actions actions -p 5055
```

### Test your chatbot locally

```bash
rasa shell --endpoints endpoints.yml
```

### Deploy the chatbot with enabled connection to a web channel through socketsio

```bash
rasa run --endpoints endpoints.yml --credentials credentials.yml --enable-api --cors "*" --port 5002
```

### Deploy the web client

```bash
cd client
npm install
npm start
```