#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# Import products to given bank_id
#
# Usage: ./import_products.py <csv file> <bank_id>


import sys

from obp_api_scripts.import_data.products import ImportProducts


ImportProducts(sys.argv).run()
