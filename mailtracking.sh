#!/bin/bash

if [ ! -f "$1" ] || [ ! "$2" ]; then
    echo "Usage: $0 <tracking numbers file> <email>" >&2
    exit 1
fi

while read lectura; do codigo=lectura
done < "$1"


codigos=$(cut -d '#' -d '\n' |tr '\n' ' ' < $1)
    echo "### Pedido [ $codigos ] ###"
#    curl -k -s --data "numeros=$codigos&numero=$codigo&ecorreo=$2&accion=LocalizaVarios" "https://aplicacionesweb.correos.es/localizadorenvios/track.asp" > /dev/null

echo "Solicitud enviada"

