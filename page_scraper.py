import csv
import sys
from os.path import exists

from errorify import errorify
from fb_scraper import Scraper, exceptions

from constants import PAGE_HEADER_NAMES

PAGE_ID = 'CocaColaBGD'
COOKIES = ['lipa.txt', 'lubana.txt', 'sharmin.txt']
COMMUNITY = 'Beverage'
PAGE_URL = f'https://mbasic.facebook.com/{PAGE_ID}'
PAGE_NAME = 'Coca-Cola Bangladesh'
PAGE_ABOUT = 'Coca-cola beverage company'
FILE_NAME = f'{PAGE_ID}.csv'
START_URL = None

scraper = Scraper(COOKIES)

next_url = None
total_posts_count = 0

if not exists(f'files/{FILE_NAME}'):
    with open(f'files/{FILE_NAME}', 'w', encoding='utf-8', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(PAGE_HEADER_NAMES)

while True:
    try:
        print(f'Total Posts Scraped: {total_posts_count}')

        if not next_url:
            data = scraper.get_page_posts_by_page_id(page_id=PAGE_ID, start_url=START_URL)
        else:
            data = scraper.get_page_posts_by_page_id(page_id=PAGE_ID, start_url=next_url)

        print(f'Next URL: {data["next_url"]}')
        next_url = data['next_url']

        if not next_url:
            print('This page might not have any posts available')
            break

        with open('next_url.txt', 'w', newline='', encoding='utf-8') as f:
            f.write(str(next_url))

        if data:
            page_posts = data['page_posts']
            total_posts_count += len(page_posts)

            for page_post in page_posts:
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
    except exceptions.RottenCookies as error:
        print(errorify(error))
        sys.exit()
    except Exception as error:
        print(errorify(error))
