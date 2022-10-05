# Programming in Go

## Installation of Go

https://go.dev/doc/install

## Code Organization

Go programs are organized into **packages**. A package is a collection of source files in the same directory that are compiled together.
Functions, types, variables, and constants defined in one source file are visible to all other source files within the same package.

A repository contains one or more **modules**. A module is a collection of related Go packages that are released together.
A Go repository typically contains only one module, located at the root of the repository.
A file named `go.mod` there declares the module **path**: the import path prefix for all packages within the module.
The module contains the packages in the directory containing its `go.mod` file as well as subdirectories of that directory, up to the next subdirectory containing another `go.mod` file (if any).

Each module's path not only serves as an import path prefix for its packages, but also indicates where the `go` command should look to download it.
For example, in order to download the module `golang.org/x/tools`, the `go` command would consult the repository indicated by https://golang.org/x/tools.

An import path is a string used to import a package. A package's import path is its module path joined with its subdirectory within the module.
For example, the module github.com/google/go-cmp contains a package in the directory `cmp/`. That package's import path is github.com/google/go-cmp/cmp.
Packages in the standard library do not have a module path prefix.

## First Program

https://go.dev/doc/code

## Go Tool

### Build and Install Go Programs

Build and install the program with the go module path `example/user/hello`:

```
$ go install example/user/hello

# build-only
$ go build
```

This command builds the `hello` command, producing an executable binary.
It then installs that binary as `$HOME/go/bin/hello` (or, under Windows, `%USERPROFILE%\go\bin\hello.exe`).

The install directory is controlled by the `GOPATH` and `GOBIN` environment variables.
- If `GOBIN` is set, binaries are installed to that directory.
- If `GOPATH` is set, binaries are installed to the `bin` subdirectory of the first directory in the `GOPATH` list.
- Otherwise, binaries are installed to the bin subdirectory of the default `GOPATH` (`$HOME/go` or `%USERPROFILE%\go`).

For convenience, `go` commands accept paths relative to the working directory, and default to the package in the current working directory if no other path is given.
So in our working directory, the following commands are all equivalent:

```
$ go install example/user/hello
$ go install .
$ go install
```

### Set and Unset Environment Variables

```
$ go env -w GOBIN=/somewhere/else/bin
$ go env -u GOBIN
```

### Import Remote Packages

```
package main

import (
    "fmt"

    "example/user/hello/morestrings"
    "github.com/google/go-cmp/cmp"
)

func main() {
    fmt.Println(morestrings.ReverseRunes("!oG ,olleH"))
    fmt.Println(cmp.Diff("Hello World", "Hello Go"))
}
```

Now that you have a dependency on an external module, you need to download that module and record its version in your `go.mod` file. The `go mod tidy` command adds missing module requirements for imported packages and removes requirements on modules that aren't used anymore.

### Vendoring
When using modules, the go command typically satisfies dependencies by downloading modules from their sources into the module cache, then loading packages from those downloaded copies. Vendoring may be used to allow interoperation with older versions of Go, or to ensure that all files used for a build are stored in a single file tree.

The `go mod vendor` command constructs a directory named vendor in the main module’s root directory containing copies of all packages needed to build and test packages in the main module. Packages that are only imported by tests of packages outside the main module are not included. As with `go mod tidy` and other module commands, build constraints except for ignore are not considered when constructing the vendor directory.

`go mod vendor` also creates the file `vendor/modules.txt` that contains a list of vendored packages and the module versions they were copied from. When vendoring is enabled, this manifest is used as a source of module version information, as reported by `go list -m` and `go version -m`. When the `go` command reads `vendor/modules.txt`, it checks that the module versions are consistent with `go.mod`. If `go.mod` has changed since `vendor/modules.txt` was generated, the go command will report an error. `go mod vendor` should be **run again** to update the vendor directory.

If the vendor directory is present in the main module’s root directory, it will be used automatically if the go version in the main module’s `go.mod` file is 1.14 or higher. To explicitly enable vendoring, invoke the go command with the flag `-mod=vendor`. To disable vendoring, use the flag `-mod=readonly` or `-mod=mod`.

When vendoring is enabled, build commands like `go build` and `go test` load packages from the vendor directory instead of accessing the network or the local module cache. The `go list -m` command only prints information about modules listed in `go.mod`. `go mod` commands such as `go mod download` and `go mod tidy` do not work differently when vendoring is enabled and will still download modules and access the module cache. `go get` also does not work differently when vendoring is enabled.
