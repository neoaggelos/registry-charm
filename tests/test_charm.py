# Copyright 2021 Ubuntu
# See LICENSE file for licensing details.
#
# Learn more about testing at: https://juju.is/docs/sdk/testing

import unittest
from unittest.mock import MagicMock, patch

from charm import RegistryCharm
from ops.model import ActiveStatus, WaitingStatus
from ops.testing import Harness


class TestCharm(unittest.TestCase):
    @patch("charm.KubernetesServicePatch", lambda _, __: None)
    def setUp(self):
        self.harness = Harness(RegistryCharm)
        self.addCleanup(self.harness.cleanup)
        self.harness.begin()

    def test_registry(self):
        # Check the initial Pebble plan is empty
        initial_plan = self.harness.get_container_pebble_plan("registry")
        self.assertEqual(initial_plan.to_dict(), {})
        # Expected plan after Pebble ready with default config

        self.harness.charm.on.config_changed.emit()
        updated_plan = self.harness.get_container_pebble_plan("registry").to_dict()
        # Check we've got the plan we expected
        self.assertEqual(
            updated_plan,
            {
                "services": {
                    "registry": {
                        "override": "replace",
                        "summary": "registry",
                        "command": "registry serve /etc/docker/registry/config.yml",
                        "startup": "enabled",
                        "environment": {"REGISTRY_HTTP_PREFIX": ""},
                    }
                },
            },
        )
        # Check the service was started
        service = self.harness.model.unit.get_container("registry").get_service(
            "registry"
        )
        self.assertTrue(service.is_running())
        # Ensure we set an ActiveStatus
        self.assertEqual(self.harness.model.unit.status, ActiveStatus("Unit started"))

        # Ensure that service is not restarted when no config has changed
        container_start = "ops.model.Container.start"
        container_stop = "ops.model.Container.stop"
        with patch(container_start) as _start, patch(container_stop) as _stop:
            self.harness.charm.on.config_changed.emit()
            _start.assert_not_called()
            _stop.assert_not_called()

    def test_prefix_config(self):
        self.harness.update_config({"prefix": "/prefix/"})
        plan = self.harness.get_container_pebble_plan("registry").to_dict()
        self.assertEqual(
            plan["services"]["registry"]["environment"]["REGISTRY_HTTP_PREFIX"],
            "/prefix/",
        )

    def test_hostname_config(self):
        self.harness.charm.ingress = MagicMock()
        self.harness.update_config({"external-hostname": "my-registry"})
        self.harness.charm.ingress.update_config.assert_called_once_with(
            {"service-hostname": "my-registry"}
        )

    def test_empty_hostname_config(self):
        self.harness.charm.ingress = MagicMock()
        self.harness.update_config({"external-hostname": ""})
        self.harness.charm.ingress.update_config.assert_called_once_with(
            {"service-hostname": self.harness.charm.app.name}
        )

    def test_container_not_read(self):
        with patch("ops.model.Container.can_connect") as can_connect:
            can_connect.return_value = False
            self.harness.charm.on.config_changed.emit()
            self.assertEqual(
                self.harness.model.unit.status, WaitingStatus("Waiting for Pebble")
            )
