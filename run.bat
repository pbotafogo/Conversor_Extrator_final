@echo off
title Conversor Extrator SIAPE
echo ========================================
echo   CONVERSOR EXTRATOR SIAPE
echo ========================================
echo.

REM Verifica se o ambiente virtual existe
if not exist venv (
    echo [ERRO] Ambiente virtual nao encontrado!
    echo.
    echo Execute setup.bat primeiro para configurar o ambiente.
    echo.
    pause
    exit /b 1
)

echo [1/2] Ativando ambiente virtual...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo [ERRO] Falha ao ativar ambiente virtual.
    pause
    exit /b 1
)
echo [OK] Ambiente virtual ativado
echo.

echo [2/2] Iniciando aplicacao...
echo.
echo ========================================
echo   Interface Grafica Iniciando...
echo ========================================
echo.

REM Executa a aplicação
python src\conversor_extrator.py

REM Captura código de saída
set EXIT_CODE=%errorlevel%

if %EXIT_CODE% neq 0 (
    echo.
    echo [ERRO] Aplicacao encerrada com erro (codigo %EXIT_CODE%)
    echo.
    pause
)

REM Desativa o ambiente virtual
call venv\Scripts\deactivate.bat 2>nul

exit /b %EXIT_CODE%
