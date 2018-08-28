Envoy Step By Step
==================

This is a simple example of how one can use Envoy to create scalable Flask apps.

The Tools
---------

Tools we'll be using:

1. [minikube](https://github.com/kubernetes/minikube)
2. [envoy](https://lyft.github.io/envoy/)


To prep everything for Minikube, run


bash prep.sh -


Should you want to clean everything up when done, use


bash clean.sh



bash up.sh postgres
bash up.sh usersvc


and then you should be able to check things out:


curl $(minikube service --url usersvc)/user/health

curl $(minikube service --url edge-envoy)/user/health
curl $(minikube service --url edge-envoy)/user/alice
bash up.sh usersvc-sds
bash up.sh edge-envoy2
