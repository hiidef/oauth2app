#-*- coding: utf-8 -*-

import json
from .base import *


class BearerTestCase(BaseTestCase):

    def test_00_bearer(self):
        client = DjangoTestClient()
        token = self.get_token()
        response = client.get(
            "/api/email_str", 
            {}, 
            HTTP_AUTHORIZATION="Bearer %s" % token)
        self.assertEqual(response.status_code, 200) 
        response = client.get(
            "/api/email_str", 
            {}, 
            HTTP_AUTHORIZATION="Bearer2 %s" % token)
        self.assertEqual(response.status_code, 401)
        response = client.get(
            "/api/email_str", 
            {}, 
            HTTP_AUTHORIZATION="Bearer !!!%s" % token)
        self.assertEqual(response.status_code, 401)

    def test_01_json_bearer(self):
        client = DjangoTestClient()
        token = self.get_token()
        response = client.get(
            "/api/email_json", 
            {}, 
            HTTP_AUTHORIZATION="Bearer %s" % token)
        self.assertEqual(response.status_code, 200) 
        self.assertTrue("email" in json.loads(response.content))
        response = client.get(
            "/api/email_json", 
            {}, 
            HTTP_AUTHORIZATION="Bearer2 %s" % token)
        self.assertEqual(response.status_code, 401)
        self.assertTrue("error" in json.loads(response.content))
        response = client.get(
            "/api/email_json", 
            {}, 
            HTTP_AUTHORIZATION="Bearer !!!%s" % token)
        self.assertEqual(response.status_code, 401)
        self.assertTrue("error" in json.loads(response.content))

    def test_02_automatic_fail(self):
        client = DjangoTestClient()
        token = self.get_token()
        response = client.get(
            "/api/automatic_error_str", 
            {}, 
            HTTP_AUTHORIZATION="Bearer %s" % token)
        self.assertEqual(response.status_code, 401)
        response = client.get(
            "/api/automatic_error_json", 
            {}, 
            HTTP_AUTHORIZATION="Bearer %s" % token)
        self.assertEqual(response.status_code, 401)
