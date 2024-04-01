#! /usr/bin/python3
import pprint
import tempfile
from bitrootlib.test import conftest  # this is require near the top to do setup of the test suite
from bitrootlib.test.fixtures.params import DEFAULT_PARAMS as DP
from bitrootlib.test import util_test
from bitrootlib.test.util_test import CURR_DIR

from bitrootlib.lib import (blocks, config, util)


FIXTURE_SQL_FILE = CURR_DIR + '/fixtures/scenarios/parseblock_unittest_fixture.sql'
FIXTURE_DB = tempfile.gettempdir() + '/fixtures.parseblock_unittest_fixture.db'


def test_config_context(cp_server):
    assert config.BTC_NAME == "Bitcoin"

    with util_test.ConfigContext(BTC_NAME="Bitcoin Testing"):
        assert config.BTC_NAME == "Bitcoin Testing"

        with util_test.ConfigContext(BTC_NAME="Bitcoin Testing Testing"):
            assert config.BTC_NAME == "Bitcoin Testing Testing"

        assert config.BTC_NAME == "Bitcoin Testing"

    assert config.BTC_NAME == "Bitcoin"


def test_mock_protocol_changes(cp_server):
    assert util.enabled('multisig_addresses') == True

    with util_test.MockProtocolChangesContext(multisig_addresses=False):
        assert util.enabled('multisig_addresses') == False

        with util_test.MockProtocolChangesContext(multisig_addresses=None):
                assert util.enabled('multisig_addresses') == None

        assert util.enabled('multisig_addresses') == False

    assert util.enabled('multisig_addresses') == True
