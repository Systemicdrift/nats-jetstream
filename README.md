# Simple nats-jestream app

Simple app to demonstrate use of docker, uv and nat-jetstream

## Dependencies
[UV](https://docs.astral.sh/uv/)
[Python](https://www.python.org/)
[Docker](https://www.docker.com/)

### Install UV

[Install uv docs](https://docs.astral.sh/uv/getting-started/installation/#pypi)

`curl -LsSf https://astral.sh/uv/install.sh | sh`

or

`brew install uv`

### Install Python
`uv python install`

## Make commands
`make help`
```
Makefile commands:
  clean       - Remove virtual environment and pycache
  clean-build - Build new docker images
  relock      - Build new uv.lock file
  run         - Run project in docker
  setup       - Setup venv, install python deps from pyproject.toml
  test        - Run pytest tests
  test-int    - Run pytest integration tests
```

## To run in minikube

[Get minikube](https://minikube.sigs.k8s.io/docs/start/?arch=%2Fmacos%2Farm64%2Fstable%2Fbinary+download)

### Install minkube
```
curl -LO https://github.com/kubernetes/minikube/releases/latest/download/minikube-darwin-arm64
sudo install minikube-darwin-arm64 /usr/local/bin/minikube
```

### Run it
```
minikube start
minikube kubectl -- get po -A

kubectl config get-contexts
kubectl config use-context minikube
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl get pods
kubectl get svc
minikube dashboard

```