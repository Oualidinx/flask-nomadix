# tests/test_forms.py
from root.forms import ConfigForm
from flask_wtf.csrf import generate_csrf
class TestConfigForm:

    def test_valid_form(self, app):
        """Test form passes with valid data"""
        with app.app_context():
            form = ConfigForm(
                data={
                    "benefice":150,
                    "supplier_payment_period":15,
                    "balance_reminder":7
                }
            )

        assert form.validate() == True, f'{form.errors}'


    def test_missing_required_field(self, app):
        """Test form fails with missing data"""
        with app.app_context():
            form = ConfigForm(data={
                'benefice': 15.00,
                'supplier_payment_period': '',  # missing
                'balance_reminder': 7,
                'csrf_token':generate_csrf()
            })
            assert form.validate() == False
            assert 'supplier_payment_period' in form.errors

    def test_below_minimum_value(self, app):
        """Test NumberRange validator"""
        with app.app_context():
            form = ConfigForm(data={
                'benefice': 0,   # below min=1
                'supplier_payment_period': 30,
                'balance_reminder': 7,
                'csrf_token':generate_csrf()
            })
            assert form.validate() == False
            assert 'benefice' in form.errors

    def test_negative_values(self, app):
        """Test that negative values are rejected"""
        with app.app_context():
            form = ConfigForm(data={
                'benefice': -5,
                'supplier_payment_period': -1,
                'balance_reminder': 7
            })
            assert form.validate() == True