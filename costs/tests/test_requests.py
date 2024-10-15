from requests import head, get
from django.test import TestCase

import re

# response = head('http://127.0.0.1:8000/tasks/')
# print(response.status_code)

DOMAIN = 'http://127.0.0.1:8000/'

PAGES_200 = (
    'tasks/',
     # '',
)
PAGES_302 = (

    'costs/costs/',
    # 'costs/addmoney/',
    # 'costs/reports/',
    # 'profile/',
    # 'days'
)

LINK_REGULAR_EXPRESSION=r'<a[^>]* href="([^"]*)'
PAGES_200 = (DOMAIN + page for page in PAGES_200)
PAGES_302 = (DOMAIN + page for page in PAGES_302)
SITE_URL = 'https://'


def get_full_link(link):

    if not link.startswith('http'):
        link = SITE_URL + link

    return link

class PagesTests(TestCase):
    """Класс с тестами страниц"""

    def test_status_code(self):
        for page in PAGES_200:
            with self.subTest(f'{page=}'):
                response = head(page) # (1)

                self.assertEqual(response.status_code, 200) # (2) и (3)
        for page in PAGES_302:
            with self.subTest(f'{page=}'):
                response = head(page) # (1)

                self.assertEqual(response.status_code, 302)

    # def test_links(self):
    #
    #     valid_links = set()
    #     for page in PAGES_200:
    #         page_content = get(page).content
    #         page_links = set(re.findall(LINK_REGULAR_EXPRESSION, str(page_content)))
    #         page_links=['tasks/']#[l for l in page_links if not l.startswith('/costs')]
    #         print(page_links)
    #         for link in page_links:
    #             #link = link[1:]
    #             link = get_full_link(link)
    #             if link in valid_links:
    #                 continue
    #             with self.subTest(f'{link=} | {page=}'):
    #                 response = head(link, allow_redirects=True)
    #                 if response.status_code == 200:
    #                     valid_links.add(link)
    #                 self.assertEqual(response.status_code, 200)
