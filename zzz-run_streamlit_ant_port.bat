@echo off
setlocal enabledelayedexpansion

set PORT=8501
set MAX_PORT=8510

:loop
netstat -ano | findstr :%PORT% >nul
if %errorlevel% == 0 (
    echo Port %PORT% is in use. Trying next port...
    set /a PORT+=1
    if %PORT% geq %MAX_PORT% (
        echo No available port found between 8501 and 8510.
        exit /b
    )
    goto loop
)

echo Running Streamlit on port %PORT%...
streamlit run app.py --server.port=%PORT%