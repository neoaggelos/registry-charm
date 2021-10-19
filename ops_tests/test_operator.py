import pytest
from pytest_operator.plugin import OpsTest


@pytest.mark.abort_on_fail
async def test_build_and_deploy(ops_test: OpsTest):
    charm = await ops_test.build_charm(".")
    await ops_test.model.deploy(charm, resources={"registry-image": "registry:2"})
    await ops_test.model.wait_for_idle()
