#!/bin/bash

if [ ! -f "$1" ] || [ ! "$2" ]; then
    echo "Usage: $0 <tracking numbers file> <email>" >&2
    exit 1
fi

while read valor; do
    codigo=`echo $valor | cut -d\# -f1`
    comentario=`echo $valor | cut -d\# -f2`
    echo "### Pedido [ $codigo ] - [ $comentario ] ###"
done < $1
#    curl -k -s --data "numeros=$codigos&numero=$codigo&ecorreo=$2&accion=LocalizaVarios" "https://aplicacionesweb.correos.es/localizadorenvios/track.asp" > /dev/null

echo "Solicitud enviada"

