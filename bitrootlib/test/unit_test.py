#! /usr/bin/python3
import tempfile
import pytest
from bitrootlib.test import conftest  # this is require near the top to do setup of the test suite
from bitrootlib.test import util_test
from bitrootlib.test.util_test import CURR_DIR
from bitrootlib.lib import config

FIXTURE_SQL_FILE = CURR_DIR + '/fixtures/scenarios/unittest_fixture.sql'
FIXTURE_DB = tempfile.gettempdir() + '/fixtures.unittest_fixture.db'

@conftest.add_fn_property(DISABLE_ARC4_MOCKING=True)
@pytest.mark.usefixtures("api_server")
def test_vector(tx_name, method, inputs, outputs, error, records, comment, mock_protocol_changes, config_context, server_db):
    """Test the outputs of unit test vector. If testing parse, execute the transaction data on test db."""

    # disable arc4 mocking for vectors because we're too lazy to update all the vectors
    config_context.update({'DISABLE_ARC4_MOCKING': True})

    with util_test.ConfigContext(**config_context):
        # force unit tests to always run against latest protocol changes
        from bitrootlib.test import conftest
        conftest.ALWAYS_LATEST_PROTOCOL_CHANGES = True
        conftest.RANDOM_ASSET_INT = 26**12 + 1

        if method == 'parse':
            util_test.insert_transaction(inputs[0], server_db)
            # insert message as 2nd arg
            inputs = inputs[:1] + (inputs[0]['data'][4:],) + inputs[1:]
        util_test.check_outputs(tx_name, method, inputs, outputs, error, records, comment, mock_protocol_changes, server_db)
