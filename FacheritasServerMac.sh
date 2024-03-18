#!/bin/bash
# 1- Abrir automator de MacOS
# 2- Selecionar aplicacion
# 3- en el segundo buscador casi en medio de todo, buscar "Ejecutar script shell"
# 4- Pegar este codigo
# 5- En la esquina superior izquierda, darle nombre y guardarlo en el escritorio
# 6- Ejecutar la app que se generó en el escritorio

cd ~/Desktop/FacherasCoffee
if [ ! -f "FacheritasVenv/bin/activate" ]; then
    python3 -m venv FacheritasVenv
	echo "entorno creado"
fi
source FacheritasVenv/bin/activate
echo "Entorno Activado"
pip3 install -r requirements.txt > /dev/null
echo "Requisitos instalados"
python3 manage.py runserver > /dev/null 2>&1 &
echo "Corriendo servidor..."

sleep 5
open http://127.0.0.1:8000