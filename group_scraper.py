import csv
from os.path import exists

from fb_scraper import get_group_posts_by_group_id

from constants import GROUP_HEADER_NAMES

GROUP_ID = '140473731634479'
COOKIES_NAME = ['nila.txt']
COMMUNITY = 'Information'
GROUP_URL = f'https://mbasic.facebook.com/groups/{GROUP_ID}'
GROUP_NAME = 'HM Tour & Travels (ট্রাভেলিং গ্রুপ)'
GROUP_ABOUT = 'Travel Group'
FILE_NAME = f'{GROUP_ID}.csv'
START_URL = None

page = 1
cookie_files = f'cookies/{COOKIES_NAME[0]}'
next_url = None
total_posts_count = 0

if not exists(f'files/{FILE_NAME}'):
    with open(f'files/{FILE_NAME}', 'w', encoding='utf-8', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(GROUP_HEADER_NAMES)

while True:
    print(f'Total Posts Scraped: {total_posts_count}')
    if not next_url:
        data = get_group_posts_by_group_id(group_id=GROUP_ID, cookies=cookie_files, start_url=START_URL)
    else:
        data = get_group_posts_by_group_id(group_id=GROUP_ID, cookies=cookie_files, start_url=next_url)

    print(f'Next URL: {data["next_url"]}')
    next_url = data['next_url']

    if not next_url:
        print('This group might not have any posts available')
        print(f'or {cookie_files} cookie is invalid')
        cookie_index = page % len(COOKIES_NAME)
        cookie_files = f'cookies/{COOKIES_NAME[cookie_index]}'
        print(f'Cookie Using: {COOKIES_NAME[cookie_index]}')
        continue

    print(next_url)
    with open('next_url.txt', 'w', newline='', encoding='utf-8') as f:
        f.write(str(next_url))

    page += 1
    cookie_index = page % len(COOKIES_NAME)
    cookie_files = f'cookies/{COOKIES_NAME[cookie_index]}'
    print(f'Cookie Using: {COOKIES_NAME[cookie_index]}')

    if data:
        group_posts = data['group_posts']
        total_posts_count += len(group_posts)

        for group_post in group_posts:
            copy_dict = {}

            for header in GROUP_HEADER_NAMES:
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
