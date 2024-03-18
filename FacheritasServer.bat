@echo off

echo Verificando entorno virtual 
if not exist FacheritasVenv\Scripts\activate.bat (
    python -m venv FacheritasVenv
    echo Entorno Creado creado... Iniciando
)
echo Creado 
call FacheritasVenv\Scripts\activate.bat


pip install -r requirements.txt >nul 2>&1
python loading_animation.py
echo Iniciando...

start  /MIN cmd /c "python manage.py runserver" >nul 2>&1

timeout /t 5 /nobreak >nul

start http://127.0.0.1:8000