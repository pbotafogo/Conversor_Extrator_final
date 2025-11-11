@echo off
title Deploy GitHub - Conversor Extrator
echo ========================================
echo   DEPLOY NO GITHUB
echo   Conversor Extrator SIAPE
echo ========================================
echo.

REM Verifica se o Git esta instalado
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] Git nao encontrado. Instale o Git primeiro.
    echo.
    echo Baixe em: https://git-scm.com/download/win
    pause
    exit /b 1
)

echo [OK] Git encontrado
git --version
echo.

REM Verifica se esta em um repositorio Git
if not exist .git (
    echo [ERRO] Este diretorio nao e um repositorio Git.
    echo Execute 'git init' primeiro ou verifique o diretorio.
    pause
    exit /b 1
)

echo ========================================
echo   CONFIGURACAO DO REPOSITORIO
echo ========================================
echo.

REM Verifica se ja existe um repositorio remoto
git remote -v | findstr "origin" >nul 2>&1
if %errorlevel% equ 0 (
    echo Repositorio remoto ja configurado:
    echo.
    git remote -v
    echo.
    echo ----------------------------------------
    set /p CONFIRM="Deseja fazer push das alteracoes? (S/N): "
    if /i not "%CONFIRM%"=="S" (
        echo.
        echo Operacao cancelada pelo usuario.
        pause
        exit /b 0
    )
    goto :push
) else (
    echo Nenhum repositorio remoto configurado.
    echo.
    echo ========================================
    echo   PASSOS PARA CONFIGURAR GITHUB:
    echo ========================================
    echo.
    echo 1. Acesse: https://github.com/new
    echo 2. Crie um novo repositorio
    echo 3. Nome sugerido: Conversor_Extrator_Final
    echo 4. Deixe DESMARCADO "Initialize with README"
    echo 5. Copie a URL do repositorio
    echo.
    echo Formatos aceitos:
    echo   HTTPS: https://github.com/usuario/repositorio.git
    echo   SSH:   git@github.com:usuario/repositorio.git
    echo.
    echo ----------------------------------------
    set /p REPO_URL="Cole a URL do repositorio GitHub: "
    
    if "%REPO_URL%"=="" (
        echo.
        echo [ERRO] URL nao fornecida.
        pause
        exit /b 1
    )
    
    echo.
    echo Adicionando repositorio remoto...
    git remote add origin %REPO_URL%
    
    if %errorlevel% neq 0 (
        echo.
        echo [ERRO] Falha ao adicionar repositorio remoto.
        echo Verifique se a URL esta correta.
        pause
        exit /b 1
    )
    
    echo [OK] Repositorio remoto adicionado com sucesso!
    echo.
)

:push
echo ========================================
echo   STATUS DO REPOSITORIO
echo ========================================
echo.
git status
echo.

REM Pergunta sobre commit
echo ----------------------------------------
set /p FAZER_COMMIT="Deseja criar um novo commit? (S/N): "

if /i "%FAZER_COMMIT%"=="S" (
    echo.
    set /p COMMIT_MSG="Digite a mensagem do commit: "
    
    if "%COMMIT_MSG%"=="" (
        set COMMIT_MSG=Atualizacao do projeto
    )
    
    echo.
    echo Adicionando arquivos ao commit...
    git add .
    
    if %errorlevel% neq 0 (
        echo [ERRO] Falha ao adicionar arquivos.
        pause
        exit /b 1
    )
    
    echo Criando commit...
    git commit -m "%COMMIT_MSG%"
    
    if %errorlevel% neq 0 (
        echo [AVISO] Nenhuma alteracao para commitar ou erro ao commitar.
        echo.
    ) else (
        echo [OK] Commit criado com sucesso!
        echo.
    )
)

echo ========================================
echo   ENVIANDO PARA O GITHUB
echo ========================================
echo.
echo Configurando branch principal como 'main'...
git branch -M main

echo Enviando arquivos para o GitHub...
echo.

git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo   DEPLOY CONCLUIDO COM SUCESSO!
    echo ========================================
    echo.
    echo Seu projeto esta disponivel no GitHub!
    echo.
    echo Acesse seu repositorio em:
    git remote get-url origin
    echo.
) else (
    echo.
    echo ========================================
    echo   ERRO AO ENVIAR PARA O GITHUB
    echo ========================================
    echo.
    echo Possiveis causas:
    echo   1. Credenciais invalidas
    echo   2. Sem conexao com internet
    echo   3. Repositorio nao existe no GitHub
    echo   4. Falta de permissao no repositorio
    echo.
    echo Para autenticacao:
    echo   - Use GitHub Desktop: https://desktop.github.com/
    echo   - Ou configure SSH keys: https://docs.github.com/pt/authentication
    echo   - Ou use Personal Access Token
    echo.
)

echo.
pause
