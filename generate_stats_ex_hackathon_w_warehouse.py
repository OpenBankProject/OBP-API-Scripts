#!/usr/bin/env python3

# Little script to answer a few questions about statistics not easily possible
# using SQL only. Run on the server where the API's database is deployed.
#
# Usage: ./generate_stats_ex_hackathon_w_warehouse.py

from obp_api_scripts.generate_stats.stats_ex_hackathon_w_warehouse import Stats


with Stats() as stats:
    stats.run_all()
