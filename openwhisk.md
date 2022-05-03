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

## Install/Deploy OpenWhisk on Docker (Single Node)

https://github.com/apache/openwhisk/blob/master/tools/ubuntu-setup/README.md

Install all required software:

```
cd tools/ubuntu-setup && ./all.sh
```

Install CouchDB (on Ubuntu **20.04**):
https://www.alibabacloud.com/blog/how-to-set-up-apache-openwhisk-on-ubuntu-18-04-part-ii_594685

```
# adding the CouchDB GPG key to the keyring
curl -L https://couchdb.apache.org/repo/keys.asc | sudo apt-key add -
# adding the repository to the sources
echo "deb https://apache.jfrog.io/artifactory/couchdb-deb focal main" | sudo tee -a /etc/apt/sources.list

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

You can also access CouchDB GUI at `http://localhost:5984/_utils` and use the credentials you set to login.

Export all DB parameters:

```
$ export OW_DB=CouchDB
$ export OW_DB_PROTOCOL=http
$ export OW_DB_HOST=127.0.0.1
$ export OW_DB_PORT=5984
$ export OW_DB_USERNAME=admin
$ export OW_DB_PASSWORD=password
```

**Or you can deploy a CouchDB container on Docker (Preferred for MacOS) and change the `OW_DB_HOST` from `127.0.0.1` to `172.17.0.1`, `OW_DB_PASSWORD` to `admin`:**

```
ansible-playbook couchdb.yml
```

Build and distribute the docker images using docker, make sure you move to the OpenWhisk root repository:

```
cd <home_openwhisk>
./gradlew distDocker
```

Generate all the config files:

```
cd ansible/
ansible-playbook -i environments/$ENVIRONMENT setup.yml
```

Enable Docker remote API
The remote Docker API is required for collecting logs using the Ansible playbook `logs.yml`.

Activate docker0 network
This is an optional step for local deployment. The OpenWhisk deployment via Ansible uses the docker0 network interface to deploy OpenWhisk and it does not exist on Docker for Mac environment.

An expedient workaround is to add alias for docker0 network to loopback interface.

```
sudo ifconfig lo0 alias 172.17.0.1/24
```

Install the prerequsites on all the OpenWhisk nodes:

```
ansible-playbook -i environments/$ENVIRONMENT prereq.yml # sudo required
```

Adjust all parameters in `ansible/db_local.ini` (should be consistent with the parameters exported).

Create the required data structures to prepare the account to be used for OpenWhisk:

```
ansible-playbook -i environments/$ENVIRONMENT initdb.yml
```

Wipe the database:

```
ansible-playbook -i environments/$ENVIRONMENT wipe.yml
```

Deploy an OpenWhisk stack:

```
ansible-playbook -i environments/$ENVIRONMENT openwhisk.yml

# installs a catalog of public packages and actions (before that, make sure the `ansible/files/runtimes.json` is not modified)
ansible-playbook -i environments/$ENVIRONMENT postdeploy.yml

# to use the API gateway
ansible-playbook -i environments/$ENVIRONMENT apigateway.yml
ansible-playbook -i environments/$ENVIRONMENT routemgmt.yml
```

Test if it's working:

```
$ wsk action invoke /whisk.system/utils/echo -p message hello --result
{
    "message": "hello"
}
```

## Usage

See the list of successfully built OpenWhisk actions:

```
wsk action list -i
```

Create an action:

```
wsk action create myAction action.js

# to specify the memory limit for the action, e.g., 128MB
wsk action create myAction action.js -m 128
```

Invoke an action:

```
wsk action invoke myAction --result

# if there's a parameter to pass
wsk action invoke myAction --result --param param_name param_value
# or use parameter file
wsk action invoke myAction --result --param-file file_name
```

Create an action from customized container (for accessing files or libraries that are larger than 48MB):

```
# create a Dockerfile
FROM openwhisk/python3action:latest

RUN apk add --update py-pip
RUN pip install numpy
ADD file_name /file_name

# build the docker image
docker build -t haoranq4/image-name:ml-libs .
docker push haoranq4/image-name:ml-libs

# create a new action with the following source code and name it action.py:
import numpy

def main(params):
    return {
        "numpy": numpy.__version__
    }

wsk action create ml-libs --docker haoranq4/image-name:ml-libs action.py
wsk action invoke ml-libs --result
```

Refer to https://github.com/apache/openwhisk/blob/master/docs/actions-docker.md and https://github.com/apache/openwhisk-runtime-python/tree/master/core/python3Action for more information.

## Install Distributed OpenWhisk on Multiple Nodes

https://github.com/apache/openwhisk/blob/053bd9aefe75033d1e6c09e341d34c4e116bf7d4/ansible/README_DISTRIBUTED.md
https://github.com/i13tum/openwhisk-bench/blob/master/README_Openwhisk.md

### Prepare All Physical Nodes or VMs (Install all dependencies including Ansible, Gradle, Java, and Scala)

On each machine, enable SSH access with the `root` user:

```
sudo passwd root
sudo su
cp /home/$USERNAME/.ssh/authorized_keys /root/.ssh/
```

Enable passwordless SSH login from the master (Ansible server) to all invokers, i.e., generate SSH keys for the `root` user and put the public key in the `authorized_keys` of each other machine.

Define `remote_user = root` in the `ansible/ansible.cfg`.

List the host machine IPs in the `ansible/environments/distributed/hosts`. The `environments/distributed` directory can be extended from the `environments/local` directory. You can simply change the IP address of the local server to be the IP address of any remote server. You can add `invoker1`, `invoker2`, ..., `invokerN` with the IP addresses of the remote servers. Don't forget to change `ansible_connection=local` to `ansible_connection=ssh` for remote servers.

Ensure that the Ansible server can authenticate to the remote servers via SSH using the following command:

```
cd ansible
ansible all -i environments/distributed -m ping
```

### Install Prerequisites on All Nodes

Generate config files

```
ansible-playbook -i environments/distributed setup.yml
```

Install prerequisites on OpenWhisk nodes.

```
ansible-playbook -i environments/distributed prereq.yml
```

### Build and Deploy OpenWhisk

Build images on each machine:

```
cd ..
./gradlew distDocker
```

Setup Openwhisk with `ansible-playbook`:

```
cd ansible
ansible-playbook -i environments/distributed couchdb.yml
ansible-playbook -i environments/distributed initdb.yml
ansible-playbook -i environments/distributed wipe.yml
ansible-playbook -i environments/distributed openwhisk.yml

# installs a catalog of public packages and actions
ansible-playbook -i environments/distributed postdeploy.yml

# to use the API gateway
ansible-playbook -i environments/distributed apigateway.yml
ansible-playbook -i environments/distributed routemgmt.yml
```

### Verification

Check all Docker containers are up and running: `docker ps`

Set the API host and the auth:

```
../bin/wsk property set --auth $(cat files/auth.whisk.system) --apihost <master_url>
../bin/wsk property get -i
```

Test to see if it's working:

```
$ ../bin/wsk -i -v action invoke /whisk.system/samples/helloWorld --blocking --result
{}
```

```
$ ../bin/wsk -i action invoke /whisk.system/utils/echo -p message hello --result
{
    "message": "hello"
}
```

## Using OpenWhisk Provided-Tools

Directory: `openwhisk/tools/build`

Tear down all invokers:

```
# local environment (default)
sudo ./redo invoker -x

# distributed environment
sudo ./redo invoker -x -t distributed
```

Build and deploy all invokers:

```
# local environment (default)
sudo ./redo invoker -bd

# distributed environment
sudo ./redo invoker -bd -t distributed
```

Rebuild and Redeploy the controller:

```
sudo ./redo controller -xbd
sudo ./redo controller -xbd -t distributed
```

## Contributing to OpenWhisk

https://medium.com/openwhisk/how-to-contribute-to-openwhisk-6164c54134a6

Redeploy/rebuild after changing the codebase: https://github.com/apache/openwhisk/tree/master/tools/build

## Uninstall OpenWhisk Deployment

Cleaning a Single Component
You can remove a single component just as you would remove the entire deployment stack. For example, if you wanted to remove only the controller you would run:

```
cd ansible
ansible-playbook -i environments/$ENVIRONMENT controller.yml -e mode=clean
```

Caveat: In distributed environments some components (e.g. Invoker, etc.) exist on multiple machines. So if you run a playbook to clean or deploy those components, it will run on all of the hosts targeted by the component's playbook.

Cleaning an OpenWhisk Deployment
Once you are done with the deployment you can clean it from the target environment.

```
ansible-playbook -i environments/$ENVIRONMENT openwhisk.yml -e mode=clean
ansible-playbook -i environments/$ENVIRONMENT apigateway.yml -e mode=clean
```

Check the logs from the controller or invoker container:

```
docker exec -it container_name/id /bin/bash
```

## Other OpenWhisk Tools

### Runtime Configurations

File: `openwhisk/ansible/files/runtimes.json`

## FaaSProfiler

https://github.com/PrincetonUniversity/faas-profiler

FaaSProfiler is a tool for testing and profiling FaaS platforms. Several features:

- Arbitrary mix of functions and invocation patterns. FaaSProfiler enables the description of various invocation patterns, function mixes, and activity windows in a clean, user-friendly format.
- FaaS-testing not plug-and-play. Each function should be invoked independently at the right time. Precisely invoking hundreds or thousands of functions per second needs a reliable, automated tool. We achieve this with FaaSProfiler.
- Large amount of performance and profiling data. FaaSProfiler enables fast analysis of performance profiling data (e.g., latency, execution time, wait time, etc.) together with resource profiling data (e.g. L1-D MPKI, LLC misses, block I/O, etc.). The user can specify which parameters to profile and make use of the rich feature sets of open-source data analysis libraries like Python pandas

Reference: Mohammad Shahrad, Jonathan Balkind, and David Wentzlaff. "Architectural Implications of Function-as-a-Service Computing." 2019 52nd Annual IEEE/ACM International Symposium on Microarchitecture (MICRO 52), October 2019.
http://parallel.princeton.edu/papers/micro19-shahrad.pdf

### Set Up

**Important Note**: Some of the default OpenWhisk configuration limits might be too restrictive for your setup. Do not forget to configure those parameters (particularly these: `invocationsPerMinute`, `concurrentInvocations`, `firesPerMinute`, and `sequenceMaxLength`) located at `openwhisk/ansible/group_vars/all`.

Clone the repository and do the one-time configuration:

```
bash configure.sh
```

### Usage

```
./WorkloadInvoker -c example_test.json
./WorkloadAnalyzer -rv -p
```

- `-v` for `--verbose`: prints the detailed test data
- `-r` for `--read_results`: gather also the results of function invocations
- `-p` for `--plot`: plots the test results 

## Set Up OpenWhisk Development Environment

https://medium.com/openwhisk/how-to-contribute-to-openwhisk-6164c54134a6

1. Fork the repository and clone to local workstation.

2. Install Java and Scala
- The backbone of OpenWhisk is developed in Scala. All the test cases are written in Scala. OpenWhisk also uses Java libraries as dependences.

3. Install Gradle
- Gradle is used as the build tool to modulize every major openwhisk projects.

4. Install Go
- The CLI of OpenWhisk is written in Go language. If the CLI is what you are interested, you need to install Go as well.

5. Install npm

6. Import the project to IntelliJ

7. Make the changes and redeploy/rebuild: https://github.com/apache/openwhisk/tree/master/tools/build
