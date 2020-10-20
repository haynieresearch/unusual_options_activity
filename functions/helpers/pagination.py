#**********************************************************
#* CATEGORY	SOFTWARE
#* GROUP	MARKET DATA
#* AUTHOR	LANCE HAYNIE <LANCE@HAYNIEMAIL.COM>
#* DATE		2020-10-20
#* PURPOSE	UNUSUAL OPTIONS ACTIVITY
#* FILE		PAGINATION.PY
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
import re
import math

class Pagination:
	def __init__(self, body_response):
		self._body_response = body_response
		self.total_records = None
		self.per_page	   = None
		self.pages_needed_to_paginate = None

	def get_pagination(self):
		"""Retrieves the total amount of records and per page; occasionaly, pagianted_text will be empty"""
		try:
			paginated_text 		= self._body_response.html.find('.pagination-info')[0].text
			self.total_records	= int(re.search('of(.*)', paginated_text).group(1).strip())
			self.per_page  		= int(re.search('-(.*)of', paginated_text).group(1).strip())
		except:
			return None

	def calculate_pages_to_paginate(self):
		"""Number of pages needed for async requests"""
		if self.total_records and self.per_page:
			self.pages_needed_to_paginate  = math.ceil(self.total_records/self.per_page)-1
		else:
			self.pages_needed_to_paginate =  0
