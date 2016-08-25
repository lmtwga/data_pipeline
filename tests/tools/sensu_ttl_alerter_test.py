# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import mock
import pysensu_yelp
import pytest

from data_pipeline.tools.sensu_ttl_alerter import SensuTTLAlerter


class TestSensuTTLAlerter(object):

    @pytest.fixture
    def sensu_ttl_alerter(self):
        test_dict = {
            "name": "datapipeline_ttl_alerter_test",
            "output": "this is only a test of the datapipeline test alerter",
            "irc_channels": "#bam",
            "check_every": 60,
            "ttl": "300s",
            "runbook": "y/datapipeline",
            "status": 0,
            "team": "bam"
        }
        return SensuTTLAlerter(test_dict, enable=True)

    @pytest.yield_fixture
    def mocked_send_event(self, sensu_ttl_alerter):
        with mock.patch.object(
            pysensu_yelp,
            'send_event',
            autospec=True
        ) as mocked_send_event:
            yield mocked_send_event

    def test_send_event_while_enabled(self, sensu_ttl_alerter, mocked_send_event):
        sensu_ttl_alerter.process()
        assert mocked_send_event.call_count == 1

    def test_toggling_enable_to_false(self, sensu_ttl_alerter, mocked_send_event):
        sensu_ttl_alerter.enable = False
        assert mocked_send_event.call_count == 1
        assert 'ttl' not in mocked_send_event.call_args

    def test_no_send_event_while_disabled(self, sensu_ttl_alerter, mocked_send_event):
        # there's one call when we toggle from True to False
        sensu_ttl_alerter.enable = False
        assert mocked_send_event.call_count == 1
        # there should be no further calls
        sensu_ttl_alerter.process()
        assert mocked_send_event.call_count == 1
