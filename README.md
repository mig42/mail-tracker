# mail-tracker

## Description
A simple application to retrieve delivery tracking information from post companies.

## Supported companies
* [Correos.es](http://www.correos.es)
* [GLS](https://www.gls-group.eu)

## Usage
    `python contentretriever.py [OPTIONS] [CODE [CODE [...]]]`

Codes are formed by a tracking code (supplied by the sender or the courier) and an optional identifier, separated by a `#` character.

Several options are available using the command line:

**-h**, **--help**: Shows a help message

**-f** `[FILE]`: Specifies a file in which tracking codes will be found. Including this option will ignore any code passed as command line argument.
 
**-q**: Quiet mode. Only critical messages will be printed.

**-m**, **--mail=** `[MAIL-LIST]`: The results will be sent to the specified comma-separated mail addresses. 

**-l**, **--last-event**: Print only the last event for each order.

