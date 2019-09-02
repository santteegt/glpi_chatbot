## story_saludo  <!--- The name of the story. It is not mandatory, but useful for debugging. -->
* saludo <!--- User input expressed as intent. In this case it represents users message 'Hola'. -->
 - utter_intro <!--- The response of the chatbot expressed as an action. In this case it represents chatbot's response '¿En que le puedo ayudar?' -->
* nombre{"sujeto": "Santiago Gonzalez"}
 - utter_saludo
 - utter_sugerencias
 
## story_opciones
* solicitar_opciones
 - utter_sugerencias
 
## story_despedida
* despedida
 - utter_despedida

## story_agradecimiento
* agradecimiento
 - utter_gracias
 - utter_mas_ayuda
 
## story_finaliza_sesion
* agradecimiento
 - utter_gracias
 - utter_mas_ayuda
* despedida
 - utter_despedida
 - action_restart
 
## story_nombre
* nombre{"sujeto": "Santiago Gonzalez"}
 - utter_saludo
 - utter_sugerencias

## story_chitchat
* chitchat
 - utter_chitchat
 - utter_sugerencias

## story_creacion_usuario
* creacion_usuarios
 - action_joke
 - utter_mas_ayuda
 
## story_recuperar_contrasena
* recuperar_contrasena
 - utter_email
* correo_electronico
 - utter_contrasena
 - utter_confirmar_atencion
* agradecimiento
 - utter_mas_ayuda
* despedida
 - utter_despedida
 - action_restart
 
## story_requerimiento_recurso_computacional_happy_path
* peticion_recurso_computacional
 - compute_resource_form
 - form {"name": "compute_resource_form"}
 - form {"name": null}
 - utter_compute_form_values
* confirmar
 - utter_enviar_ticket_no
 - slot {"ticket_no": "0055"}
 - utter_confirmar_solicitud
 - utter_mas_ayuda
 
## story_requerimiento_recurso_computacional_unhappy_path_1
* peticion_recurso_computacional
 - compute_resource_form
 - form {"name": "compute_resource_form"}
* chitchat
 - utter_chitchat
 - compute_resource_form
 - form {"name": null}
 - utter_compute_form_values
* confirmar
 - utter_enviar_ticket_no
 - slot {"ticket_no": "0055"}
 - utter_confirmar_solicitud
 - utter_mas_ayuda
 
## story_requerimiento_recurso_computacional_unhappy_path_2
* peticion_recurso_computacional
 - compute_resource_form
 - form {"name": "compute_resource_form"}
* chitchat
 - utter_chitchat
 - compute_resource_form
* chitchat
 - utter_chitchat
 - compute_resource_form
* chitchat
 - utter_chitchat
 - compute_resource_form
 - form {"name": null}
 - utter_compute_form_values
* confirmar
 - utter_enviar_ticket_no
 - slot {"ticket_no": "0055"}
 - utter_confirmar_solicitud
 - utter_mas_ayuda

## story_requerimiento_recurso_computacional_stop_but_continue
* peticion_recurso_computacional
 - compute_resource_form
 - form {"name": "compute_resource_form"}
* cancelar
 - utter_continuar
* confirmar
 - compute_resource_form
 - form {"name": null}
 - utter_compute_form_values
* confirmar
 - utter_enviar_ticket_no
 - slot {"ticket_no": "0055"}
 - utter_confirmar_solicitud
 - utter_mas_ayuda

## story_requerimiento_recurso_computacional_stop_and_confirm
* peticion_recurso_computacional
 - compute_resource_form
 - form {"name": "compute_resource_form"}
* cancelar
 - utter_continuar
* cancelar
 - action_deactivate_form
 - form {"name": null}
 - utter_cancelado
 - utter_mas_ayuda