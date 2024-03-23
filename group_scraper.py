import csv
import sys
from os.path import exists

from errorify import errorify
from fb_scraper import Scraper
from fb_scraper.exceptions import RottenCookies

from constants import GROUP_HEADER_NAMES

GROUP_ID = 'weeforum'
COOKIES = ['khatun.txt', 'labbonno.txt', 'madison.txt', 'mhiya.txt', 'mim.txt']
COMMUNITY = 'Women'
GROUP_URL = f'https://mbasic.facebook.com/groups/{GROUP_ID}'
GROUP_NAME = 'Women Entrepreneurs and e-Commerce Forum (weeforum)'
GROUP_ABOUT = 'Discussion'
FILE_NAME = f'{GROUP_ID}.csv'
START_URL = 'https://mbasic.facebook.com/groups/289401598768855?bacr=1706690501%3A1120313032344370%3A1120313032344370%2C0%2C122%3A7%3AKw%3D%3D&multi_permalinks&eav=AfZLBlaBNA-CMSUbaw_3jYukaaft5ojCOnPyE6V2_5DC1FiJqXPnpIzVyt3T1WoKnKE&paipv=0&refid=18'

scraper = Scraper(COOKIES)

next_url = None
total_posts_count = 0

if not exists(f'files/{FILE_NAME}'):
    with open(f'files/{FILE_NAME}', 'w', encoding='utf-8', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(GROUP_HEADER_NAMES)

while True:
    try:
        print(f'Total Posts Scraped: {total_posts_count}')

        if not next_url:
            data = scraper.get_group_posts_by_group_id(group_id=GROUP_ID, start_url=START_URL)
        else:
            data = scraper.get_group_posts_by_group_id(group_id=GROUP_ID, start_url=next_url)

        print(f'Next URL: {data["next_url"]}')
        next_url = data['next_url']

        if not next_url:
            print('This group might not have any posts available')
            break

        with open('next_url.txt', 'w', newline='', encoding='utf-8') as f:
            f.write(str(next_url))

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
    except RottenCookies as error:
        sys.exit()
    except Exception as error:
        print(errorify(error))
