# RocketChat Installation

## Server Setup using docker-compose

* Download the latest `docker-compose.yml` file from this [link](https://docs.rocket.chat/installation/docker-containers/docker-compose)
* A complete setup guide can be found [here](https://docs.rocket.chat/installation/docker-containers)
* Start the server by running the following on a terminal:

```bash
docker-compose up -d
```

* In case you face issues with the Setup wizard, you can deploy it manually by following the steps in this [script](https://github.com/RocketChat/Rocket.Chat/blob/develop/example-build-run.sh). However, make sure you run te mongo instances defined in the `docker-compose.yml` file

## Configuration steps for MVP

* When you first open the Administration UI at  `http://localhost:3000` you'll need to create an Admin user (e.g. admin/glpi@dmin)
* Register your server at `Administration > Connectivity Services` using the internet connection
* Create the following users at `Administration > Users`
    * A Helpdesk Agent user with role `Livechat Agent` (e.g. dtic_agent_1/1234abcd) 
    * A Bot user with roles `bot` & `Livechat Agent` (e.g. ucbot/ucbotpassword)
* Define a webhook integration at `Administration > Integrations > Outgoing` with the following properties:
    * Event Trigger: Message Sent
    * Enabled: true
    * Name (e.g UCBot DM)
    * Channel: all_direct_messages
    * URLs: Rocketchat webhook URL from your deployed Rasa bot (e.g. http://host.docker.internal:5005/webhooks/rocketchat/webhook)
    * Post as: the bot username you created above (e.g. ucbot)
* Enable the Omnichannel feature at `Administration > Omnichannel` with set the following properties:
    * Omnichannel enabled: true
    * Business Hours: enabled
    * Livechat:
        * Livechat Title
        * Offline Form Unavailable Message
        * Title
        * Instructions
        * Offline Success Message
        * Allow Visitor to Switch Departments: disabled
        * Show Agent email: disabled
        * Conversation Finished Message
        * Conversation Finished Text
        * Registration Form Message
        * Livechat Allowed Domains: domains where the Rochetchat client will be available
    * Routing:
        * Assign new conversations to bot agent: enabled
* Now, you'll be able to see the Omnichannel option at the `...` menu in the root page. Click it and configure the following:
    * Managers: select your Admin user
    * Agents: make sure the two users you created above are listed
    * Departments: create a new one with the following settings:
        * Enabled: true
        * Name: a name for a helpdesk department (e.g. Mesa de servicios - DTIC)
        * Description
        * Email
        * Show on offline page
        * Request tag(s) before closing conversation: enabled
        * Conversation closing tags: add at least one tag like `#helpdesk`
        * Agents: add the human agent you created above
    * Livechat appearance
    * Business Hours
* Install Rasa App through `Administration > Marketplace`
    * Check this [guide](https://github.com/RocketChat/Apps.Rasa/blob/master/docs/api-endpoints/perform-handover.md) for a more in-depth instructions on how this app can be used in conjuction with a [Rasa Action (ActionHandoff)](../actions/actions_helpdesk.py) to perform handover to an agent
    * Once it is installed, go to `Administration > Apps > Rasa` and set the following properties:
        * Bot Username: the bot username you created above (e.g. ucbot)
        * Rasa Server URL: your deployed Rasa bot (e.g. http://host.docker.internal:5005)
        * Service Unavailable Message
        * Close Chat Message
        * Handover Message
        * Default Handover Department Name: the name of th department created above (e.g. Mesa de servicios - DTIC)

    

