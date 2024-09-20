# FLOCK GAME

## Requirements
Python (3.11.9 se dove scaricarlo)
Virtualenv
Installate i requirements.txt tramite pip

## Istruzioni Base


## Funzionamento Generale
Il programma è diviso in SCENE che costituiscono possibili livelli o menu. In ogni momento c'è una scena attiva scelta tramite MANAGER che consente anche di cambiare le scene tra di loro.
Le scene di gioco si basano sulla classe GAME. Il meccaniso generale di qualsiasi scena è mostrato nella funzione RUN del MAIN ed è basato sul loop:
- POOL_EVENTS: raccogliere gli input, sia da tastiera che da tracker
- UPDATE: Aggiorna tutto il necessario spostandosi di dt (dt è adattivo in funzione di quanto ci mette a calcolare) rispetto all'istante precedente
- RENDER: Ridisegna tutto sullo SCREEN. 

## Questioni Aperte
- Che forme possono avere gli ostacoli
- Come interagiscono con gli ostacoli in caso di schianto?
- Ha senso muovere il player tramite l'angolo, immaginando la direzione puntata con la mano?