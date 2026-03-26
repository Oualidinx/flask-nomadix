import unittest
import json

from app.modules.finance.controller import FinanceController


def test_index():
    finance_controller = FinanceController()
    result = finance_controller.index()
    assert result == {'message': 'Hello, World!'}
