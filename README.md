# Unusual Options Activity Download [![Build Status](https://travis-ci.com/haynieresearch/unusual_options_activity.svg?branch=master)](https://travis-ci.com/haynieresearch/unusual_options_activity)
This program is designed to extract Unusual Options Activity from [Barchart](https://www.barchart.com/options/unusual-activity/stocks) as a local csv file.

## INSTALL
pip3 install -r requirements.txt

## USAGE
uoa.py --stock /path/of/your/choice/report.csv\
uoa.py --etf /path/of/your/choice/report.csv

## GOAL
The goal of this project is to enable automatic download of unusual options activity into our SAS environment which will be converted to SAS datasets.

## DEBUGGING HEADLESS
If you get a "BrowserError: Browser closed unexpectedly" Python will not give you a meaningful error message to trace. The best way to identify the error is to execute Python and type the command "from pyppeteer.launcher import Launcher" and then "' '.join(Launcher().cmd)" which will give you the command that it is executing. Exit Python and run that command, more than likely it is a dependency issue. Resolve any dependencies and then execute again, if there are no errors, you can execute this script without error.

## LICENSE
Copyright (c) 2020 Haynie IPHC, LLC\
Developed by Haynie Research & Development, LLC for Black Label Investment Partners, LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

<http://www.apache.org/licenses/LICENSE-2.0>

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
