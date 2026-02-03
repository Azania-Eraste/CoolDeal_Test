@echo off
REM quick-test.bat - Commandes rapides pour tester CoolDeal sur Windows

setlocal enabledelayedexpansion

echo.
echo  ======== COOLDEAL - Tests Rapides (Windows) ========
echo.
echo [1] Installation des dependances
echo     pip install -r requirements-test.txt
echo.
echo [2] Executer TOUS les tests
echo     pytest
echo.
echo [3] Tests UNITAIRES uniquement
echo     pytest -m unit
echo.
echo [4] Tests INTEGRATION uniquement
echo     pytest -m integration
echo.
echo [5] Tests d'une app specifique
echo     pytest shop/tests/
echo     pytest customer/tests/
echo.
echo [6] Rapport couverture (HTML + Terminal)
echo     pytest --cov=. --cov-exclude=*/migrations/* --cov-exclude=*/venv/* --cov-report=html --cov-report=term-missing
echo.
echo [7] Tests avec verbose
echo     pytest -v
echo.
echo [8] Tests avec affichage des print()
echo     pytest -s
echo.
echo [9] Tests les plus lents
echo     pytest --durations=10
echo.
echo [10] Reexecuter tests echoues
echo     pytest --lf
echo.
echo [11] Tests en parallele (rapide - necessite pytest-xdist)
echo     pytest -n auto
echo.
echo ====================================
echo Consultez TESTING_GUIDE.py pour plus d'options
echo ====================================
echo.

REM Prompt pour l'utilisateur
set /p choice="Choisir une option (1-11) ou 0 pour quitter: "

if "%choice%"=="0" goto end
if "%choice%"=="1" (
    echo.
    echo Installation en cours...
    pip install -r requirements-test.txt
    goto end
)
if "%choice%"=="2" (
    echo.
    echo Lancement des tests...
    pytest
    goto end
)
if "%choice%"=="3" (
    echo.
    echo Tests unitaires...
    pytest -m unit
    goto end
)
if "%choice%"=="4" (
    echo.
    echo Tests d'integration...
    pytest -m integration
    goto end
)
if "%choice%"=="5" (
    echo.
    echo Quelle app? (shop/customer)
    set /p app="App: "
    pytest !app!/tests/
    goto end
)
if "%choice%"=="6" (
    echo.
    echo Generation rapport couverture...
    pytest --cov=. --cov-exclude=*/migrations/* --cov-exclude=*/venv/* --cov-report=html --cov-report=term-missing
    echo.
    echo Ouvrir htmlcov\index.html pour le rapport HTML
    goto end
)
if "%choice%"=="7" (
    echo.
    pytest -v
    goto end
)
if "%choice%"=="8" (
    echo.
    pytest -s
    goto end
)
if "%choice%"=="9" (
    echo.
    pytest --durations=10
    goto end
)
if "%choice%"=="10" (
    echo.
    pytest --lf
    goto end
)
if "%choice%"=="11" (
    echo.
    pytest -n auto
    goto end
)

echo Option invalide!

:end
endlocal
