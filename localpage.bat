@echo off
SETLOCAL

REM Check for a "rebuild" or "build" argument
IF /I "%1"=="rebuild" GOTO :BUILD
IF /I "%1"=="build" GOTO :BUILD
GOTO :SERVE

:BUILD
    echo Building Jekyll site...
    jekyll build
    IF %ERRORLEVEL% NEQ 0 (
        echo Jekyll build failed.
        GOTO :EOF
    )
    echo Build complete.

:SERVE
    echo Serving Jekyll site locally...
    jekyll serve --baseurl ""
    IF %ERRORLEVEL% NEQ 0 (
        echo Jekyll serve failed.
    )

ENDLOCAL