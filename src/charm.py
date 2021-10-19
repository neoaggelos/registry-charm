#!/usr/bin/env python3
# Copyright 2021 Ubuntu
# See LICENSE file for licensing details.
#
# Learn more at: https://juju.is/docs/sdk

import logging

from ops.charm import CharmBase
from ops.framework import StoredState
from ops.main import main
from ops.model import ActiveStatus, WaitingStatus, MaintenanceStatus

from charms.observability_libs.v0.kubernetes_service_patch import KubernetesServicePatch
from charms.nginx_ingress_integrator.v0.ingress import IngressRequires

LOG = logging.getLogger(__name__)


class RegistryCharm(CharmBase):
    """Charm for Docker registry service."""

    _stored = StoredState()

    def service_hostname(self):
        return self.config["external-hostname"] or self.app.name

    def __init__(self, *args):
        super().__init__(*args)
        self.framework.observe(self.on.install, self._on_config_changed)
        self.framework.observe(self.on.config_changed, self._on_config_changed)
        self.framework.observe(self.on.registry_pebble_ready, self._on_config_changed)

        self.service_patcher = KubernetesServicePatch(self, [("http", 5000)])
        self.ingress = IngressRequires(
            self,
            {
                "service-hostname": self.service_hostname(),
                "service-name": self.app.name,
                "service-port": 80,
            },
        )

    def _on_config_changed(self, _):
        self.ingress.update_config({"service-hostname": self.service_hostname()})
        container = self.unit.get_container("registry")
        layer = {
            "summary": "registry layer",
            "description": "pebble config layer for registry",
            "services": {
                "registry": {
                    "override": "replace",
                    "summary": "registry",
                    "command": "registry serve /etc/docker/registry/config.yml",
                    "startup": "enabled",
                    "environment": {
                        "REGISTRY_HTTP_PREFIX": self.config["prefix"],
                    },
                },
            },
        }
        if container.can_connect():
            if container.get_plan().to_dict().get("services", {}) != layer["services"]:
                self.unit.status = MaintenanceStatus("Unit is updating")
                container.add_layer("registry", layer, combine=True)
                LOG.info("Added container layer to Pebble")
                container.restart("registry")
                LOG.info("Restarted")

            self.unit.status = ActiveStatus("Unit started")
        else:
            self.unit.status = WaitingStatus("Waiting for Pebble")


if __name__ == "__main__":
    main(RegistryCharm)
