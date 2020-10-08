## out of scope path
* out_of_scope
 - utter_out_of_scope

## help
* help
 - utter_help

## happy path
* greet
 - utter_greet
 - utter_suggest
 
## login happy path
* login{"auth_token": "a_token_auth"}
 - action_validate_auth
 - slot{"username": "normal", "email": "normal@ucuenca.edu.ec"}
 - utter_logged_in

## login failed to validate
* login{"auth_token": "a_token_auth"}
 - action_validate_auth
 - slot{"username": null, "email": null}
 - utter_login_failed

## ask for options
* show_menu
 - utter_help
 - utter_suggest

## say goodbye
* goodbye
 - utter_goodbye

## bot challenge
* bot_challenge
 - utter_iamabot
  
## ask more help + confirm
* thank
 - utter_welcome
 - utter_more_help
* confirm
 - utter_suggest
  
## ask more help + deny
* thank
 - utter_welcome
 - utter_more_help
* deny
 - utter_goodbye
 - action_restart

## incident form
* open_incident OR password_reset OR problem_email
 - open_incident_form
 - form{"name": "open_incident_form"}
 - form{"name": null}
 - slot {"ticket_no": "0055"}

## incident form interrupted
* open_incident OR password_reset OR problem_email
 - open_incident_form
 - form{"name":"open_incident_form"}
* help
 - utter_help
 - open_incident_form
 - form{"name":null}
 - slot {"ticket_no": "0055"}

## incident form interrupted
* open_incident OR password_reset OR problem_email
 - open_incident_form
 - form{"name":"open_incident_form"}
* out_of_scope
 - utter_out_of_scope
 - open_incident_form
 - form{"name":null}
 - slot {"ticket_no": "0055"}

## incident form stop but continue
* open_incident OR password_reset OR problem_email
 - open_incident_form
 - form{"name":"open_incident_form"}
* deny
 - utter_continue
* confirm
 - open_incident_form
 - form{"name":null}
 - slot {"ticket_no": "0055"}

## incident form stop + cancel
* open_incident OR password_reset OR problem_email
 - open_incident_form
 - form{"name":"open_incident_form"}
* deny
 - utter_continue
* deny
 - action_deactivate_form
 - form{"name":null}
 - utter_process_cancelled

## get incident status form
* get_incident_status
 - incident_status_form
 - form{"name": "incident_status_form"}
 - form{"name": null}

## get incident status form interrupted
* get_incident_status
 - incident_status_form
 - form{"name": "incident_status_form"}
* help
 - utter_help
 - incident_status_form
 - form{"name":null}

## get incident status form interrupted
* get_incident_status
 - incident_status_form
 - form{"name": "incident_status_form"}
* out_of_scope
 - utter_out_of_scope
 - incident_status_form
 - form{"name":null}

## get incident status form stop but continue
* get_incident_status
 - incident_status_form
 - form{"name": "incident_status_form"}
* deny
 - utter_continue
* confirm
 - incident_status_form
 - form{"name":null}

## get incident status form stop + cancel
* get_incident_status
 - incident_status_form
 - form{"name": "incident_status_form"}
* deny
 - utter_continue
* deny
 - action_deactivate_form
 - form{"name":null}
 - utter_process_cancelled
 
## connect_wifi form happy_path success
* connect_wifi
 - wifi_faq_form
 - form{"name": "wifi_faq_form"}
 - form{"name": null}
* confirm
 - utter_welcome

## connect_wifi form happy_path fail
* connect_wifi
 - wifi_faq_form
 - form{"name": "wifi_faq_form"}
 - form{"name": null}
* deny{"incident_title":"Problema de conexion a la red WIFI", "itilcategory_id":"52"}
 - open_incident_form
 - form{"name": "open_incident_form"}
 - form{"name":null}
 - slot {"ticket_no": "0055"}

## connect_wifi form interrupted
* connect_wifi
 - wifi_faq_form
 - form{"name":"wifi_faq_form"}
* help
 - utter_help
 - wifi_faq_form
 - form{"name":null}

## connect_wifi form interrupted with chitchat
* connect_wifi
 - wifi_faq_form
 - form{"name":"wifi_faq_form"}
* out_of_scope
 - utter_out_of_scope
 - wifi_faq_form
 - form{"name":null}

## connect_wifi form stop + cancel
* connect_wifi
 - wifi_faq_form
 - form{"name":"wifi_faq_form"}
* deny
 - utter_continue
* deny
 - action_deactivate_form
 - form{"name":null}
 - utter_process_cancelled

## connect_wifi form stop but continue
* connect_wifi
 - wifi_faq_form
 - form{"name":"wifi_faq_form"}
* deny
 - utter_continue
* confirm
 - wifi_faq_form
 - form{"name":null}
 
## create_user form happy_path success
* create_user
 - create_user_faq_form
 - form{"name": "create_user_faq_form"}
 - form{"name": null}
* confirm
 - utter_welcome

## create_user form happy_path fail
* create_user
 - create_user_faq_form
 - form{"name": "create_user_faq_form"}
 - form{"name": null}
* deny{"incident_title":"Problema para crear un usuario", "itilcategory_id":"56"}
 - open_incident_form
 - form{"name": "open_incident_form"}
 - form{"name":null}
 - slot {"ticket_no": "0055"}

## create_user form interrupted
* create_user
 - create_user_faq_form
 - form{"name":"create_user_faq_form"}
* help
 - utter_help
 - create_user_faq_form
 - form{"name":null}

## create_user form interrupted with chitchat
* create_user
 - create_user_faq_form
 - form{"name":"create_user_faq_form"}
* out_of_scope
 - utter_out_of_scope
 - create_user_faq_form
 - form{"name":null}

## request_biometrics_report form
* request_biometrics_report
 - biometrics_report_form
 - form{"name": "biometrics_report_form"}
 - form{"name": null}
 - slot {"ticket_no": "0055"}

## request_biometrics_report form interrupted
* request_biometrics_report
 - biometrics_report_form
 - form{"name":"biometrics_report_form"}
* help
 - utter_help
 - biometrics_report_form
 - form{"name":null}
 - slot {"ticket_no": "0055"}

## request_biometrics_report form interrupted with chitchat
* request_biometrics_report
 - biometrics_report_form
 - form{"name":"biometrics_report_form"}
* out_of_scope
 - utter_out_of_scope
 - biometrics_report_form
 - form{"name":null}
 - slot {"ticket_no": "0055"}

## request_biometrics_report form stop but continue
* request_biometrics_report
 - biometrics_report_form
 - form{"name":"biometrics_report_form"}
* deny
 - utter_continue
* confirm
 - biometrics_report_form
 - form {"name": null}
 - slot {"ticket_no": "0055"}
 
## request_biometrics_report form stop + cancel
* request_biometrics_report
 - biometrics_report_form
 - form{"name":"biometrics_report_form"}
* deny
 - utter_continue
* deny
 - action_deactivate_form
 - form{"name":null}
 - utter_process_cancelled
