from datetime import datetime, timedelta
import logging
import re
import requests
import ruamel.yaml
import os
import sys
from typing import Dict, Optional, Text

if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

logger = logging.getLogger(__name__)

OATH_ENDPOINT = '/oauth/token'
API_ENDPOINT = '/usuarios/existenCuentas'


class User(TypedDict, total=False):
	id: Text
	fullname: Text
	email: Text

def load_api_config(config_file="api_credentials.yml"):
    """
	Load configuration setting to setup the USers API
	:param config_file: config filename
	:return: tuple-like with config settings (base_uri, client_id, client_secret)
	"""
    api_config = {}
    try:
        yaml_config = ruamel.yaml.safe_load(open(config_file, "r"))
        api_config = yaml_config.get("users-api")
    except Exception as e:
        logger.warning(f"{config_file} NOT FOUND")
    api_base_uri = (
        os.environ.get("USERS_API_BASE_URI")
        if os.environ.get("USERS_API_BASE_URI")
        else api_config["base_uri"]
    )
    api_client_id = (
        os.environ.get("USERS_API_CLIENT_ID")
        if os.environ.get("USERS_API_CLIENT_ID")
        else api_config["client_id"]
    )
    api_client_secret = (
        os.environ.get("USERS_API_CLIENT_SECRET")
        if os.environ.get("USERS_API_CLIENT_SECRET")
        else api_config["client_secret"]
    )

    local_mode = not api_base_uri

    if not os.environ.get("USERS_API_CONFIG_LOADED"):
	    os.environ["USERS_API_CONFIG_LOADED"] = "1"
	    logger.info(
		    f"Users API settings: "
		    f"BASE_URI: {api_base_uri} | Cliend Id?: {api_client_id}"
		    f"| Client Secret?: {api_client_secret is not None} | Local Mode?: {local_mode}"
	    )

    return api_base_uri, api_client_id, api_client_secret, local_mode


class UserApi(object):
	"""
		Connects to the University of Cuenca Users API
		Useful to validate if a user exists per certain criteria (identity, email)
	"""

	base_uri: Text = None
	client_id: Text = None
	client_secret: Text = None
	access_token: Text = None
	token_type: Text = None
	delta_expires = None

	__instance__ = None

	@staticmethod
	def get_instance(base_uri: Text, client_id: Text, client_secret: Text) -> "UserApi":
		"""Singleton pattern"""
		if not UserApi.__instance__:
			UserApi(base_uri, client_id, client_secret)
		return UserApi.__instance__

	def __init__(self, base_uri: Text, client_id: Text, client_secret: Text):
		if not UserApi.__instance__:
			self.base_uri = base_uri
			self.client_id = client_id
			self.client_secret = client_secret
			self.__request_access_token__()
			UserApi.__instance__ = self

	def __request_access_token__(self):
		try:
			rs = requests.request('POST', f'{self.base_uri}{OATH_ENDPOINT}',
			                      data={
				                      'grant_type': 'client_credentials',
				                      'client_id': self.client_id,
				                      'client_secret': self.client_secret,
				                      'scope': 'read'
			                      }, timeout = 10)
			if rs.status_code == 200:
				token_data = rs.json()
				self.access_token = token_data['access_token']
				self.token_type = token_data['token_type']
				expires_in = token_data['expires_in']
				self.delta_expires = datetime.now() + timedelta(0, expires_in)
				logger.info(f'New Access token! Expires at {self.delta_expires}')
			else:
				raise APIException(f"Failed to get access token for API: {self.base_uri}{API_ENDPOINT}")
		except requests.exceptions.ConnectionError as err:
			raise APIException(f"API Service not available. {err}")

	def validate_user(self, identity: Text = None, email: Text = None) -> Optional[User]:
		if self.delta_expires <= datetime.now():
			logger.info('Access Token has expired!. Requesting a new one')
			self.__request_access_token__()

		criteria = {
			'type': 'CuentaUsuario',
		}
		if identity:
			criteria['identificacion'] = identity
		elif email:
			criteria['email'] = email
		else:
			raise APIException(f'At least one criteria must be provided: identity ({identity}) email ({email})')

		try:
			rs = requests.request('POST', f'{self.base_uri}{API_ENDPOINT}',
			                      headers={
				                      'Authorization': f'{self.token_type.capitalize()} {self.access_token}',
				                      'Content-Type': 'application/json'
			                      },
			                      json=criteria,
			                      timeout = 10,
			                      )
		except requests.exceptions.ConnectionError as err:
			raise APIException(f"API Service not available. {err}")
		if rs.status_code == 200:
			data = rs.json()
			if data['status'] == 'OK':
				managers = data['objeto']
				email_source = list(filter(lambda x: x['nombreGestor'] == 'GestorGmail', managers))
				email = email_source[0]['resultado']['mensaje'] if len(email_source) > 0 and email_source[0][
					'estaCorrecto'] else None
				oracle_source = list(filter(lambda x: x['nombreGestor'] == 'GestorOracle', managers))
				user_data = oracle_source[0]['resultado']['mensaje'] if len(oracle_source) > 0 and oracle_source[0][
					'estaCorrecto'] else None
				if user_data:
					regex = re.compile(r'\d+(?=\s\()|[\w\s]+(?=\))')
					rs = regex.findall(user_data)
					user_data = tuple(rs)  # (id, name)
				return User({
					'id': user_data[0],
					'fullname': user_data[1],
					'email': email
				})
			else:
				logger.info(f'User not found. Criteria {criteria}')
				return None
		else:
			error_data = rs.json()
			raise APIException(f"API returned status {rs.status_code}. Reason: {error_data['error']}")


class APIException(Exception):
	"""
	A custom exception for the UserApi
	"""

	pass
