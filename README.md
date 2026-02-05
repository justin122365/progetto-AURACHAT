AURACHAT
Descrizione del progetto

AURACHAT è un semplice sistema di chat client-server sviluppato in Python che utilizza i socket di rete.
Il progetto dimostra l’uso combinato dei protocolli UDP e TCP per permettere ai client di scoprire automaticamente il server e comunicare tra loro tramite messaggi di testo.

Il server non partecipa attivamente alla comunicazione, ma si occupa solo della gestione dei client e dell’instradamento dei messaggi.

Struttura del progetto
AURACHAT/
├── server.py
├── client.py
└── util/
    ├── config.json
    └── log.xml

Descrizione file

server.py → avvia il server TCP e UDP, gestisce i client e i log

client.py → permette a un utente di collegarsi e chattare

util/config.json → contiene porte di rete e configurazioni

util/log.xml → salva i log del server in formato XML

Funzionamento generale

Il server viene avviato ed entra in attesa:

UDP per la discovery

TCP per le connessioni dei client

Il client:

invia un messaggio UDP di discovery

riceve l’IP del server

si collega al server tramite TCP

I client possono:

inviare comandi

chattare con altri client

uscire dal sistema

Il server:

gestisce più client contemporaneamente

chiude automaticamente un client dopo 2 minuti di inattività

salva tutte le attività nel file log.xml

Protocolli utilizzati

UDP

utilizzato per la fase di discovery

permette ai client di trovare il server automaticamente

TCP

utilizzato per la comunicazione principale

garantisce affidabilità dei messaggi

Comandi principali supportati

TIME → restituisce l’ora corrente del server

EXIT → disconnette il client

CHAT <ID> <messaggio> → invia un messaggio a un altro client

Esempio:

CHAT c2 Ciao come stai?

Logging

Il server salva gli eventi principali in formato XML, tra cui:

connessione di un client

disconnessione

messaggi inviati

Questo permette di mantenere uno storico strutturato delle attività.

Obiettivi del progetto

Utilizzare socket TCP e UDP

Gestire più client contemporaneamente

Implementare una chat client-client

Gestire timeout di inattività

Salvare i log in formato XML

Mantenere il codice semplice e comprensibile

Note finali

Il progetto è stato sviluppato con l’obiettivo di comprendere il funzionamento delle reti, senza utilizzare librerie avanzate o database, mantenendo una struttura semplice e didattica.
