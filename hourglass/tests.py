import unittest
import json

from .settings_utils import load_cups_from_vcap_services


class CupsTests(unittest.TestCase):
    @staticmethod
    def make_vcap_services_env(vcap_services):
        return {
            'VCAP_SERVICES': json.dumps(vcap_services)
        }

    def test_noop_if_vcap_services_not_in_env(self):
        env = {}
        load_cups_from_vcap_services('blah', env=env)
        self.assertEqual(env, {})

    def test_irrelevant_cups_are_ignored(self):
        env = self.make_vcap_services_env({
          "user-provided": [
            {
              "label": "user-provided",
              "name": "NOT-boop-env",
              "syslog_drain_url": "",
              "credentials": {
                "boop": "jones"
              },
              "tags": []
            }
          ]
        })

        load_cups_from_vcap_services('boop-env', env=env)

        self.assertFalse('boop' in env)

    def test_credentials_are_loaded(self):
        env = self.make_vcap_services_env({
          "user-provided": [
            {
              "label": "user-provided",
              "name": "boop-env",
              "syslog_drain_url": "",
              "credentials": {
                "boop": "jones"
              },
              "tags": []
            }
          ]
        })

        load_cups_from_vcap_services('boop-env', env=env)

        self.assertEqual(env['boop'], 'jones')
