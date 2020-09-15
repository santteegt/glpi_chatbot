from actions.user_api import APIException, load_api_config, UserApi

# Loading Users API Config
uapi_base_uri, uapi_client_id, uapi_client_secret, uapi_local_mode = load_api_config()
users_api = (
    UserApi.get_instance(uapi_base_uri, uapi_client_id, uapi_client_secret)
    if not uapi_local_mode
    else None
)