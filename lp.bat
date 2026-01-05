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
    echo Copying all_adventures.json...
    copy maintaindb\_stats\all_adventures.json assets\data\all_adventures.json
    IF %ERRORLEVEL% NEQ 0 (
        echo Failed to copy all_adventures.json.
        GOTO :EOF
    )
    echo Building Jekyll site...
    call bundle exec jekyll build
    IF %ERRORLEVEL% NEQ 0 (
        echo Jekyll build failed.
        GOTO :EOF
    )
    echo Build complete.
    GOTO :SERVE

:SERVE
    echo Serving Jekyll site locally...
    echo To rebuild the site before serving, run with the "rebuild" parameter (e.g., lp rebuild)
    bundle exec jekyll serve --baseurl ""
    IF %ERRORLEVEL% NEQ 0 (
        echo Jekyll serve failed.
    )

ENDLOCAL