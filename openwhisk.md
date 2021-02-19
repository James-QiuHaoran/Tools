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

## OpenWhisk Install on Docker

https://github.com/apache/openwhisk/blob/master/tools/ubuntu-setup/README.md

Install all required software:

```
cd tools/ubuntu-setup && ./all.sh
```

Install CouchDB (on Ubuntu 18.04):
https://www.alibabacloud.com/blog/how-to-set-up-apache-openwhisk-on-ubuntu-18-04-part-ii_594685

```
# adding the CouchDB GPG key to the keyring
curl -L https://couchdb.apache.org/repo/bintray-pubkey.asc | sudo apt-key add -
# adding the repository to the sources
echo "deb https://apache.bintray.com/couchdb-deb bionic main" | sudo tee -a /etc/apt/sources.list

sudo apt update
sudo apt install -y couchdb
```

When a pop-up window shows, select "standalone" as the installation type and "0.0.0.0" for the binding IP.

After the installation, you can check the service status then:

```
sudo service couchdb status
```

One of the big features of CouchDB is the availability of REST API. If you run the following command, you should see all the information in a JSON format. This confirms that the API is up and running on the server.

```
$ curl http://0.0.0.0:5984
{"couchdb":"Welcome","version":"3.1.1","git_sha":"ce596c65d","uuid":"80f58ffcf3560af247974b2b4b87b48b","features":["access-ready","partitioned","pluggable-storage-engines","reshard","scheduler"],"vendor":{"name":"The Apache Software Foundation"}}
```

Adjust all parameters in `ansible/db_local.ini`.

Create the required data structures to prepare the account to be used for OpenWhisk:

```
cd ansible/
ansible-playbook initdb.yml
```

Export all DB parameters:

```
$ export OW_DB=CouchDB
$ export OW_DB_PROTOCOL=http
$ export OW_DB_HOST=127.0.0.1
$ export OW_DB_PORT=5984
$ export OW_DB_USERNAME=admin
$ export OW_DB_PASSWORD=password
```

Generate all the config files:

```
ansible-playbook setup.yml
```

Install the prerequsites on all the OpenWhisk nodes:

```
ansible-playbook prereq.yml # sudo required
```

Build and distribute the docker images using docker, make sure you move to the OpenWhisk root repository:

```
cd <home_openwhisk>
./gradlew distDocker
```

Wipe the database:

```
ansible-playbook wipe.yml
```

Deploy an OpenWhisk stack:

```
ansible-playbook openwhisk.yml

# installs a catalog of public packages and actions
ansible-playbook -i environments/$ENVIRONMENT postdeploy.yml

# to use the API gateway
ansible-playbook -i environments/$ENVIRONMENT apigateway.yml
ansible-playbook -i environments/$ENVIRONMENT routemgmt.yml
```
