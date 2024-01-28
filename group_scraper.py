import csv
from os.path import exists

from fb_scraper import get_group_posts_by_group_id

from constants import HEADER_NAMES

GROUP_ID = '140473731634479'
COOKIES_NAME = ['tuli.txt', 'keye.txt']
COMMUNITY = 'Information'
GROUP_URL = f'https://mbasic.facebook.com/groups/{GROUP_ID}'
GROUP_NAME = 'HM Tour & Travels (ট্রাভেলিং গ্রুপ)'
GROUP_ABOUT = 'Travel Group'
FILE_NAME = f'{GROUP_ID}.csv'
START_URL = None

page = 1
post_ids = []
next_url = None

if not exists(f'files/{FILE_NAME}'):
    with open(f'files/{FILE_NAME}', 'w', encoding='utf-8', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(HEADER_NAMES)

while True:
    if not next_url:
        data = get_group_posts_by_group_id(group_id=GROUP_ID, cookies=f'cookies/{COOKIES_NAME[0]}', start_url=START_URL)
    else:
        data = get_group_posts_by_group_id(group_id=GROUP_ID, cookies=f'cookies/{COOKIES_NAME[0]}', start_url=next_url)

    print(f'Next URL: {data["next_url"]}')
    next_url = data['next_url']

    if not next_url:
        break

    cookie_index = page % len(COOKIES_NAME)
    print(f'Cookie Using: {COOKIES_NAME[cookie_index]}')

    if data:
        group_posts = data['group_posts']

        for group_post in group_posts:
            print(group_post['post_id'])
            copy_dict = {}

            for header in HEADER_NAMES:
                if header in list(group_post.keys()):
                    copy_dict[header] = group_post[header]
                else:
                    copy_dict[header] = None

            copy_dict['community'] = COMMUNITY
            copy_dict['group_id'] = GROUP_ID
            copy_dict['group_url'] = GROUP_URL
            copy_dict['group_name'] = GROUP_NAME
            copy_dict['group_about'] = GROUP_NAME

            if exists(f'files/{FILE_NAME}'):
                with open(f'files/{FILE_NAME}', 'a', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=copy_dict.keys())
                    writer.writerow(copy_dict)
            else:
                with open(f'files/{FILE_NAME}', 'a', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=copy_dict.keys())
                    writer.writeheader()
                    writer.writerow(copy_dict)
