#**********************************************************
#* CATEGORY	SOFTWARE
#* GROUP	MARKET DATA
#* AUTHOR	LANCE HAYNIE <LANCE@HAYNIEMAIL.COM>
#* DATE		2020-10-20
#* PURPOSE	UNUSUAL OPTIONS ACTIVITY
#* FILE		UOA.PY
#**********************************************************
#* MODIFICATIONS
#* 2020-10-20 - LHAYNIE - INITIAL VERSION
#**********************************************************
#UNUSUAL OPTIONS ACTIVITY
#Copyright 2020 Haynie IPHC, LLC
#Developed by Haynie Research & Development, LLC
#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.#
#You may obtain a copy of the License at
#http://www.apache.org/licenses/LICENSE-2.0
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.
import json
import csv
from datetime import datetime
from requests_html import HTMLSession
from user_agent import generate_user_agent
from functions.helpers.errors import InvalidTimeoutValue, HttpErrors, ParsingError
from functions.helpers.pagination import Pagination
from functions.helpers.parser import UOAParse
from functions.helpers.async_request import AsyncRequest

class UOA:
	def __init__(self, file,url):
		self.timeout 			= 100
		self._total_records 	= None
		self._records_per_page  = None
		self._pages_to_paginate = None
		self.data 				= []
		self.file				= file
		self.url				= url
		self._report 			= self._generate_report()

	@property
	def timeout(self):
		return self._timeout

	@timeout.setter
	def timeout(self, data):
		if not data or type(data) is not int:
			raise InvalidTimeoutValue(data)
		self._timeout = data


	def _generate_report(self):
		init_req = self._initial_request()

	def _initial_request(self):
		session = HTMLSession()
		initial_response = session.get(self.url, headers={'User-Agent': generate_user_agent()})
		HttpErrors.handle_errors(initial_response)
		HttpErrors.handle_render_errors(initial_response.html.render, timeout=self.timeout)

		self._parse_pagination(initial_response)
		parser = UOAParse(initial_response)
		parser.get_table_headers()
		parser.get_table_body()
		self.data = parser.data

		if self._has_pagination():
			async_req = AsyncRequest(self.url, self._pages_to_paginate, parser_type=UOAParse)
			async_req.run()
			self.data.extend(async_req.data)

	def _parse_pagination(self, response):
		parse_pag = Pagination(response)
		parse_pag.get_pagination()
		parse_pag.calculate_pages_to_paginate()
		self._total_records 	= parse_pag.total_records
		self._records_per_page 	= parse_pag.per_page
		self._pages_to_paginate = parse_pag.pages_needed_to_paginate

	def _has_pagination(self):
		return bool(self._total_records) and bool(self._records_per_page) and bool(self._pages_to_paginate)

	def to_csv(self):
		keys = self.data[0].keys()
		with open(self.file, 'w', newline='') as file:
		    dict_writer = csv.DictWriter(file, keys)
		    dict_writer.writeheader()
		    dict_writer.writerows(self.data)
