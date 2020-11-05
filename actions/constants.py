# -*- coding: utf-8 -*-


class EntitySlotEnum(object):
    CONFIRM = "confirm"
    ROLE = "role"
    EMAIL = "email"
    FOUND_EMAIL = "found_email"
    FACULTY = "faculty"
    PRIORITY = "priority"
    TIME = "time"
    INCIDENT_TITLE = "incident_title"
    INCIDENT_DESCRIPTION = "incident_description"
    ITILCATEGORY_ID = "itilcategory_id"
    APPLICATION = "application"
    DEPARTMENT = "department"
    VM_ENVIRONMENT = "vm_environment"
    VM_RAM = "vm_ram"
    VM_CPU_CORES = "vm_cpu_cores"
    VM_DISK_SPACE = "vm_disk_space"
    VM_SCALABILITY = "vm_scalability"
    OBSERVATIONS = "observations"
    WIFI_NETWORK = "wifi_network"
    HAS_EMAIL = "has_email"
    COURSE_TYPE = "course_type"
    PERSONAL_ID = "personal_id"
    BIOMETRICS_ID = "biometrics_id"
    TIME_PERIOD = "time_period"  # dummy to get from time entity
    START_TIME = "start_time"  # Obtained from Duckling
    END_TIME = "end_time"  # Obtained from Duckling
    GRAIN = "grain"  # Obtained from Duckling
    TICKET_NO = "ticket_no"
    AGREEMENT_REASON = "agreement_reason"
    DATA_CONFIRMATION = "data_confirmation"
    ACCEPT_AGREEMENT = "accept_agreement"


class IntentEnum(object):
    INFORM = "inform"
    OUT_OF_SCOPE = "out_of_scope"
    SHOW_MENU = "show_menu"
    CONFIRM = "confirm"
    DENY = "deny"
    OPEN_INCIDENT = "open_incident"
    GET_INCIDENT_STATUS = "get_incident_status"
    CONNECT_WIFI = "connect_wifi"
    FAQ_CREATE_USER = "faq_create_user"
    CREATE_APP_USER = "create_app_user"
    REQUEST_BIOMETRICS_REPORT = "request_biometrics_report"
    PASSWORD_RESET = "password_reset"
    PROBLEM_EMAIL = "problem_email"


class UtteranceEnum(object):
    SUGGEST = "utter_suggest"
    INVALID = "utter_invalid"
    NO_WIFI_NETWORK = "utter_no_wifi_network"
    EMAIL_NO_MATCH = "utter_email_no_match"
    EDUROAM_INSTRUCTIONS = "utter_eduroam_instructions"
    UCWIFI_INSTRUCTIONS = "utter_ucwifi_instructions"
    GUEST_WIFI_INSTRUCTIONS = "utter_guest_wifi_instructions"
    RECOVER_PASSWORD = "utter_recover_password"
    NO_PERSONAL_ID = "utter_no_personal_id"
    PRIORITY_NO_MATCH = "utter_priority_no_match"
    TICKET_NO = "utter_ticket_no"
    TICKET_STATUS = "utter_ticket_status"
    CONFIRM_REQUEST = "utter_confirm_request"
    PROCESS_FAILED = "utter_process_failed"
    PROCESS_CANCELLED = "utter_process_cancelled"
    CONFIRM_ASK_SUCCESS = "utter_confirm_ask_success"  # With default buttons
    CONFIRM_SUCCESS = "utter_confirm_success"  # Template to use custom buttons
    ACCEPT_AGREEMENT_FORM = "utter_ask_accept_agreement_form"
    OUT_OF_SCOPE = "utter_out_of_scope"


class TicketTypes(object):
    INCIDENT = 1
    REQUEST = 2


class GLPICategories(object):
    NETWORK_CONNECTIVITY = 52
    EMAIL_ISSUE = 53  # Correo electronico 41 ?
    EQUIP_MGMT = 54  # Equipos de Computo
    USER_MGMT = 56  # Gestion de usuarios
    DATA_REPORT = 60  # Reporte de datos
    MISC = 65  # Varios 61 ?


class DTICApplication(object):
    URKUND = "urkund"
    KOHA = "koha"
    GAS = "gas"


class RasaConstants(object):
    # Intents
    INTENT_RANKING_KEY = "intent_ranking"
    DEFAULT_NLU_FALLBACK_INTENT_NAME = "nlu_fallback"
    # Actions
    ACTION_DEFAULT_ASK_AFFIRMATION_NAME = "action_default_ask_affirmation"
