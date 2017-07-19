#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# Import banks to the API
#
# Usage: ./import_banks.py <csv file>


import sys

from obp_api_scripts.import_data.banks import ImportBanks


ImportBanks(sys.argv).run()
