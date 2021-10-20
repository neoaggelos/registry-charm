# registry

## Description

This charm deploys a single node Docker registry to Kubernetes.

Note that this is not a production-grade registry, but rather developed as an exercise to get familiar with the [Charmed Operator Framework](https://juju.is/docs/sdk).

## Usage

```
charmcraft build
juju deploy registry ./registry*.charm --resource registry-image=registry:2
```

The registry is exposed at port 5000 of the `registry` service.

## Relations

TODO.

## Tests

Run unit tests.

```bash
pip install tox
tox -e lint
tox -e test
tox -e opstest
```

To run integration tests, Charmcraft and Juju is required. Juju must have a controller bootstrap on a Kubernetes cloud.

```bash
./scripts/setup_charmcraft.sh
./scripts/setup_juju.sh
```

## OCI Images

- [Docker Registry](https://hub.docker.com/_/registry/)

## Contributing

Please see the [Juju SDK docs](https://juju.is/docs/sdk) for guidelines
on enhancements to this charm following best practice guidelines, and
`CONTRIBUTING.md` for developer guidance.
