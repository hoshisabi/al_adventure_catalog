import pathlib
import os
import logging
import sys
import json
import datetime
from collections import defaultdict

from adventure import DC_CAMPAIGNS, DungeonCraft
import glob

logger = logging.getLogger()
logger.level = logging.INFO
stream_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stream_handler)

root = str(pathlib.Path(__file__).parent.absolute())
input_path = os.path.join(root, '_stats')








def __get_dc_per_month(data):
    result = defaultdict(list)
    for dc in data:
        month = dc.convert_date_to_readable_str()
        result[month].append(dc)
    return result


def __sort_formatted_dates(dates):
    def sort_key(date_str):
        year, month_str = date_str.split(", ")
        month_num = datetime.datetime.strptime(month_str, "%b").month  # Convert month name to number
        return year, month_num

    return sorted(dates, key=sort_key)


def summarize(data, dc_season):
    logger.info(f"")
    logger.info(f"Stats for {dc_season}")
    logger.info(f"\nDC count {len(data)}")

    logger.info(f"\nTier split")
    t1_dcs = list(filter(lambda k: k.is_tier(1), data))
    t2_dcs = list(filter(lambda k: k.is_tier(2), data))
    t3_dcs = list(filter(lambda k: k.is_tier(3), data))
    t4_dcs = list(filter(lambda k: k.is_tier(4), data))
    tier_unknown = list(filter(lambda k: k.is_tier_unknown(), data))

    logger.info(f"    t1={len(t1_dcs)}")
    logger.info(f"    t2={len(t2_dcs)}")
    logger.info(f"    t3={len(t3_dcs)}")
    logger.info(f"    t4={len(t3_dcs)}")
    logger.info(f"    ??={len(tier_unknown)}")

    logger.info(f"\nHour split")
    h2_dcs = list(filter(lambda k: k.is_hour(2), data))
    h4_dcs = list(filter(lambda k: k.is_hour(4), data))
    hour_unknown = list(filter(lambda k: k.is_hour_unknown(), data))

    logger.info(f"    2h={len(h2_dcs)}")
    logger.info(f"    4h={len(h4_dcs)}")
    logger.info(f"    ??={len(hour_unknown)}")

    logger.info(f"\nTime split (grouped by month)")
    dc_per_month = __get_dc_per_month(data)

    for month in __sort_formatted_dates(dc_per_month.keys()):
        logger.info(f"    {month} =\t{len(dc_per_month[month])}")


input_season = 'FR-DC'

if __name__ == '__main__':
    if len(sys.argv) > 1:
        input_season = sys.argv[1]

    print(f"Printing stats for {input_season} season.")
    for dc_season in DC_CAMPAIGNS.keys():
        # TODO: add flag
        if input_season == dc_season:
            output_full_path = f"{str(input_path)}/{dc_season}.json"
            with open(output_full_path) as f:
                raw_data = json.load(f)
                data = []
                for d in raw_data:
                    # Rename 'full_title' to 'title' for DungeonCraft constructor
                    d['title'] = d.pop('full_title')
                    # Convert date_created string to datetime.date object
                    d['date_created'] = datetime.datetime.strptime(d['date_created'], "%Y%m%d").date()
                    data.append(DungeonCraft(**d))

                summarize(data, dc_season)
    # crawl_dc_listings(page_number=2, max_results=15)
