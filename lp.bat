@echo off
SETLOCAL

REM Check for a "rebuild" or "build" argument
IF /I "%1"=="rebuild" GOTO :BUILD
IF /I "%1"=="build" GOTO :BUILD
GOTO :SERVE

:BUILD
    echo Running aggregator.py...
    uv run maintaindb\aggregator.py
    IF %ERRORLEVEL% NEQ 0 (
        echo Aggregator failed.
        GOTO :EOF
    )
    echo Copying all_adventures.json...
    copy maintaindb\_stats\all_adventures.json assets\data\all_adventures.json
    IF %ERRORLEVEL% NEQ 0 (
        echo Failed to copy all_adventures.json.
        GOTO :EOF
    )
    echo Building Jekyll site...
    call jekyll build
    IF %ERRORLEVEL% NEQ 0 (
        echo Jekyll build failed.
        GOTO :EOF
    )
    echo Build complete.
    GOTO :SERVE

:SERVE
    echo Serving Jekyll site locally...
    echo To rebuild the site before serving, run with the "rebuild" parameter (e.g., lp rebuild)
    jekyll serve --baseurl ""
    IF %ERRORLEVEL% NEQ 0 (
        echo Jekyll serve failed.
    )

ENDLOCAL