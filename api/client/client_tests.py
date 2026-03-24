import unittest
import json

from app.modules.client.controller import ClientController


def test_index():
    client_controller = ClientController()
    result = client_controller.index()
    assert result == {'message': 'Hello, World!'}
