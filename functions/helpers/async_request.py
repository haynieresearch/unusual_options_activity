#**********************************************************
#* CATEGORY	SOFTWARE
#* GROUP	MARKET DATA
#* AUTHOR	LANCE HAYNIE <LANCE@HAYNIEMAIL.COM>
#* DATE		2020-10-20
#* PURPOSE	UNUSUAL OPTIONS ACTIVITY
#* FILE		ASYNC_REQUEST.PY
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
import asyncio
import  pyppeteer
from user_agent import generate_user_agent
from requests_html import AsyncHTMLSession
from functions.helpers.parser import UOAParse
from functions.helpers.errors import HttpErrors, TimeoutError, MissingParserType

class AsyncRequest:
	def __init__(self, base_url, number_of_requests, timeout=1000, parser_type=None):
		self.base_url   		= base_url
		self.number_of_requests = number_of_requests
		self.parser_type 		= parser_type
		self.timeout			= timeout
		self.data				= []

	@property
	def parser_type(self):
		return self._parser_type

	@parser_type.setter
	def parser_type(self, data):
		if not data:
			raise MissingParserType
		self._parser_type = data

	async def make_requests(self, url):
		session = AsyncHTMLSession()
		response = await session.get(url, headers={'User-Agent': generate_user_agent()})
		HttpErrors.handle_errors(response)
		try:
			response_url = await response.html.arender(wait=5.0, timeout=self.timeout, script=self.js_script())
		except pyppeteer.errors.TimeoutError:
			raise TimeoutError

		if self._is_unique_page_request(response.html.url, response_url):
			parser = self.parser_type(response)
			parser.get_table_headers()
			parser.get_table_body()
			self.data.extend(parser.data)

		await session.close()

	async def main(self):
		"""Runs subsequent requests after the initial request"""
		#network erros occuring when multiple tasks created pyppeteer.errors.NetworkError
		# tasks = []
		for i in range(2, self.number_of_requests+2):
			url = self.base_url +f'/?page={i}'
			await self.make_requests(url)
		# 	tasks.append(
		# 		self.make_requests(url)
		# 	)
		# results = await asyncio.gather(*tasks)

	def js_script(self):
		"""Gets the web page url by javascript"""
		script = """
			() => { return window.location.href }
		"""
		return script

	def _is_unique_page_request(self, request_url, response_url):
		"""Barchart will redirect requests if a query params is invalid"""
		return request_url == response_url


	def run(self):
		run_async = asyncio.get_event_loop()
		run_async.run_until_complete(self.main())
