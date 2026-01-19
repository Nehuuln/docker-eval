@echo off
REM Script complet de déploiement avec Minikube

echo ========================================
echo DEPLOIEMENT COMPLET SUR MINIKUBE
echo ========================================
echo.

REM Étape 1: Vérifier/Démarrer Minikube
echo [1/4] Verification de Minikube...
minikube status >nul 2>&1
if errorlevel 1 (
    echo Minikube n'est pas demarre. Demarrage...
    minikube start --driver=docker
    if errorlevel 1 (
        echo ERREUR: Impossible de demarrer Minikube
        exit /b 1
    )
) else (
    echo Minikube est deja demarre!
)

echo.
echo [2/4] Configuration de l'environnement Docker...
FOR /F "tokens=*" %%i IN ('minikube docker-env --shell cmd') DO %%i

echo.
echo [3/4] Construction des images Docker...
call build-images.bat

echo.
echo [4/4] Deploiement sur Kubernetes...
call deploy-k8s.bat

echo.
echo ========================================
echo DEPLOIEMENT TERMINE!
echo ========================================
echo.
echo Pour acceder a l'application:
echo   minikube service frontend --url
echo.
echo Autres commandes utiles:
echo   kubectl get all
echo   kubectl logs -f deployment/auth-service
echo   minikube dashboard
echo ========================================
