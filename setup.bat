@echo off
echo ========================================
echo   CONFIGURACAO DO CONVERSOR EXTRATOR
echo ========================================
echo.

REM Verifica se Python esta instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] Python nao encontrado. Instale o Python primeiro.
    echo.
    echo Baixe em: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [OK] Python encontrado
python --version
echo.

echo [1/3] Criando ambiente virtual...
if not exist venv (
    python -m venv venv
    if %errorlevel% neq 0 (
        echo [ERRO] Falha ao criar ambiente virtual.
        pause
        exit /b 1
    )
    echo [OK] Ambiente virtual criado com sucesso!
) else (
    echo [INFO] Ambiente virtual ja existe.
)
echo.

echo [2/3] Ativando ambiente virtual...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo [ERRO] Falha ao ativar ambiente virtual.
    pause
    exit /b 1
)
echo [OK] Ambiente virtual ativado
echo.

echo [3/3] Instalando dependencias...
echo Atualizando pip...
python -m pip install --upgrade pip --quiet
echo Instalando pacotes...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERRO] Falha ao instalar dependencias.
    pause
    exit /b 1
)
echo [OK] Dependencias instaladas com sucesso!
echo.

echo ========================================
echo   CONFIGURACAO CONCLUIDA!
echo ========================================
echo.
echo Pacotes instalados:
pip list | findstr /i "pandas sqlalchemy mysql"
echo.
echo Para executar o programa, use: run.bat
echo.
pause
