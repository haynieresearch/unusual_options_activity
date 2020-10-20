#**********************************************************
#* CATEGORY	SOFTWARE
#* GROUP	MARKET DATA
#* AUTHOR	LANCE HAYNIE <LANCE@HAYNIEMAIL.COM>
#* DATE		2020-10-20
#* PURPOSE	UNUSUAL OPTIONS ACTIVITY
#* FILE		PARSER.PY
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
from functions.helpers.errors import ParsingError

class BaseParser:
	def __init__(self, body):
		self.body 				= body
		self.table_headers 		= None
		self.data 				= []


class UOAParse(BaseParser):
	def __init__(self, body):
		super(UOAParse, self).__init__(body)

	def get_table_headers(self):
		"""Returns array of table header titles"""
		try:
			self.table_headers = self.body.html.find('table thead tr')[0].text.split('\n')[0:15]
		except IndexError:
			raise ParsingError(msg='Index error on table headers, check response')
		if len(self.table_headers) < 15:
			raise ParsingError(msg='table headers collection is less than 15, check response')

	def get_table_body(self):
		"""Returns collection of table body data"""
		table_body_collection = self.body.html.find('table tbody tr')[0:]
		for row in table_body_collection:
			try:
				row_data = row.text.split('\n')[0:]
				if len(row_data) < 15:
					raise ParsingError(msg='table body collection is less than 15, check response')
				obj_struct = dict(zip(self.table_headers, row_data))
				self.data.append(obj_struct)
			except IndexError:
				raise ParsingError(msg='Index error on table body, check response')
