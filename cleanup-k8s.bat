@echo off
REM Script de nettoyage pour Windows

echo Nettoyage des ressources Kubernetes...

kubectl delete -f k8s/frontend.yaml
kubectl delete -f k8s/user-service.yaml
kubectl delete -f k8s/message-service.yaml
kubectl delete -f k8s/auth-service.yaml
kubectl delete -f k8s/configmap.yaml

echo Toutes les ressources ont ete supprimees!
kubectl get all
