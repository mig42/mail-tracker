# mail-tracker

A simple application to retrieve delivery tracking information from post companies.

### Companies supported
* [Correos.es](http://www.correos.es)
* [GLS](https://www.gls-group.eu)

### Usage
    python contentretriever.py [CODE]... [OPTION]...

Several options are available using the command line:
    -h, --help            show this help message and exit
    -f FILE             specifies a file in which tracking codes will be found.
    -q                    supresses superfluous output messages.
    -m MAIL_1,MAIL_2,..., --mail=MAIL_1,MAIL_2,...
                          specifies a mail to send tracking information
    -l, --last-event      just print last order event

