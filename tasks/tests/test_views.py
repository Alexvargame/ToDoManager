from django.test import TestCase

# Create your tests here.

from costs.models import Cost, CategoryCost
from django.contrib.auth.models import User

from django.urls import reverse
import datetime


class CostListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        #Create 13 authors for pagination tests
        number_of_costs = 13
        user = User.objects.create(id=1)
        category = CategoryCost.objects.create(id=1)
        for cost_num in range(number_of_costs):
            cls.cost = Cost.objects.create(
                user=user,
                category=category,
                cost_date=datetime.datetime.now(),
                cost_name='Еда',
                cost_sum=100.00
            )



    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/costs/costs/')
        self.assertEqual(resp.status_code, 302)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('costs_front_list_url'))
        self.assertEqual(resp.status_code, 302)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('costs_front_list_url'))
        self.assertEqual(resp.status_code, 302)
        self.client.login(username='alex', password='admin')
        print(resp)
        # self.assertTemplateUsed(resp, '/costs/costs_list.html')

    # def test_pagination_is_ten(self):
    #     resp = self.client.get(reverse('authors'))
    #     self.assertEqual(resp.status_code, 200)
    #     self.assertTrue('is_paginated' in resp.context)
    #     self.assertTrue(resp.context['is_paginated'] == True)
    #     self.assertTrue( len(resp.context['author_list']) == 10)
    #
    # def test_lists_all_authors(self):
    #     #Get second page and confirm it has (exactly) remaining 3 items
    #     resp = self.client.get(reverse('authors')+'?page=2')
    #     self.assertEqual(resp.status_code, 200)
    #     self.assertTrue('is_paginated' in resp.context)
    #     self.assertTrue(resp.context['is_paginated'] == True)
    #     self.assertTrue( len(resp.context['author_list']) == 3)

class CostListByUser(TestCase):

    def setUp(self):
        test_user1 = User.objects.create_user(username='testuser1', password='12345')
        test_user1.save()
        test_user2 = User.objects.create_user(username='testuser2', password='12345')
        test_user2.save()
        number_of_costs = 13
        category = CategoryCost.objects.create(id=1)
        for cost_num in range(number_of_costs):

            cost = Cost.objects.create(
                user=test_user1 if cost_num//2 else test_user2,
                category=category,
                cost_date=datetime.datetime.now(),
                cost_name='Еда',
                cost_sum=100.00
            )
            cost.save()

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/costs/costs/')
        self.assertEqual(resp.status_code, 302)

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('report_cost_url'))
        self.assertRedirects(resp, '/login/?next=/costs/reports/')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='testuser1', password='12345')
        resp = self.client.get(reverse('report_cost_url'))

        # Проверка что пользователь залогинился
        self.assertEqual(str(resp.context['user']), 'testuser1')
        # Проверка ответа на запрос
        self.assertEqual(resp.status_code, 200)

        # Проверка того, что мы используем правильный шаблон
        self.assertTemplateUsed(resp, 'costs/report.html')