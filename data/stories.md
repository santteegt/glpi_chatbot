## story_saludo  <!--- The name of the story. It is not mandatory, but useful for debugging. -->
* saludo <!--- User input expressed as intent. In this case it represents users message 'Hola'. -->
 - utter_intro <!--- The response of the chatbot expressed as an action. In this case it represents chatbot's response '¿En que le puedo ayudar?' -->
 - utter_sugerencias
 
## story_despedida
* despedida
 - utter_despedida

## story_agradecimiento
* agradecimiento
 - utter_gracias
 
## story_nombre
* nombre{"sujeto": "Santiago Gonzalez"}
 - utter_saludo
 - utter_sugerencias

## story_creacion_usuario
* creacion_usuarios
 - action_joke
 - utter_mas_ayuda
 
## story_recuperar_contrasena
* recuperar_contrsena
 - utter_email
 - utter_contrasena
 - utter_mas_ayuda
* finaliza_sesion
 - utter_despedida
 - action_restart