<!--- Rule of thumb: 10-15 examples per intent. -->
<!--- Examples should be relevant and diverse in vocab -->

## intent:greet
- hey
- hola
- hola que tal
- buenos dias
- buenas tardes
- buenas noches
- Que hay
- holas
- saludos
- hola hola
- buenas
- hola buenos dias

## intent:goodbye
- chao
- adios
- nos vemos
- nos vemos luego
- chau
- pues adios
- hasta luego
- hasta pronto
- salir
- finaliza sesion
- chao chao
- fin
- terminar sesion

## intent:thank
- gracias!
- gracias
- muchas gracias
- lo agradezco
- muy bien gracias
- gracias por su ayuda
- agradezco su ayuda
- estoy agradecido

## intent:help
- Necesito ayuda
- Con que me puedes ayudar?
- Puedes ayudarme?
- Que puedes hacer?
- Necesito algo de ayuda
- Ayudame
- Me puede ayudar?
- Ayuda
- Requiero su ayuda
- Necesito asistencia
- Ayuda con un problema

## intent:show_menu
- opciones
- ver opciones
- menu
- mostrar menu
- ver menu
- mostrar opciones disponibles

## intent:bot_challenge
- eres un robot?
- eres humano?
- estoy hablando con un robot?
- estoy hablando con un humano?
- eres un robot verdad?
- acaso eres un robot?
- como te llamas?
- cual es tu nombre?

## intent:confirm
- si
- bueno
- esta bien
- acepto
- confirmar
- aceptar
- si si
- bueno bueno
- ok
- si acepto
- si confirmo
- si confirma
- okay
- confirmar

## intent:deny
- no
- no continuar
- cancelar
- no es lo que quiero
- cancela
- negativo
- no es lo que deseo
- no gracias
- no
- denegar
- nop
- nada
- no soluciona

## intent:open_incident
- Necesito reportar una incidencia
- Me puede ayudar abriendo una incidencia?
- Tengo un problema y necesito reportar una incidencia
- Abrir incidencia
- Reportar incidencia
- Por favor me puede ayudar a reportar una incidencia por favor?
- Quiero reportar una nueva incidencia
- Quiero abrir una incidencia
- Tengo un problema muy extraño
- Quiero reportar un problema
- Tengo un problem y necesito reportar una incidecia
- Tengo un inconveniente y necesito abrir una incidencia

## intent:get_incident_status
- cual es el estado actual de mi ticket [0055](ticket_no)
- estado de incidencia
- ya fue solucionado mi inconveniente?
- quiero saber el estado de mi incidencia
- consultar el estado de incidencia
- consulta ticket numero [64524](ticket_no)
- estado de ticket [1234546](ticket_no)
- solucionaron mi ticket?
- cual fue la resolucion de mi incidencia?
- estado de ticket [2356](ticket_no)
- ver estado de ticket con id [653354](ticket_no)
- que paso con la incidencia que reporte?
- atendieron mi ticket?
- cual es el progreso de la incidencia [0055](ticket_no)
- cual es el estado de mi requerimiento
- consultar el estado de mi requerimiento
- quiero saber el estado de mi requerimiento
- como va mi requerimiento

## intent:password_reset
- necesito recuperar mi contraseña
- necesito ayuda para recuperar mi contaseña
- no puedo reestablecer mi contraseña
- necesito ayuda con mi contraseña
- tengo problemas para reestablecer mi contraseña
- la contraseña no funciona
- recuperar la contraseña
- reestablecer contraseña
- he olvidado mi contraseña y no se como reestablecerla
- perdi mi contraseña
- no me acuerdo de la contraseña
- no recuerdo mi contraseña
- ayuda no recuerdo mi clave
- olvide mi clave de usuario
- como puedo recuperar mi clave de usuario?

## intent:problem_email
- no puedo acceder a mi cuenta de correo electrónico
- tengo problemas con mi correo 
- problemas con gmail
- existe un problema con mi correo electrónico
- no puedo iniciar sesion con mi correo electronico
- no puedo abrir mi correo
- no puedo iniciar sesion en gmail
- no puedo iniciar sesion con mi cuenta de correo
- tengo inconvenientes con mi email
- problema con mi email
- problemas con el correo institucional
- el correo institucional no funciona
- no funciona mi correo

## intent:connect_wifi
- necesito conectarme a la red [eduroam](wifi_network)
- como puedo conectarme a la red wifi
- necesito conectarme a la red de internet de la universidad
- como puedo conectarme a la red [ucwifi](wifi_network) 
- quiero conectarme a la red wifi de del campus 
- ayuda con conexion a la red wifi 
- cual es la contraseña de la red wifi de la universidad
- como conectarme a la red [guest](wifi_network)
- quiero conectarme al wifi
- no tengo acceso a la red wifi
- como conectarme a la red de [invitado]{"entity":"wifi_network", "value":"guest"}

## intent:faq_create_user
- crear cuenta para estudiante de curso
- nueva cuenta para estudiente de carrera
- me he inscrito en un curso y necesito una cuenta de usuario
- soy un nuevo estudiante de carrera y necesito crear una cuenta

## intent:create_app_user
- Ayuda a crear un usuario
- Necesito registrarme como usuario
- Necesito una cuenta de usuario
- Como puedo crear mi cuenta de estudiante?
- Quiero crear una cuenta institucional
- Ayuda a registrarme en el sistema
- Necesito un usuario para acceder al sistema
- Como crear una cuenta de usuario de la u
- crear cuenta de usuario
- registar una nueva cuenta de sistema
- necesito un usuario para el sistema [koha](application)
- no tengo usuario en sistema de la [biblioteca](application)
- No puedo ingresar al [catalogo de libros](application)
- necesito crear un cuenta para el sistema [sgb](application)
- como puedo acceder al sistema [koha](application)
- quiero crear un usuario para el sistema de [silabos](application)
- quiero ingresar al sistema de [gestion academica](application)
- quiero utilizar el sistema de [clinicas](application)
- no puedo acceder al portal de [bolsa de trabajo](application)
- quiero entrar al sistema de [estudiantes](application)
- necesito acceso al sitema de [docentes](application)
- necesito un usuario [urkund](application)
- necesito usuario y contraseña para [urkund](application)
- como puedo tener un usuario en [urkund](application)
- como puedo ingresar a [urkund](application)
- necesito un usuario para el sistema antiplagio [urkund](application)
- necesito credenciales para el [sistema antiplagio](application)

## intent:request_biometrics_report
- necesito un informe de marcación en el biométrico
- reporte de entrada salida del sistema biométrico
- solicitar un informe de marcación de este mes
- necesito revisar mis marcaciones en el sistema biometrico del dia de hoy
- informe de marcacion de la semana anterior
- informe de intentos de marcacion del dia de hoy
- solicito informe de intentos de marcacion del dia de ayer
- ver mis intentos de marcacion de hoy
- reporte diario de marcacion en sistema biometrico
- requiero un informe de intentos de marcacion de esta semana

## intent:inform
- mi correo es test@ucuenca.edu.ec
- mi correo es abraham.lincoln@ucuenca.edu.ec
- abraham.licoln@ucuenca.edu.ec
- es abraham.licoln@ucuenca.edu.ec
- abraham.lincolon@ucuenca.edu.ec
- hoy
- ayer
- esta semana
- este mes
- el mes pasado
- la semana anterior
- [baja](priority)
- [media](priority)
- [alta](priority)
- es de prioridad [baja](priority)
- prioridad [media](priority)
- prioridad [alta](priority)
- [urgente]{"entity":"priority", "value": "alta"}
- [muy urgente]{"entity":"priority", "value": "alta"}
- [crucial]{"entity":"priority", "value": "alta"}
- [eduroam](wifi_network)
- [ucwifi](wifi_network)
- [guest](wifi_network)
- la red de [invitados]{"entity":"wifi_network", "value":"guest"}
- [carrera](course_type) universitaria
- [curso](course_type) de corta duración
- [carrera](course_type) de [ingenieria](faculty)
- [carrera](course_type) de [arquitectura](faculty)
- [carrera](course_type) universitaria
- [curso](course_type) de idiomas
- [curso](course_type) de inglés
- [curso](course_type) de aleman
- [taller]{"entity":"course_type", "value":"curso"} de informática
- un [seminario]{"entity":"course_type", "value":"curso"} de emprendimiento
- una [charla]{"entity":"course_type", "value":"curso"} técnica
- facultad de [arquitectura y urbanismo](faculty)
- en [arquitectura](faculty)
- facultad de [artes](faculty)
- facu de [agropecuarias](faculty)
- [ciencias medicas](faculty)
- [ciencias quimicas](faculty)
- facultad de [economia](faculty)
- soy de [filosofia](faculty)
- la facultad de [hospitalidad](faculty)
- [ingenieria](faculty)
- [jurisprudencia](faculty)
- [medicina](faculty)
- faultad de [odontologia](faculty)
- [psicologia]](faculty)
- facultad de [quimica](faculty)
- soy [alumno](role)
- soy [empleado](role)
- rol de [trabajador](role)
- soy [docente](role)

## intent:out_of_scope
- cual es la raiz cuadrada de 5
- como esta el clima
- cual es el significado de la vida
- mi regrigerador no funciona
- la TV no funciona
- quiero pizza
- mi lavadora esta dañada
- que año es
- odernar una pizza
- quiero ordenar una pizza
- como sera el clima el dia de hoy
- que dia es hoy
- que fecha es hoy
- como te llamas
- quiero comida

## lookup:application
data/software-dtic.txt

## lookup:faculty
data/faculties.txt

## lookup:department
data/departments.txt

## lookup:role
data/roles.txt

## synonym:koha
- biblioteca
- catalogo de libros
- sistema de gestion de biblioteca
- sgb

## synonym:urkund
- sistema antiplagio

## synonym:alumno
- estudiante
- universitario