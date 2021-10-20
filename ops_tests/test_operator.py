import json
from urllib.request import urlopen

import pytest
from pytest_operator.plugin import OpsTest


@pytest.mark.abort_on_fail
async def test_build_and_deploy(ops_test: OpsTest):
    charm = await ops_test.build_charm(".")
    await ops_test.model.deploy(charm, resources={"registry-image": "registry:2"})
    await ops_test.model.wait_for_idle()


async def test_using_charm(ops_test: OpsTest):
    status = await ops_test.model.get_status()

    address = status.applications["registry"].public_address
    req = urlopen("http://{}:5000/v2/_catalog".format(address))

    assert req.code == 200
    assert json.loads(req.read()) == {"repositories": []}
