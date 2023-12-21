#!/bin/bash

# Función recursiva para borrar el contenido de una carpeta o crearla si no existe
function borrar_contenido_carpeta {
    local carpeta=$1

    # Verificar si la carpeta existe
    if [ ! -d "$carpeta" ]; then
        echo "Creando carpeta: $carpeta"
        mkdir -p "$carpeta"
    else
        echo "Borrando contenido de: $carpeta"
        rm -r "$carpeta"/*
    fi
}

# Obtener la ruta del directorio actual donde se encuentra el script
directorio_actual=$(dirname "$(readlink -f "$0")")

borrar_contenido_carpeta "$directorio_actual"/pdhg_rgb_den_gradient
borrar_contenido_carpeta "$directorio_actual"/pdhg_opp_den_gradient
borrar_contenido_carpeta "$directorio_actual"/pdhg_rgb_deb_gradient
borrar_contenido_carpeta "$directorio_actual"/pdhg_opp_deb_gradient


echo "Se ha completado el borrado de archivos en las carpetas."