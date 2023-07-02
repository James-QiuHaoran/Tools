# code-generator

https://github.com/kubernetes/code-generator

Generator for kube-like APIs such as CRDs.

## Usage

### Multi-dimensional Pod Autoscaler

- Go path: /home/jamesqiu/go
- Project path: /home/jamesqiu/go/src/k8s.io/autoscaler/multidimensional-pod-autoscaler
- code-generator path: /home/jamesqiu/go/src/k8s.io/code-generator

It needs to be a Go project and `go.mod` file is required.
If there's no `go.mod` file, you can generate one by:

```
go mod init
go mod tidy
```

If the Go project uses `vendor/` then you probably need to run `go mod vendor` to make sure that the vendor folder is consistent with the `go.mod` file.

Code structure:

```
$ tree pkg/apis/autoscaling.k8s.io/v1alpha1/
pkg/apis/autoscaling.k8s.io/v1alpha1/
├── doc.go
├── register.go
└── types.go
```

Run the following to generate code:

```
../../code-generator/generate-groups.sh "all" "pkg/client" "k8s.io/autoscaler/multidimensional-pod-autoscaler/pkg/apis" "autoscaling.k8s.io:v1alpha1" -v 10
```

Generated code:

```
$ tree pkg/client/
pkg/client/
├── clientset
│   └── versioned
│       ├── clientset.go
│       ├── doc.go
│       ├── fake
│       │   ├── clientset_generated.go
│       │   ├── doc.go
│       │   └── register.go
│       ├── scheme
│       │   ├── doc.go
│       │   └── register.go
│       └── typed
│           └── autoscaling.k8s.io
│               └── v1alpha1
│                   ├── autoscaling.k8s.io_client.go
│                   ├── doc.go
│                   ├── fake
│                   │   ├── doc.go
│                   │   ├── fake_autoscaling.k8s.io_client.go
│                   │   └── fake_multidimpodautoscaler.go
│                   ├── generated_expansion.go
│                   └── multidimpodautoscaler.go
├── informers
│   └── externalversions
│       ├── autoscaling.k8s.io
│       │   ├── interface.go
│       │   └── v1alpha1
│       │       ├── interface.go
│       │       └── multidimpodautoscaler.go
│       ├── factory.go
│       ├── generic.go
│       └── internalinterfaces
│           └── factory_interfaces.go
└── listers
    └── autoscaling.k8s.io
        └── v1alpha1
            ├── expansion_generated.go
            └── multidimpodautoscaler.go
```

Note that the generated `pkg/client` directory path is relative to the `$GOPATH`.
