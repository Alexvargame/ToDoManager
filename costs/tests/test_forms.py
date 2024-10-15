from django.test import TestCase

from costs.forms import CostForm

class CostFormTests(TestCase):
    """Тесты формы TrialForm"""

    def test_field_cost_name_labels(self):
        """Тест лейблов полей"""

        form = CostForm()
        cost_name_label = form.fields['cost_name'].label

        self.assertEqual(cost_name_label, 'Назначение')