#-*- coding: utf-8 -*-

import json
from .base import *

class JSONTestCase(BaseTestCase):
    
    def test_00_email(self):
        client = DjangoTestClient()
        token = self.get_token()
        # Sufficient scope.
        response = client.get(
            "/api/email_json", 
            {}, 
            HTTP_AUTHORIZATION="Bearer %s" % token)
        self.assertEqual(response.status_code, 200) 
        self.assertEqual(json.loads(response.content)["email"], USER_EMAIL)
        response = client.get(
            "/api/email_json?callback=foo", 
            {}, 
            HTTP_AUTHORIZATION="Bearer %s" % token)
        self.assertEqual(response.status_code, 200) 
        # Remove the JSON callback.
        content = response.content.replace("foo(", "").replace(");", "")
        self.assertEqual(json.loads(content)["email"], USER_EMAIL)
        response = client.get(
            "/api/email_json?callback=foo", 
            {}, 
            HTTP_AUTHORIZATION="Bearer !!!%s" % token)
        content = response.content.replace("foo(", "").replace(");", "")
        self.assertEqual(response.status_code, 200) 
        self.assertTrue("error" in json.loads(content))
