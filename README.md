# mail-tracker

A simple application to retrieve delivery tracking information from post companies.

### Companies supported
* [Correos.es](http://www.correos.es)
* [GLS](https://www.gls-group.eu)

### Usage
    python contentretriever.py [CODE]... [OPTION]...

> Receives a list of codes as arguments, or a file containing them.
>   -f <file>
>        Specifies a file in which tracking codes will be found.
>   -q
>       Supresses superfluous output messages.
>   -m, --mail <mail1,mail2,...>:
>       Specifies a mail to send tracking information
>   -l, --last-event
>       Just print last order event