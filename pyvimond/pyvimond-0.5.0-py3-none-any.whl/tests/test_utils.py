import unittest
import pyvimond.utils as utils


class UtilsTest(unittest.TestCase):

    def test_create_http_client(self):
        self.assertIsNotNone(utils.create_http_client())

    def test_create_api_metadata(self):
        metadata = {
            'foo': True,
            'bar': 'very bar',
            'baz': 42
        }

        self.assertEqual({
            'entries': {
                'foo': [{'value': True, 'lang': '*'}],
                'bar': [{'value': 'very bar', 'lang': '*'}],
                'baz': [{'value': 42, 'lang': '*'}],
            },
            'empty': True
        }, utils.create_api_metadata(metadata))

    def test_parse_metadata(self):
        asset = {
            # Normally there are other fields here, but here we only need "metadata"
            'metadata': {
                'entries': {
                    'foo': [{'value': True, 'lang': '*'}],
                    'bar': [{'value': 'very bar', 'lang': '*'}],
                    'baz': [{'value': 42, 'lang': '*'}],
                },
                'empty': True
            }
        }

        self.assertEqual({
            'foo': True,
            'bar': 'very bar',
            'baz': 42
        }, utils.parse_metadata(asset))

    def test_get_metadata_value(self):
        asset = {
            # Normally there are other fields here, but here we only need "metadata"
            'metadata': {
                'entries': {
                    'foo': [{'value': True, 'lang': '*'}],
                    'bar': [{'value': 'very bar', 'lang': '*'}],
                    'baz': [{'value': 42, 'lang': '*'}],
                    # Metadata entries can inexplicably exist without values
                    'hurr': [{'lang': '*'}]
                },
                'empty': True
            }
        }

        self.assertTrue(utils.get_metadata_value('foo', asset))
        self.assertEqual('very bar', utils.get_metadata_value('bar', asset))
        self.assertEqual(42, utils.get_metadata_value('baz', asset))
        self.assertEqual(None, utils.get_metadata_value('hurr', asset))
        self.assertEqual(None, utils.get_metadata_value('ei ole', asset))

    def test_parse_category_metadata(self):
        category = {
            'metadata': {
                '@uri': '/api/metadata/category/123',
                'foo': {
                    '@xml:lang': '*',
                    '$': 'Category Foo',
                },
                'bar': {
                    '@xml:lang': '*',
                    '$': 'Category Bar',
                }
            }
        }

        self.assertEqual({
            'foo': 'Category Foo',
            'bar': 'Category Bar',
        }, utils.parse_category_metadata(category))

    def test_get_category_metadata_value(self):
        # get_category() uses this slightly unexpected format
        category = {
            'category': {
                'metadata': {
                    '@uri': '/api/metadata/category/123',
                    'string': {
                        '@xml:lang': '*',
                        '$': 'some string',
                    },
                    'int': {
                        '@xml:lang': '*',
                        '$': '42',
                    },
                    'bool': {
                        '@xml:lang': '*',
                        '$': 'false',
                    }
                }
            }
        }

        # Make sure no automatic type coercion is going on
        self.assertEqual('some string', utils.get_category_metadata_value('string', category['category']))
        self.assertEqual('42', utils.get_category_metadata_value('int', category['category']))
        self.assertEqual('false', utils.get_category_metadata_value('bool', category['category']))
        self.assertEqual(None, utils.get_category_metadata_value('baz', category['category']))

    def test_create_sumo_signature(self):
        method = 'GET'
        path = '/api/web/asset/1334686?expand=metadata&showHiddenMetadata=true'
        secret = 'secret'
        timestamp = 'Wed, 09 Dec 2020 09:48:44 +0200'

        self.assertEqual('Xm2Kr+xdb4uEp3F7COA+oj8EOpg=', utils.create_sumo_signature(method, path, secret, timestamp))

    def test_create_basic_auth_token(self):
        token = utils.create_basic_auth_token("username", "password")

        self.assertEqual('dXNlcm5hbWU6cGFzc3dvcmQ=', token)

    def test_create_update_asset_payload_skeleton(self):
        # Check that "id" is required, Vimond gives misleading errors if it's missing
        with self.assertRaises(ValueError):
            utils.create_update_asset_payload({})

        # Test with missing values
        self.assertEqual({
            'id': 123,
            'live': False,
            'archive': False,
        }, utils.create_update_asset_payload({
            'id': 123,
        }))

        # Test with values
        self.assertEqual({
            'id': 456,
            'live': True,
            'archive': True,
        }, utils.create_update_asset_payload({
            'id': 456,
            'live': True,
            'archive': True,
        }))

        # Test with payload
        self.assertEqual({
            'id': 789,
            'live': False,
            'archive': True,
            'categoryId': 123456,
        }, utils.create_update_asset_payload({
            'id': 789,
            'live': False,
            'archive': True,
        }, {
            'categoryId': 123456
        }))

    def test_get_platform_publishing_info(self):
        asset = {
            'id': 123,
            'platformPublishInfo': [
                {
                    "id": 8712972,
                    "platformId": 1,
                    "assetId": 1685213,
                    "platformName": "web",
                    "livePublished": False,
                    "onDemandPublished": True,
                    "downloadable": False,
                    "expire": "2022-11-14T05:12:00Z"
                },
                {
                    "id": 8712973,
                    "platformId": 2,
                    "assetId": 1685213,
                    "platformName": "mobile",
                    "livePublished": False,
                    "onDemandPublished": True,
                    "downloadable": False,
                    "expire": "2022-11-14T05:12:00Z"
                },
                {
                    "id": 8712974,
                    "platformId": 3,
                    "assetId": 1685213,
                    "platformName": "iptv",
                    "livePublished": False,
                    "onDemandPublished": True,
                    "downloadable": False,
                    "expire": "2022-11-14T05:12:00Z"
                },
                {
                    "id": 8712975,
                    "platformId": 4,
                    "assetId": 1685213,
                    "platformName": "mce",
                    "livePublished": False,
                    "onDemandPublished": True,
                    "downloadable": False,
                    "expire": "2022-11-14T05:12:00Z"
                },
                {
                    "id": 8712976,
                    "platformId": 5,
                    "assetId": 1685213,
                    "platformName": "sctv",
                    "livePublished": False,
                    "onDemandPublished": True,
                    "downloadable": False,
                    "expire": "2022-11-14T05:12:00Z"
                },
                {
                    "id": 8712977,
                    "platformId": 6,
                    "assetId": 1685213,
                    "platformName": "mobileapp",
                    "livePublished": False,
                    "onDemandPublished": True,
                    "downloadable": False,
                    "expire": "2022-11-14T05:12:00Z"
                }
            ]
        }

        self.assertEqual({
            'assetId': 1685213,
            'downloadable': False,
            'expire': '2022-11-14T05:12:00Z',
            'id': 8712972,
            'livePublished': False,
            'onDemandPublished': True,
            'platformId': 1,
            'platformName': 'web'
        }, utils.get_platform_publishing_info(asset, 'web'))

        self.assertEqual({
            'assetId': 1685213,
            'downloadable': False,
            'expire': '2022-11-14T05:12:00Z',
            'id': 8712977,
            'livePublished': False,
            'onDemandPublished': True,
            'platformId': 6,
            'platformName': 'mobileapp'
        }, utils.get_platform_publishing_info(asset, 'mobileapp'))

        self.assertIsNone(utils.get_platform_publishing_info(asset, 'unknown platform'))


if __name__ == '__main__':
    unittest.main()
