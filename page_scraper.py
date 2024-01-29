import csv
from os.path import exists

from fb_scraper import get_page_posts_by_page_id

from constants import PAGE_HEADER_NAMES

PAGE_ID = 'earkidotcom'
COOKIES_NAME = ['keye.txt']
COMMUNITY = 'Information'
PAGE_URL = f'https://mbasic.facebook.com/{PAGE_ID}'
PAGE_NAME = 'Earki'
PAGE_ABOUT = 'Comedy'
FILE_NAME = f'{PAGE_ID}.csv'
START_URL = None

page = 1
post_ids = []
next_url = None

if not exists(f'files/{FILE_NAME}'):
    with open(f'files/{FILE_NAME}', 'w', encoding='utf-8', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(PAGE_HEADER_NAMES)

while True:
    if not next_url:
        data = get_page_posts_by_page_id(page_id=PAGE_ID, cookies=f'cookies/{COOKIES_NAME[0]}', start_url=START_URL)
    else:
        data = get_page_posts_by_page_id(page_id=PAGE_ID, cookies=f'cookies/{COOKIES_NAME[0]}', start_url=next_url)

    print(f'Next URL: {data["next_url"]}')
    next_url = data['next_url']

    if not next_url:
        break

    print(next_url)
    with open('next_url.txt', 'w', newline='', encoding='utf-8') as f:
        f.write(str(next_url))

    page += 1
    cookie_index = page % len(COOKIES_NAME)
    print(f'Cookie Using: {COOKIES_NAME[cookie_index]}')

    if data:
        page_posts = data['page_posts']

        for page_post in page_posts:
            if page_post['post_id'] not in post_ids:
                copy_dict = {}

                for header in PAGE_HEADER_NAMES:
                    if header in list(page_post.keys()):
                        copy_dict[header] = page_post[header]
                    else:
                        copy_dict[header] = None

                copy_dict['community'] = COMMUNITY
                copy_dict['page_id'] = PAGE_ID
                copy_dict['page_url'] = PAGE_URL
                copy_dict['page_name'] = PAGE_NAME
                copy_dict['page_about'] = PAGE_NAME

                if exists(f'files/{FILE_NAME}'):
                    with open(f'files/{FILE_NAME}', 'a', newline='', encoding='utf-8') as f:
                        writer = csv.DictWriter(f, fieldnames=copy_dict.keys())
                        writer.writerow(copy_dict)
                else:
                    with open(f'files/{FILE_NAME}', 'a', newline='', encoding='utf-8') as f:
                        writer = csv.DictWriter(f, fieldnames=copy_dict.keys())
                        writer.writeheader()
                        writer.writerow(copy_dict)

                post_ids.append(page_post['post_id'])