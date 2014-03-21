#!/bin/bash

if [ ! -f "$1" ] || [ ! "$2" ]; then
    echo "Usage: $0 <tracking numbers file> <email>" >&2
    exit 1
fi

while read lectura; do codigo=lectura
done < "$1"
echo $codigo

codigos=$(tr '\n' ' ' < $1)
    echo "### Pedido [ $codigos ] ###"
    curl -k -s --data "numeros=$codigos&numero=$codigo&ecorreo=$2&accion=LocalizaVarios" "https://aplicacionesweb.correos.es/localizadorenvios/track.asp"


#  curl -k -s --data "numeros=RF196344966SG RF207323315SG&numero=RF207323315SG&ecorreo=Pando85@msn.com&accion=LocalizaVarios" "https://aplicacionesweb.correos.es/localizadorenvios/track.asp"

