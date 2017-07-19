#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# Import branches to given bank id
#
# Usage: ./import_branches.py <csv file> <bank_id>


import sys

from obp_api_scripts.import_data.branches import ImportBranches


ImportBranches(sys.argv).run()
