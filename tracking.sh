#!/bin/bash

function print_usage {
    echo "Usage: $0 <tracking numbers file> [-s || --short]" >&2
}

function is_correct {
    if [ ! "$1" ]; then
        return 1
    fi
    if [ "$1" == "-s" ] || [ "$1" == "--short" ]; then
        return 0
    fi
    return 1
}

if [ ! -f "$1" ]; then
    print_usage
    exit 1
fi

parameter=
if [ "$2" ]; then
    if ! is_correct $2; then
        print_usage
        exit 2
    fi
    parameter="$2"
fi

while read linea; do
    codigo=`echo $linea | cut -d\# -f1`
    comentario=`echo $linea | cut -d\# -f2`
    if [ ! "$comentario" ]; then
        comentario=$codigo
    fi    
    echo "### Pedido [ $comentario ] ###"
    curl -k -s --data "numero=$codigo&accion=LocalizaUno" "https://aplicacionesweb.correos.es/localizadorenvios/track.asp" | tail -n 4 | head -1 | LANG=es_ES.iso88591 sed 's/.*soap:Body.\(.*\)<\/soap:Body.*/\1/g' | python mailTracker.py $parameter
    echo ""
done < "$1"
