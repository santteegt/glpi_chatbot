# -*- coding: utf-8 -*-

from datetime import datetime
from future.utils import viewitems
from glpi import GLPI
import logging
import os
import re
import requests
import ruamel.yaml
import sys
from typing import Any, Dict, Optional, Text

if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

logger = logging.getLogger(__name__)


class Ticket(TypedDict, total=False):
	ticket_no: Optional[int]  # Generated
	username: Optional[Text]  # Optional
	title: Text
	description: Text
	priority: Optional[int]  # Optional (Set by GLPI)
	requesttypes_id: Optional[int]  # Default value
	itilcategories_id: Optional[int]  # Default value
	alternative_email: Optional[Text]  # Optional


def load_glpi_config(config_file="glpi_credentials.yml"):
	"""
	Load configuration setting to setup  the GLPI API
	:param config_file: config filename
	:return: tuple-like with config settings (uri, app_token, auth_token, local_mode)
	"""
	glpi_config = {}
	try:
		glpi_config = ruamel.yaml.safe_load(open(config_file, "r"))
	except Exception as e:
		logger.warning(f"{config_file} NOT FOUND")
	glpi_api_uri = os.environ.get("GLPI_API_URI") if os.environ.get("GLPI_API_URI") else glpi_config.get("uri")
	glpi_app_token = os.environ.get("GLPI_APP_TOKEN") if os.environ.get("GLPI_APP_TOKEN") else glpi_config.get("app_token")
	glpi_auth_token = os.environ.get("GLPI_AUTH_TOKEN") if os.environ.get("GLPI_AUTH_TOKEN") else glpi_config.get("auth_token")
	local_mode = os.environ.get("GLPI_LOCALMODE") if os.environ.get("GLPI_LOCALMODE") else glpi_config.get("localmode", True)

	if not os.environ.get("GLPI_CONFIG_LOADED"):
		os.environ["GLPI_CONFIG_LOADED"] = "1"
		logger.info(f"GLPI Helpdesk settings in {config_file}: "
		            f"URI: {glpi_api_uri} | Auth Token?: {glpi_app_token is not None}"
		            f"| App Token?: {glpi_auth_token is not None} | Local Mode?: {local_mode}")

	return glpi_api_uri, glpi_app_token, glpi_auth_token, local_mode


class GLPIService(object):
	"""
	Connect to a GLPI instance using its API
	It requires the following the following parameters;
		uri: GLPI API URI
		auth_token: Authentication token obtained by a registered user on GLPI (API Token on User Settings)
						You must set the "Enable login with external token" to "Yes" under Setup > General > API
		app_token: GLPI API Token (generated on Setup > General > API)
	"""

	__instance = None

	@staticmethod
	def get_instance(uri, app_token, auth_token):
		"""Singleton pattern"""
		if not GLPIService.__instance:
			GLPIService(uri, app_token, auth_token)
		return GLPIService.__instance

	def __init__(self, uri, app_token, auth_token, *args, **kwargs):
		if not GLPIService.__instance:
			super(GLPIService, self).__init__(*args, **kwargs)

			if uri is None or app_token is None or auth_token is None:
				raise GlpiException(f"parameters missing:  uri{uri is None}| app_token: {app_token is None}"
									f"| auth_token: {auth_token is None}")
			self.base_uri = uri
			self.glpi: GLPI = GLPI(uri, app_token, auth_token)
			session = self.glpi.init_api()
			self.headers = {
				"App-Token": app_token,
				"Content-Type": "application/json",
				"Session-Token": session['session_token']
			}
			session_data = self.glpi.get('getFullSession')['session']
			self.agent_id = session_data['glpiID']
			self.agent_username = session_data['glpiname']
			GLPIService.__instance = self

	def get_ticket(self, ticket_id: Text):
		"""
		Get ticket info by ID
		:param ticket_id: integer identifier
		:return: Ticket metadata
		"""
		return self.glpi.get('ticket', ticket_id)

	def get_ticket_status(self, ticket_id: Text):
		"""
		Get ticket specific metadata about its status
		:param ticket_id: integer identifier
		:return: Ticket metadata based on metacriteria
		"""
		metacriteria = [{
			'id': '1',
			'field': 'name'  # title
		}, {
			'id': '7',
			'field': 'completename'  # category name
		}, {
			'id': '2',
			'field': 'id'
		}, {
			'id': '14',
			'field': 'type'
		}, {
			'id': '12',
			'field': 'status'
		}, {
			'id': '4',
			'field': 'user_id'  # name
		}, {
			'id': '9',
			'field': 'source'  # name
		}, {
			'id': '35',
			'field': 'use_notification'
		}, {
			'id': '34',
			'field': 'alternative_email'  # name
		}, {
			'id': '10',
			'field': 'urgency'
		}, {
			'id': '11',
			'field': 'impact'
		}, {
			'id': '3',
			'field': 'priority'
		}, {
			'id': '15',
			'field': 'date'  # opendate
		}, {
			'id': '16',
			'field': 'closedate'
		}, {
			'id': '17',
			'field': 'solvedate'
		}, {
			'id': '18',
			'field': 'time_to_solve'
		}]
		full_url = f'{self.base_uri}/search/ticket?criteria[0][field]=2&criteria[0][value]={ticket_id}' + \
		           '&criteria[0][searchtype]=equals'

		for idx, meta in enumerate(metacriteria):
			full_url += '&forcedisplay[%d]=%s' % (idx, meta['id'])

		opts = self.glpi.search_options('ticket')
		r = requests.request('GET', full_url, headers=self.headers)
		if r.status_code != 200:
			raise GlpiException(f'Failed to fetch info about ticket: {ticket_id} Reason: {r.reason}')
		json_data = r.json()
		data = json_data['data'] if 'data' in json_data else []
		return {opts[k]['field']: v for k, v in data[0].items()}

	def get_user(self, username: Text):
		"""
		Get user basic information
		:param username: username used for authentication
		:return: User data fields specified in the metacriteria (see below)
		Example:
			{'name': john.doe,
			'id': 5,
			'firstname': 'John',
			'realname': 'Doe',
			'email': 'jhon.doe@ucuenca.edu.ec',
			'is_active': 1}
		"""
		user_criteria: Dict = {
			'criteria': [
				{
					'searchtype': 'contains',
					'field': 1,  # name
					'value': username
				}
			],
			'metacriteria': [
				{
					'id': '1',
					'field': 'name'
				},
				{
					'id': '2',
					'field': 'id'
				},
				{
					'id': '9',
					'field': 'firstname'
				},
				{
					'id': '34',
					'field': 'realname'
				},
				{
					'id': '5',
					'field': 'email'
				},
				{
					'id': '8',
					'field': 'is_active'
				}
			]
		}

		opts = self.glpi.search_options('user')
		uri_query = self.build_user_query(user_criteria, opts)
		full_url = f'{self.base_uri}/search/{uri_query}'
		r = requests.request('GET', full_url, headers=self.headers)
		if r.status_code != 200:
			raise GlpiException(f'Failed to fetch info about username: {username} Reason: {r.reason}')
		json_data = r.json()
		data = json_data['data'] if 'data' in json_data else []
		return {opts[k]['field']: v for k, v in data[0].items()}

	def create_ticket(self, ticket: Ticket, ticket_type: int = 1) -> Dict[Text, Any]:
		"""
		Post a new ticket on the GLPI system and assign roles properly
		:param ticket: Ticket data to be publihsed
		:param ticket_type: Ticker type: Incident: 1 | Request: 2
		:return: id and message from the published ticket
			Schema: { 'id': int, 'message': str }
		"""
		requesttypes_id_default = 41  # TODO: Communication but TBD
		itilcategories_id_default = 65  # TODO: Various but TBD
		date_string = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

		user = self.get_user(ticket['username']) if 'username' in ticket else None
		new_ticket: Dict = {
			'name': ticket['title'],
			'date': date_string,
			'status': 1,
			'_users_id_recipient': self.agent_id,  # User Id from session
			'_users_id_requester': self.agent_id,
			'requesttypes_id': requesttypes_id_default if 'requesttypes_id' not in ticket else ticket['requesttypes_id'],
			'content': ticket['description'],
			# 'urgency': 3,  # medium
			# 'impact': 2,  # low
			# 'priority': ticket['priority'],  # low:2 | medium:3 | high:4
			'itilcategories_id': itilcategories_id_default if 'itilcategories_id' not in ticket else ticket['itilcategories_id'],
			'type': ticket_type,
			'date_creation': date_string,
		}

		try:
			# logger.info(f'Request body to GLPI: {new_ticket} | session: {self.glpi.api_session}')
			# {id: int, message: str}
			rs = self.glpi.create('ticket', new_ticket)
			# logger.info(f'Response from GLPI: {rs}')
			if 'id' in rs:
				ticket['ticket_no'] = rs['id']
				self.assign_ticket(ticket, user_id=user['id'] if user is not None else None)
			elif type(rs) == list:
				raise GlpiException(f'Error during GLPI API call: {rs}')

		except Exception as e:
			raise GlpiException(f'Failed to create ticket on the GLPI instance: {e}')

		return rs

	def build_user_query(self, criteria: Dict, opts) -> Text:
		"""
		Build query string for querying a user metadata
		:param criteria: Specify conditions and metadata to retrieve
		:param opts: Available fields on the user entity
		:return: a query string specifying conditions and metatada
		"""
		field_map = {}
		item_name = 'user'
		for field_id, field_opts in viewitems(opts):
			if field_id.isdigit() and 'uid' in field_opts:
				# support case-insensitive strip from item_name!
				field_name = re.sub('^' + item_name + '.', '', field_opts['uid'], flags=re.IGNORECASE)
				field_map[field_name] = int(field_id)

		uri_query = f'{item_name}?'

		for idx, c in enumerate(criteria['criteria']):
			# build field argument
			if idx == 0:
				uri = ""
			else:
				uri = "&"
			if 'field' in c and c['field'] is not None:
				field_name = ""
				# if int given, use it directly
				if isinstance(c['field'], int) or c['field'].isdigit():
					field_name = int(c['field'])
				# if name given, try to map to an int
				elif c['field'] in field_map:
					field_name = field_map[c['field']]
				else:
					raise GlpiException(
						'Cannot map field name "' + c['field'] + '" to ' +
						'a field id for ' + str(idx + 1) + '. criterion ' + str(c))
				uri = uri + f"criteria[{idx}][field]={field_name}"
			else:
				raise GlpiException(
					'Missing "field" parameter for ' + str(idx + 1) +
					'the criteria: ' + str(c))

			# build value argument
			if 'value' not in c or c['value'] is None:
				uri = uri + f"&criteria[{idx}][value]="
			else:
				uri = uri + f"&criteria[{idx}][value]={c['value']}"

			# build searchtype argument
			# -> optional! defaults to "contains" on the server if empty
			if 'searchtype' in c and c['searchtype'] is not None:
				uri = uri + f"&criteria[{idx}][searchtype]={c['searchtype']}"
			else:
				uri = uri + f"&criteria[{idx}][searchtype]="

			# link is optional for 1st criterion according to docs...
			# -> error if not present but more than one criterion
			if 'link' not in c and idx > 0:
				raise GlpiException(
					'Missing link type for ' + str(idx + 1) + '. criterion ' + str(c))
			elif 'link' in c:
				uri = uri + f"&criteria[{idx}][link]={c['link']}"

			# add this criterion to the query
			uri_query = uri_query + uri

		for idx, meta in enumerate(criteria['metacriteria']):
			uri_query = uri_query + f"&forcedisplay[{idx}]={meta['id']}"

		return uri_query

	def assign_ticket(self, ticket: Ticket, user_id: int = None):
		"""
		Update user roles to assign requester to the actual user that reports the incident
		while ticket sender through the API is set as Watcher
		:param ticket: metadata of the newly created ticket
		:param user_id: ID of actual user that reports the incident
		"""
		full_url = f'{self.base_uri}/Ticket/{ticket["ticket_no"]}/Ticket_User/'
		# Fetch current user involved in Ticket
		r = requests.request('GET', full_url, headers=self.headers)
		if r.status_code != 200:
			raise GlpiException(f'Failed to fetch people involved in ticket: {ticket["ticket_no"]} Reason: {r.reason}')
		people = r.json()
		requester = list(filter(lambda x: x['type'] == 1, people))[0]
		assigned = list(filter(lambda x: x['type'] == 2, people))[0]

		if user_id is not None or "alternative_email" in ticket:
			requester_payload = {
				"input": [{
					"id": requester['id'],
					"tickets_id": ticket["ticket_no"],
					"users_id": user_id if user_id is not None else requester['users_id'],
					"type": requester['type'],  # Requester:1 | Assign: 2 | Observer:3
					"use_notification": 1
				}]
			}
			if "alternative_email" in ticket:
				requester_payload["input"][0]["alternative_email"] = ticket['alternative_email']
			# Update requester role on the created ticket
			r = requests.request('PUT', full_url, headers=self.headers, json=requester_payload)
			if r.status_code != 200:
				error_msg = f'Failed to update user {user_id} with requester role on ticket: {ticket["ticket_no"]} '
				error_msg += f'Reason: {r.reason} Payload: {requester_payload}'
				raise GlpiException(error_msg)

		assigned_payload = {
			"input": [{
				"id": assigned['id'],
				"tickets_id": ticket['ticket_no'],
				"users_id": assigned['users_id'],
				# "type": assigned['type'],  # Requester:1 | Assign: 2 | Observer:3
				# "use_notification": assigned['use_notification'],
				# # 'alternative_email': assigned['alternative_email'] if len(
				# # 	assigned['alternative_email']) > 0 else 'chatbot@ucuenca.edu.ec',
			}]
		}
		# Delete assigned role on the created ticket
		r = requests.request('DELETE', full_url, headers=self.headers, json=assigned_payload)
		if r.status_code != 200:
			raise GlpiException(f'Failed to update user roles on ticket: {ticket["ticket_no"]} Reason: {r.reason}')

	@staticmethod
	def priority_values():
		return {
			'baja': 2,
			'media': 3,
			'alta': 4
		}


class GlpiException(Exception):
	"""
	A custom exception for the GLPIService
	"""
	pass
