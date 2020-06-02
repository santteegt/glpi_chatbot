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

## intent:create_user
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

## intent:request_vm
- necesito una maquina virtual
- requiero acceso a una maquina virtual
- requiero una maquina virtual 
- necesito un servidor de [desarrollo](vm_environment)
- requiero una VM para [pruebas](vm_environment)
- solicito una instancia para [producción](vm_environment)
- pedir una maquina virtual de [16](vm_ram) GB en RAM y [128](vm_disk_space) GB de disco duro
- solicito maquina virtual [16](vm_ram) GB de ram [8](vm_cpu_cores) nucleos de cpu
- acceso a una maquina de [16](vm_ram) GB de ram [2](vm_cpu_cores) CPUs y [16](vm_disk_space) GB de disco
- solicito un servidor para [desarrollo](vm_environment)

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
- necesito [512](vm_disk_space) GB de disco duro
- [8](vm_disk_space) GB de capacidad
- escalabilidad [horizontal](vm_scalability)
- necesito escalabilidad [vertical](vm_scalability)
- [32](vm_ram) GB de ram
- necesito un ambiente de [desarrollo](vm_environment)
- [16](vm_disk_space) GB de HD
- solicito [64](vm_ram) GB de ram
- [8](vm_ram) GB de ram
- [32](vm_cpu_cores) nucleos de cpu
- [4](vm_cpu_cores) nucleos
- necesito [8](vm_cpu_cores) procesadores
- necesito un entorno de [pruebas](vm_environment)
- [2](vm_cpu_cores) procesadores
- necesito [16](vm_disk_space) GB de HD
- necesito [3](vm_cpu_cores) procesadores
- [512](vm_disk_space) GB de disco duro
- ambiente de [producción](vm_environment)
- ambiente de [pruebas](vm_environment)
- ambiente de [desarrollo](vm_environment)
- escalable [horizontalmente]{"entity": "vm_scalability", "value": "horizontal"}
- para escalar [verticalmente]{"entity": "vm_scalability", "value": "vertical"}

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

## lookup:software
data/software-dtic.txt

## lookup:faculty
data/faculties.txt

## lookup:department
data/departments.txt
