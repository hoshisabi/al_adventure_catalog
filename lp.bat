@echo off
SETLOCAL

REM Check for a "rebuild" or "build" argument
IF /I "%1"=="rebuild" GOTO :BUILD
IF /I "%1"=="build" GOTO :BUILD
GOTO :SERVE

:BUILD
    echo Running aggregator.py...
    REM Note: Script uses centralized path configuration and works regardless of CWD,
    REM but this .bat file assumes it's run from the project root (where pyproject.toml is).
    uv run python -m maintaindb.aggregator
    IF %ERRORLEVEL% NEQ 0 (
        echo Aggregator failed.
        GOTO :EOF
    )
    echo Aggregator finished.
    GOTO :SERVE

:SERVE
    echo Serving site locally at http://localhost:8000 ...
    echo To rebuild the catalog before serving, run with the "rebuild" parameter (e.g., lp rebuild)
    uv run python serve.py
    IF %ERRORLEVEL% NEQ 0 (
        echo Serve failed.
    )

ENDLOCAL