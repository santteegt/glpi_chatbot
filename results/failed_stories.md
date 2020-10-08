## unable to connect to wifi (/var/folders/5z/_0rg80mn4cj4_7rvglfhthcr0000gn/T/tmpty_wos43/824fb25ef4f5461c9a2928c8688b5142_conversation_tests.md)
* connect_wifi: como conectarme a la red wifi
    - wifi_faq_form   <!-- predicted: utter_default -->
    - form{"name": "wifi_faq_form"}
    - form{"name": null}
* deny
    - open_incident_form
    - form{"name": "open_incident_form"}
    - form{"name": null}
    - slot{"ticket_no": "0055"}


## create a user (/var/folders/5z/_0rg80mn4cj4_7rvglfhthcr0000gn/T/tmpty_wos43/824fb25ef4f5461c9a2928c8688b5142_conversation_tests.md)
* create_user: necesito crear un usuario
    - create_user_faq_form   <!-- predicted: utter_default -->
    - form{"name": "create_user_faq_form"}
    - form{"name": null}
* confirm: si
    - utter_welcome   <!-- predicted: utter_default -->


## unable to create a user (/var/folders/5z/_0rg80mn4cj4_7rvglfhthcr0000gn/T/tmpty_wos43/824fb25ef4f5461c9a2928c8688b5142_conversation_tests.md)
* create_user: necesito registrarme como usuario
    - create_user_faq_form   <!-- predicted: utter_default -->
    - form{"name": "create_user_faq_form"}
    - form{"name": null}
* deny
    - open_incident_form
    - form{"name": "open_incident_form"}
    - form{"name": null}
    - slot{"ticket_no": "0055"}


## request biometrics report (/var/folders/5z/_0rg80mn4cj4_7rvglfhthcr0000gn/T/tmpty_wos43/824fb25ef4f5461c9a2928c8688b5142_conversation_tests.md)
* request_biometrics_report: solicito un reporte de intentos de marcacion
    - biometrics_report_form   <!-- predicted: utter_default -->
    - form{"name": "biometrics_report_form"}
    - form{"name": null}
    - slot{"ticket_no": "0055"}


## request biometrics report interrupted (/var/folders/5z/_0rg80mn4cj4_7rvglfhthcr0000gn/T/tmpty_wos43/824fb25ef4f5461c9a2928c8688b5142_conversation_tests.md)
* request_biometrics_report: necesito un reporte de mis intentos de marcacion
    - biometrics_report_form   <!-- predicted: utter_default -->
    - form{"name": "biometrics_report_form"}
* help
    - utter_help
    - biometrics_report_form   <!-- predicted: action_listen -->
    - form{"name": null}
    - slot{"ticket_no": "0055"}


## bot challenge (/var/folders/5z/_0rg80mn4cj4_7rvglfhthcr0000gn/T/tmpty_wos43/824fb25ef4f5461c9a2928c8688b5142_conversation_tests.md)
* bot_challenge: Eres un robot?
    - utter_iamabot   <!-- predicted: utter_default -->


## ask for options (/var/folders/5z/_0rg80mn4cj4_7rvglfhthcr0000gn/T/tmpty_wos43/824fb25ef4f5461c9a2928c8688b5142_conversation_tests.md)
* show_menu: ver opciones disponibles
    - utter_help   <!-- predicted: utter_default -->
    - utter_suggest   <!-- predicted: action_listen -->


## out of scope (/var/folders/5z/_0rg80mn4cj4_7rvglfhthcr0000gn/T/tmpty_wos43/824fb25ef4f5461c9a2928c8688b5142_conversation_tests.md)
* out_of_scope: Quiero una pizza
    - utter_out_of_scope   <!-- predicted: utter_default -->


## ask for more help (/var/folders/5z/_0rg80mn4cj4_7rvglfhthcr0000gn/T/tmpty_wos43/824fb25ef4f5461c9a2928c8688b5142_conversation_tests.md)
* thank: muchas gracias
    - utter_welcome   <!-- predicted: utter_default -->
    - utter_more_help   <!-- predicted: utter_default -->
* confirm: si
    - utter_suggest   <!-- predicted: utter_default -->


## open incident (/var/folders/5z/_0rg80mn4cj4_7rvglfhthcr0000gn/T/tmpty_wos43/824fb25ef4f5461c9a2928c8688b5142_conversation_tests.md)
* greet: hola
    - utter_greet   <!-- predicted: utter_default -->
    - utter_help   <!-- predicted: utter_suggest -->
    - utter_suggest   <!-- predicted: action_listen -->
* open_incident: quiero reportar un problema
    - open_incident_form   <!-- predicted: utter_default -->
    - form{"name": "open_incident_form"}
    - form{"name": null}
    - slot{"ticket_no": "0055"}


## password reset incident (/var/folders/5z/_0rg80mn4cj4_7rvglfhthcr0000gn/T/tmpty_wos43/824fb25ef4f5461c9a2928c8688b5142_conversation_tests.md)
* password_reset: no recuerdo mi contraseña
    - open_incident_form   <!-- predicted: utter_default -->
    - form{"name": "open_incident_form"}
    - form{"name": null}
    - slot{"ticket_no": "0055"}


## problem email incident (/var/folders/5z/_0rg80mn4cj4_7rvglfhthcr0000gn/T/tmpty_wos43/824fb25ef4f5461c9a2928c8688b5142_conversation_tests.md)
* greet: hello
    - utter_greet   <!-- predicted: utter_default -->
    - utter_help   <!-- predicted: utter_suggest -->
    - utter_suggest   <!-- predicted: action_listen -->
* problem_email: no puedo acceder a mi correo electronico
    - open_incident_form   <!-- predicted: utter_default -->
    - form{"name": "open_incident_form"}
    - form{"name": null}


## problem with email interrupted (/var/folders/5z/_0rg80mn4cj4_7rvglfhthcr0000gn/T/tmpty_wos43/824fb25ef4f5461c9a2928c8688b5142_conversation_tests.md)
* problem_email: Tengo un problema con mi correo
    - open_incident_form   <!-- predicted: utter_default -->
    - form{"name": "open_incident_form"}
* form: help: help
    - form: utter_help   <!-- predicted: open_incident_form -->
    - form: open_incident_form   <!-- predicted: action_listen -->
    - form{"name": null}
    - slot{"ticket_no": "0055"}


## connect to wifi (/var/folders/5z/_0rg80mn4cj4_7rvglfhthcr0000gn/T/tmpty_wos43/824fb25ef4f5461c9a2928c8688b5142_conversation_tests.md)
* connect_wifi: quiero conectarme a la red de wifi de la u
    - wifi_faq_form   <!-- predicted: utter_default -->
    - form{"name": "wifi_faq_form"}
    - form{"name": null}
* confirm: si
    - utter_welcome   <!-- predicted: utter_default -->


