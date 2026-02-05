@echo off
setlocal
REM =====================================================
REM  KBJ ↔ KBJ2 Dual-Agent System Launcher
REM =====================================================

set "KBJ2_ROOT=F:\kbj2"
set "GLM_KEYS=384fffa4d8a44ce58ee573be0d49d995.kqLAZNeRmjnUNPJh,9c5b377b9bf945d0a2b00eacdd9904ef.BoRiu74O1h0bV2v6,a9bd9bd3917c4229a49f91747c4cf07e.PQBgL1cU7TqcNaBy,f7cd2ea443964565aadf6191f49ac90b.MmysR4QLiQAvv2kZ"
set "ANTHROPIC_API_KEY=a9bd9bd3917c4229a49f91747c4cf07e.PQBgL1cU7TqcNaBy"
set "ANTHROPIC_BASE_URL=https://api.z.ai/api/anthropic"
set "API_TIMEOUT_MS=3000000"
set "PYTHONIOENCODING=utf-8"

:: Check Mode - 자연어 명령은 300인 총동원으로
if "%~1"=="--dual" goto DualDialog
if "%~1"=="--solve" goto ProblemSolve
if "%~1"=="--turbo" goto TurboCollab
if "%~1"=="--server" goto SocketServer
if "%~1"=="--corp100" goto Corp100
if "%~1"=="--supreme" goto Supreme300
if "%~1"=="--old" goto Automation
if "%~1"=="" goto Interactive
if "%~1"=="-p" goto OneShot
:: 자연어 명령 → 300인 총동원 (KBJ+KBJ2 세트 + 서브에이전트)
goto Supreme300Cmd

:TurboCollab
    echo.
    echo ====================================================
    echo  ⚡ KBJ ↔ KBJ2 Turbo Collaboration Mode
    echo ====================================================
    echo  KBJ 전략 + KBJ2 120에이전트 병렬 실행
    echo ====================================================
    echo.
    shift
    python "%KBJ2_ROOT%\turbo_collab.py" %1 %2
    goto End

:SocketServer
    echo.
    echo ====================================================
    echo  🌐 KBJ2 Socket Server Mode (NEW GUIDE 20인 조직)
    echo ====================================================
    echo  localhost:9100-9300 고속 통신
    echo ====================================================
    echo.
    shift
    python "%KBJ2_ROOT%\socket_server.py" %1 %2 %3
    goto End

:Corp100
    echo.
    echo ====================================================
    echo  🏢 KBJ2 Real 100-Agent Corporation Mode
    echo ====================================================
    echo  실제 100개 에이전트 인스턴스 병렬 실행
    echo ====================================================
    echo.
    shift
    python "%KBJ2_ROOT%\real_100_agents.py" %1 %2
    goto End

:Supreme300
    echo.
    echo ====================================================
    echo  🔥🔥🔥 SUPREME 300-AGENT TOTAL MOBILIZATION 🔥🔥🔥
    echo ====================================================
    echo  KBJ+KBJ2 세트 지휘 + 300인 병렬 + 66개 스킬 총동원
    echo ====================================================
    echo.
    shift
    python "%KBJ2_ROOT%\supreme_300.py" %1 %2 %3
    goto End

:Supreme300Cmd
    echo.
    echo ====================================================
    echo  🔥🔥🔥 SUPREME 300-AGENT TOTAL MOBILIZATION 🔥🔥🔥
    echo ====================================================
    echo  KBJ+KBJ2 세트 지휘 + 300인 병렬 + 66개 스킬 총동원
    echo ====================================================
    echo.
    python "%KBJ2_ROOT%\supreme_300.py" "%*" "%CD%"
    goto End

:AutoOrchestrate
    echo.
    echo ====================================================
    echo  🤖 KBJ2 Auto Orchestrator - 자연어 명령 자동 실행
    echo ====================================================
    echo  에이전트 자동 토론 → 코드 생성 → 검증
    echo ====================================================
    echo.
    python "%KBJ2_ROOT%\auto_orchestrator.py" "%*" "%CD%"
    goto End

:DualDialog
    echo.
    echo ====================================================
    echo  🤝 KBJ ↔ KBJ2 Dual-Agent Dialog Mode
    echo ====================================================
    echo.
    shift
    python "%KBJ2_ROOT%\dual_agent_dialog.py" %1 %2 %3
    goto End

:ProblemSolve
    echo.
    echo ====================================================
    echo  🔧 KBJ ↔ KBJ2 Problem Solver Mode
    echo ====================================================
    echo  문제 발견 → 의견 교환 → 실행 → 해결까지 반복
    echo ====================================================
    echo.
    shift
    python "%KBJ2_ROOT%\problem_solver.py" %1 %2
    goto End

:Interactive
    :: Launch Interactive Mode (Chat)
    echo 🏢 [KBJ2 Corp] Entering Secure Command Line...
    echo 🗣️  [Interactive Mode] - Supreme Commander Online
    
    if exist "%~dp0claude-orig.cmd" (
        "%~dp0claude-orig.cmd" --model GLM-4.7 "%~dp0KBJ2_MANUAL.md"
    ) else (
        "%APPDATA%\npm\claude.cmd" --model GLM-4.7 "%~dp0KBJ2_MANUAL.md"
    )
    goto End

:OneShot
    :: Launch One-Shot Mode (Print)
    if exist "%~dp0claude-orig.cmd" (
        "%~dp0claude-orig.cmd" %* --model GLM-4.7 "%~dp0KBJ2_MANUAL.md"
    ) else (
        "%APPDATA%\npm\claude.cmd" %* --model GLM-4.7 "%~dp0KBJ2_MANUAL.md"
    )
    goto End

:Automation
    :: Launch Automation Mode (Python)
    echo [KBJ2] Initializing Universal Orchestrator...
    python "%~dp0kbj2_orchestrator.py" %*
    goto End

:End
echo.
echo ====================================================
echo  🔥 KBJ2 Available Modes:
echo    kbj2 [command]          = 🔥 300인 총동원 (DEFAULT)
echo    kbj2 --supreme [cmd]    = 🔥 300인 총동원 (명시적)
echo    kbj2 --corp100 [path]   = 🏢 100-Agent Corporation
echo    kbj2 --turbo [path]     = ⚡ Turbo Collaboration
echo    kbj2 --dual [path]      = 🤝 Dual-Agent Dialog
echo    kbj2 --solve [path]     = 🔧 Problem Solver
echo    kbj2 --server           = 🌐 Socket Server (20인)
echo    kbj2 --old              = 📜 Legacy Orchestrator
echo    kbj2                    = 💬 Interactive Chat
echo ====================================================

