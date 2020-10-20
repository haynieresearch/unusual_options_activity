#!/usr/local/bin/python3.8
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
import sys
from functions import UOA

if len(sys.argv) == 1:
    args = sys.argv
    print("No option provided, use --help for options.")
    exit(0)
elif len(sys.argv) == 2:
    args = sys.argv
    arg1 = sys.argv[1]
elif len(sys.argv) == 3:
    args = sys.argv
    arg1 = sys.argv[1]
    arg2 = sys.argv[2]
elif len(sys.argv) == 4:
    args = sys.argv
    arg1 = sys.argv[1]
    arg2 = sys.argv[2]
    arg3 = sys.argv[3]
else:
    print("No option provided, use --help for options.")
    exit(0)

if len(args) > 1:
    if arg1.lower() == "--help":
        print("help stuff")

    elif arg1.lower() == "--stock":
        options = UOA(arg2,"https://www.barchart.com/options/unusual-activity/stocks")
        options.data
        options.to_csv()

    elif arg1.lower() == "--etf":
        options = UOA(arg2,"https://www.barchart.com/options/unusual-activity/etfs")
        options.data
        options.to_csv()

    elif arg1.lower() == "--check_config":
        print("Just making sure everything works!")

    else:
        print("Error: invalid option, use --help for options.")
else:
    print("No option provided, use --help for options.")

exit(0)
