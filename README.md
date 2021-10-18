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

## OCI Images

- [Docker Registry](https://hub.docker.com/_/registry/)

## Contributing

Please see the [Juju SDK docs](https://juju.is/docs/sdk) for guidelines
on enhancements to this charm following best practice guidelines, and
`CONTRIBUTING.md` for developer guidance.
