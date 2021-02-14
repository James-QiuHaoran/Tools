# OpenWhisk

GitHub Link: https://github.com/apache/openwhisk

## Introduction

OpenWhisk is a serverless functions platform for building cloud applications. OpenWhisk offers a rich programming model for creating serverless APIs from functions, composing functions into serverless workflows, and connecting events to functions using rules and triggers.

## OpenWhisk CLI

GitHub Link: https://github.com/apache/openwhisk-cli
Doc: https://github.com/apache/openwhisk/blob/master/docs/cli.md

OpenWhisk Command-line Interface (CLI) is a unified tool that provides a consistent interface to interact with OpenWhisk services.

To build, execute:

```
$ ./gradlew compile -PnativeCompile
```

After the build, you can find the binary `wsk` in the `build` folder under the OpenWhisk CLI home directory. In addition, it is also available under the folder `build/<os>-<architecture>/`. For example, if your local operating system is Mac, and the CPU architecture is amd64, the binary can be found at `build/mac-amd64/wsk` and `build/mac`.

When you have the binary, you can copy the binary to any folder, and add folder into the system `PATH` in order to run the OpenWhisk CLI command.
To get the CLI command help, execute the following command:

```
$ wsk --help
```

There are two required properties to configure in order to use the CLI:
- API host (name or IP address) for the OpenWhisk deployment you want to use.
- Authorization key (username and password) which grants you access to the OpenWhisk API.

## OpenWhisk Quick Start

```
$ ./gradlew core:standalone:bootRun
```

When the OpenWhisk stack is up, it will open your browser to a functions Playground, typically served from http://localhost:3232. The Playground allows you create and run functions directly from your browser.

To make use of all OpenWhisk features, you will need the OpenWhisk command line tool called wsk which you can download from https://s.apache.org/openwhisk-cli-download. Please refer to the CLI configuration for additional details. Typically you configure the CLI for **Standalone OpenWhisk** as follows:

```
$ wsk property set --apihost 'http://172.17.0.1:3233' --auth '23bc46b1-71f6-4ed5-8c54-816aa4f8c502:123zO3xZCLrMN6v2BKK1dXYFpXlPkccOFqm12CdAsMgRU4VrNZ9lyGVCGuMDGIwP'
```
