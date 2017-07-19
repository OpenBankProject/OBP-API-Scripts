#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Import ATMs to given bank id
#
# Usage: ./import_atms.py <csv file> <bank_id>


import sys

from obp_api_scripts.import_data.atms import ImportATMs


ImportATMs(sys.argv).run()
