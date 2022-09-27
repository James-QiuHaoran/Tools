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
