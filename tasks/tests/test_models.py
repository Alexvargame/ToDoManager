# import datetime
#
# from django.test import TestCase
#
# from costs.models import Cost,CategoryCost,DayCost
# from django.contrib.auth.models import User
#
#
# def run_field_parameter_test(model, self_, field_and_parameter_value, parameter_name):
#     for instance in model.objects.all():
#         for field, expected_value in field_and_parameter_value.items():
#             parameter_real_value = getattr(instance._meta.get_field(field), parameter_name)
#             self_.assertEqual(parameter_real_value, expected_value)
# class TestVerboseNameMixin:
#
#     def run_verbose_name_test(self, model):
#         run_field_parameter_test(model,self,self.field_and_verose_name,'verbose_name')
#
# class TestMaxLengthMixin:
#
#     def run_max_length_test(self, model):
#         run_field_parameter_test(model, self, self.field_and_max_length, 'max_length')
#
#
# class CostTests(TestCase,TestVerboseNameMixin, TestMaxLengthMixin):
#     """Тесты для модели Trial"""
#
#     @classmethod
#     def setUpTestData(cls):
#         """Заносит данные в БД перед запуском тестов класса"""
#         user = User.objects.create(id=1)
#         category = CategoryCost.objects.create(id=1)
#         cls.cost = Cost.objects.create(
#             user=user,
#             category=category,
#             cost_date=datetime.datetime.now(),
#             cost_name='Еда',
#             cost_sum=100.00
#         )
#         cls.user = cls.cost._meta.get_field('user')
#         cls.category = cls.cost._meta.get_field('category')
#         cls.cost_date = cls.cost._meta.get_field('cost_date')
#         cls.cost_name = cls.cost._meta.get_field('cost_name')
#         cls.cost_sum = cls.cost._meta.get_field('cost_sum')
#         cls.field_and_verose_name={
#             'user': 'Пользователь',
#             'category': 'Категория',
#             'cost_date': 'День',
#             'cost_name': 'Назначение',
#             'cost_sum': 'Сумма'
#         }
#         cls.field_and_max_length = {
#             'cost_name': 1000,
#
#         }
#
#     def test_verbose_name(self):
#         super().run_verbose_name_test(Cost)
#
#     # def test_verbose_name_category(self):
#     #     real_verbose_name = getattr(self.category,'verbose_name')
#     #     expected_verbose_name = 'Категория'
#     #     self.assertEquals(real_verbose_name, expected_verbose_name)
#     #
#     # def test_verbose_name_cost_date(self):
#     #     real_verbose_name = getattr(self.cost_date,'verbose_name')
#     #     expected_verbose_name = 'День'
#     #     self.assertEquals(real_verbose_name, expected_verbose_name)
#     #
#     # def test_verbose_name_cost_name(self):
#     #     real_verbose_name = getattr(self.cost_name,'verbose_name')
#     #     expected_verbose_name = 'Назначение'
#     #     self.assertEquals(real_verbose_name, expected_verbose_name)
#     #
#     # def test_verbose_name_cost_sum(self):
#     #     real_verbose_name = getattr(self.cost_sum,'verbose_name')
#     #     expected_verbose_name = 'Сумма'
#     #     self.assertEquals(real_verbose_name, expected_verbose_name)
#
#     def test_max_length(self):
#         super().run_max_length_test(Cost)
#
#     def test_unique_user(self):
#         real_unigue_user = getattr(self.user,'unique')
#         self.assertFalse(real_unigue_user)
#
#     def test_str_method(self):
#         self.assertEqual(str(self.cost), f'{self.cost.cost_name}-{self.cost.cost_sum}')
#
#     def test_model_verbose_name(self):
#         self.assertEqual(Cost._meta.verbose_name,'Расход')
#
#     def test_model_verbose_name_plural(self):
#         self.assertEqual(Cost._meta.verbose_name_plural, 'Расходы')
#
#
# class DayCostTests(TestCase, TestVerboseNameMixin):
#
#
#     @classmethod
#     def setUpTestData(cls):
#         """Заносит данные в БД перед запуском тестов класса"""
#         user = User.objects.create(id=1)
#         cls.daycost = DayCost.objects.create(
#             user=user,
#             day_date=datetime.datetime.now(),
#         )
#         cls.daycost.costs.set([])
#         cls.user = cls.daycost._meta.get_field('user')
#         cls.cost_date = cls.daycost._meta.get_field('day_date')
#         cls.costs= cls.daycost._meta.get_field('costs')
#         cls.field_and_verose_name={
#             'user': 'Пользователь',
#             'day_date': 'День',
#             'costs': 'Расходы',
#         }
#     def test_verbose_name(self):
#         super().run_verbose_name_test(DayCost)
#
