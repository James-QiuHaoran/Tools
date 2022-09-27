# Kubernetes Development Guide

This guide tells you how to contribute to the Kubernetes project and be part of the open-source community.

Reference: https://github.com/kubernetes/community/tree/master/contributors/guide

## Prerequisite

Hardware requirements:
- 8GB of RAM
- 50GB of free disk space

Set up the development requirements: https://github.com/kubernetes/community/tree/master/contributors/guide

Install a series of prerequisites according to https://github.com/kubernetes/community/blob/master/contributors/devel/development.md:
- Basic tools on the OS: https://github.com/kubernetes/community/blob/master/contributors/devel/development.md#setting-up-macos
- Docker
- GNU development tools
- rsync
- jq
- gcloud
- Go
- PyYAML

### Cloning the Kubernetes Git Repository

Refer to the GitHub workflow: https://github.com/kubernetes/community/blob/master/contributors/guide/github-workflow.md
- Fork in the cloud
- Clone fork to local storage on `GOPATH`
- Create a working branch

### Install etcd

To test Kubernetes, you will need to install a recent version of etcd, a consistent and highly-available key-value store.
To install a local version of etcd, run the following command in your Kubernetes working directory.

```
./hack/install-etcd.sh
```

Add the following to your profile:

```
export PATH="$GOPATH/src/k8s.io/kubernetes/third_party/etcd:${PATH}"
```

## Building Kubernetes

The best way to validate your development environment is to build part of Kubernetes.
This allows you to address issues and correct your configuration without waiting for a full build to complete.

Reference: https://github.com/kubernetes/kubernetes/blob/master/build/README.md

To build a specific part of Kubernetes use the `WHAT` environment variable. In `$GOPATH/src/k8s.io/kubernetes/`, the Kubernetes project directory, run the following command:

```sh
make WHAT=cmd/<subsystem>
```

Replace `<subsystem>` with one of the command folders under the `cmd/` directory. For example, to build the `kubectl` CLI, run the following:

```sh
make WHAT=cmd/kubectl
```

If this command succeeds, you will now have an executable at `_output/bin/kubectl` off of your Kubernetes project directory.

To build the entire Kubernetes project, run the following command:

```sh
make all
```

**Note:** You can omit `all` and just run `make`.

The Kubernetes build system defaults to limiting the number of reported Go compiler errors to 10. If you would like to remove this limit, add `GOGCFLAGS="-e"` to your command line. For example:

```sh
make WHAT="cmd/kubectl" GOGCFLAGS="-e"
```

If you need to use debugging inspection tools on your compiled Kubernetes executables, add `-N -l` to `GOGCFLAGS`. For example:

```sh
make WHAT="cmd/kubectl" GOGCFLAGS="-N -l"
```

To cross-compile Kubernetes for all platforms, run the following command:

```sh
make cross
```

To build binaries for a specific platform, add `KUBE_BUILD_PLATFORMS=<os>/<arch>`. For example:

```sh
make cross KUBE_BUILD_PLATFORMS=windows/amd64
```

### Build Artifacts

The build system output all its products to a top level directory in the source repository named `_output`.
These include the binary compiled packages (e.g. `kubectl`, `kube-scheduler` etc.) and archived Docker images.
If you intend to run a component with a docker image you will need to import it from this directory with the appropriate command (e.g. `docker import _output/release-images/amd64/kube-scheduler.tar k8s.io/kube-scheduler:$(git describe)`).

## Testing

Because kubernetes only merges pull requests when unit, integration, and e2e tests are
passing, your development environment needs to run all tests successfully. While this quick start will get you going,
to really understand the testing infrastructure, read the
[Testing Guide](sig-testing/testing.md) and check out the
[SIG Architecture developer guide material](README.md#sig-testing).

Note that all of the commands in this section are run in your
Kubernetes project directory at `$GOPATH/src/k8s.io/kubernetes/`
unless otherwise specified.

**Note:** You can get additional information for many of the commands
mentioned here by running `make help`.

### Presubmission Verification

Presubmission verification provides a battery of checks and tests to
give your pull request the best chance of being accepted. Developers need to run as many verification tests as possible
locally. 

You can view a list of all verification tests in `hack/verify-*.sh`
off of your Kubernetes project directory.

To run all presubmission verification tests, use this command:

```sh
make verify
```

If a specific verification test is failing, there could be an update
script to help fix the problem. These are located in
`hack/update-*.sh`. For example, `hack/update-gofmt.sh` makes sure
that all source code files are correctly formatted. This is usually
needed when you add new files to the project.

You can also run all update scripts with this command:

```sh
make update
```

### Unit Tests

Pull requests need to pass all unit tests. To run every unit test, use
this command:

```sh
make test
```

You can also use the `WHAT` option to control which packages and
subsystems are testing and use `GOFLAGS` to change how tests are
run. For example, to run unit tests verbosely against just one
package, use a command like this:

```
make test WHAT=./pkg/apis/core/helper GOFLAGS=-v
```

### Integration Tests

All integration tests need to pass for a pull request to be
accepted. Note that for this stage, in particular, it is important that
[etcd](#etcd) be properly installed. Without it, integration testing
will fail.

To run integration tests, use this command:

```sh
make test-integration
```

To learn more about integration testing, read the
[SIG Testing Integration Tests guide](./sig-testing/integration-tests.md).

### E2E Tests

End-to-end (E2E) tests provide a mechanism to test the end-to-end behavior
of the system. The primary objective of the E2E tests is to ensure
consistent and reliable behavior of the Kubernetes code base,
especially in areas where unit and integration tests are insufficient.

E2E tests build test binaries, spin up a test cluster,
run the tests, and then tear the cluster down.

**Note:** Running all E2E tests takes a *very long time*!

For more information on E2E tests, including methods for saving time
by just running specific tests, read
[End-to-End Testing in Kubernetes](./sig-testing/e2e-tests.md) and the
[getting started guide for `kubetest2`](./sig-testing/e2e-tests-kubetest2.md).

## Dependency management

Kubernetes uses [go modules](https://github.com/golang/go/wiki/Modules) to manage
dependencies.

Developers who need to manage dependencies in the `vendor/` tree should read
the docs on [using go modules to manage dependencies](/contributors/devel/sig-architecture/vendor.md).
