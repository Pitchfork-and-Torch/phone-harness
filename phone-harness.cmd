@echo off
REM Windows / generic launcher. Actions refuse unless the host is Darwin.
setlocal
set "ROOT=%~dp0"
set "PYTHONPATH=%ROOT%src;%PYTHONPATH%"
py -3 -m phone_harness.run %*
exit /b %ERRORLEVEL%
