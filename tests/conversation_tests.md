## bot challenge
* bot_challenge: Eres un robot?
    - utter_iamabot

## ask for options
* show_menu: ver opciones disponibles
    - utter_help
    - utter_suggest

## out of scope
* out_of_scope: Quiero una pizza
    - utter_out_of_scope

## ask for more help
* thank: muchas gracias
     - utter_welcome
     - utter_more_help
* confirm: si
    - utter_suggest

## open incident
* greet: hola
    - utter_greet
    - utter_help
    - utter_suggest
* open_incident: quiero reportar un problema
    - open_incident_form
    - form{"name": "open_incident_form"}
    - form{"name": null}
    - slot {"ticket_no": "0055"}

## password reset incident
* password_reset: no recuerdo mi contraseña
    - open_incident_form
    - form{"name": "open_incident_form"}
    - form{"name": null}
    - slot {"ticket_no": "0055"}

## problem email incident
* greet: hello
    - utter_greet
    - utter_help
    - utter_suggest
* problem_email: no puedo acceder a mi correo electronico
    - open_incident_form
    - form{"name": "open_incident_form"}
    - form{"name": null}

## problem with email interrupted
* problem_email: Tengo un problema con mi correo
    - open_incident_form
    - form{"name": "open_incident_form"}
* help: help
    - utter_help
    - open_incident_form
    - form{"name": null}
    - slot {"ticket_no": "0055"}
    
## connect to wifi
* connect_wifi: quiero conectarme a la red de wifi de la u
    - wifi_faq_form
    - form{"name": "wifi_faq_form"}
    - form{"name": null}
* confirm: si
    - utter_welcome

## unable to connect to wifi
* connect_wifi: como conectarme a la red wifi
    - wifi_faq_form
    - form{"name": "wifi_faq_form"}
    - form{"name": null}
* deny {"incident_title":"Problema de conexion a la red WIFI", "itilcategory_id":"52"}: no
    - open_incident_form
    - form{"name": "open_incident_form"}
    - form{"name":null}
    - slot {"ticket_no": "0055"}
    
## create a user
* create_user: necesito crear un usuario
    - create_user_faq_form
    - form{"name": "create_user_faq_form"}
    - form{"name": null}
* confirm: si
    - utter_welcome

## unable to create a user
* create_user: necesito registrarme como usuario
    - create_user_faq_form
    - form{"name": "create_user_faq_form"}
    - form{"name": null}
* deny{"incident_title":"Problema para crear un usuario", "itilcategory_id":"56"}: no pude
    - open_incident_form
    - form{"name": "open_incident_form"}
    - form{"name":null}
    - slot {"ticket_no": "0055"}

## request biometrics report
* request_biometrics_report: solicito un reporte de intentos de marcacion
    - biometrics_report_form
    - form{"name": "biometrics_report_form"}
    - form{"name": null}
    - slot {"ticket_no": "0055"}

## request biometrics report interrupted
* request_biometrics_report: necesito un reporte de mis intentos de marcacion
    - biometrics_report_form
    - form{"name":"biometrics_report_form"}
* help
    - utter_help
    - biometrics_report_form
    - form{"name":null}
    - slot {"ticket_no": "0055"}