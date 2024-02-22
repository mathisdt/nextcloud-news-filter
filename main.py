#!/usr/bin/env python3
#
# mark specific news items as read (so they don't show in the "unread" feed)
#
import base64
import sys
import logging
import os.path
import configparser
import re
from _datetime import datetime, timedelta
import requests

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        stream=sys.stdout)
    logging.debug('starting run')

    configfile = f"{os.path.realpath(os.path.dirname(__file__))}/config.ini"
    if not os.path.isfile(configfile):
        logging.log(logging.ERROR, f"{configfile} not found")
        exit(1)
    config = configparser.ConfigParser()
    config.read(configfile)

    if 'login' not in config:
        logging.log(logging.ERROR, 'configuration has to contain [login] section')
        exit(1)
    if 'address' not in config['login'] or config['login']['address'] == '':
        logging.log(logging.ERROR, 'configuration has to contain address in [login] section')
        exit(1)
    if 'username' not in config['login'] or config['login']['username'] == '' \
            or 'password' not in config['login'] or config['login']['password'] == '':
        logging.log(logging.ERROR, 'configuration has to contain username and password in [login] section')
        exit(1)
    token = base64.encodebytes((config['login']['username'] + ':' + config['login']['password'])
                               .encode(encoding='UTF-8')).decode(encoding='UTF-8').strip()

    filters = []
    for section in config:
        if section not in ['DEFAULT', 'login']:
            one_filter = {'name': section,
                          'feedId': int(config[section]['feedId']) if 'feedId' in config[section] else None,
                          'titleRegex': re.compile(config[section]['titleRegex'], re.IGNORECASE)
                          if 'titleRegex' in config[section] else None,
                          'bodyRegex': re.compile(config[section]['bodyRegex'], re.IGNORECASE)
                          if 'bodyRegex' in config[section] else None,
                          'minPubDate': int((datetime.now() - timedelta(hours=int(config[section]['hoursAge']))).timestamp()) if 'hoursAge' in config[section] else None}
            filters.append(one_filter)

    response = requests.get(url=config['login']['address'] + '/index.php/apps/news/api/v1-3/items',
                            headers=dict(Authorization=f"Basic {token}"),
                            json=dict(batchSize=-1,
                                      offset=0,
                                      type=3,
                                      id=0,
                                      getRead='false'))
    data = response.json()

    unread_item_count = 0
    matched_item_ids = []
    for item in data['items']:
        if item['unread']:
            unread_item_count = unread_item_count + 1
            for one_filter in filters:
                if ('feedId' not in one_filter
                    or one_filter['feedId'] is "NoneType"
                    or one_filter['feedId'] == item['feedId']) \
                        and ('titleRegex' not in one_filter
                             or one_filter['titleRegex'] is None
                             or one_filter['titleRegex'].search(item['title'])) \
                        and ('bodyRegex' not in one_filter
                             or one_filter['bodyRegex'] is None
                             or one_filter['bodyRegex'].search(item['body'])) \
                        and ('minPubDate' not in one_filter
                             or one_filter['minPubDate'] is None
                             or item['pubDate'] < one_filter['minPubDate']):
                    logging.log(logging.DEBUG,
                                f"filter {one_filter['name']} matched item {item['id']} with title {item['title']}")
                    matched_item_ids.append(item['id'])

    if matched_item_ids:
        logging.log(logging.INFO, f"marking as read: {len(matched_item_ids)} of {unread_item_count} items")
        requests.post(url=config['login']['address'] + '/index.php/apps/news/api/v1-3/items/read/multiple',
                      headers=dict(Authorization=f"Basic {token}"),
                      json=dict(itemIds=matched_item_ids))

    logging.debug('finished run')
