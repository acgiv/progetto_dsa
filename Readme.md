# I Segreti della memoria: Un approccio Delizioso per apprendere e conservare i concetti

### Cosa caratterizza i bambini con Disturbi Specifici dell'Apprendimento (DSA)

I bambini con Disturbi Specifici dell'Apprendimento (DSA) spesso incontrano difficoltà nella lettura.
La loro lettura può essere faticosa, lenta e caratterizzata da vari tipi di errori, come scambi di lettere, omissioni di parole, riduzioni o aggiunte di elementi, e salti di righe. 
Questi errori possono influire sulla loro capacità di comprendere correttamente il testo. I bambini con DSA possono avere difficoltà nel decodificare correttamente i suoni delle lettere e nel collegarli in modo accurato per formare parole. 
Questa difficoltà può portare a confusione durante la lettura e causare errori.

Durante le attività di lettura, i bambini con DSA possono commettere i seguenti tipi di errori:
1. **Inversioni**:
   * Scambiano l'ordine delle lettere nelle parole, leggendo ad esempio "**pirgione**" al posto di "**prigione**".
   * Scambiano le lettere con le loro speculari, ad esempio leggono "**b**" al posto di "**q**". 
   * Invertono l'ordine delle parole nella frase, ad esempio leggono "il ratto insegue il "**gatto**" al posto di "**il gatto insegue il ratto**".
2. **Omissioni**:
   * Omettono una o più parole o parti di parole durante la lettura.
3. **Sostituzioni**:
   * Sostituiscono una consonante con un'altra che ha una grafia simile, come ad esempio 
   "**E**" al posto di "**F**".
   * Sostituiscono una lettera con un'altra che ha una grafia simile, ma è speculare, come 
   ad esempio "**b**" con "d**" o "**p**" con "**t**".
   * Sostituiscono una lettera con un'altra che ha un suono articolatorio simile, come ad 
   esempio "**d**" con "**t**".
   * Sostituiscono una parola con un'altra che non ha alcun grafema in comune.
   * Sostituiscono una o più parole con termini dialettali corrispondenti.

Questi errori possono verificarsi a causa delle difficoltà nel decodificare correttamente i suoni delle 
lettere, collegarli in modo accurato per formare parole e organizzare correttamente la sequenza delle 
parole durante la lettura.
Inoltre, nel momento in cui i bambini con DSA imparano a leggere, questa attività viene svolta 
lentamente e con numerosi errori caratteristici, a causa di una carenza delle funzioni principali 
coinvolte.

1. **Funzioni linguistiche**: i bambini con DSA presentano una ridotta capacità di percepire, 
   distinguere e manipolare i suoni del linguaggio, noto come deficit fonologico e 
   metafonologico. Ciò comporta difficoltà nel distinguere chiaramente i suoni che compongono 
   le parole, nell'associare il suono alla lettera corrispondente e nel mettere insieme i suoni per 
   formare parole.
2. **Funzioni di percezione visiva e di focalizzazione attentiva**: i bambini con DSA possono 
   manifestare un deficit nel processamento percettivo dell'informazione visiva. Questo si 
   traduce in inversioni.

## Soluzione alla problematica
Per affrontare questa problematica, è stato sviluppato un sistema che consente di inserire del testo da sintetizzare all'interno di una chatbot.
Il sistema restituisce il testo sintetizzato con una spiegazione adeguata all'età del destinatario. La sintesi è realizzata utilizzando **ChatGPT**.
Per migliorare la comprensione e la memorizzazione dei concetti, hai deciso di adottare la tecnica dell'associazione di testi alle immagini, con spiegazioni fornite oralmente dal robot Pepper Tony.
Quando l'utente desidera utilizzare questa funzionalità, sarà sufficiente premere il pulsante presente sul robot.

#### Tecnica associazioni alle immagini 
La tecnica dell'associazione di immagini per la memorizzazione dei concetti è un metodo efficace per 
migliorare la capacità di ricordare informazioni in modo più vivido e duraturo. Questa tecnica sfrutta 
il potere delle immagini per creare un collegamento visivo e emotivo tra i concetti da imparare e le 
immagini stesse. Quando associamo un'immagine vivida e significativa a un concetto, creiamo un 
collegamento visivo ed emotivo che facilita il recupero delle informazioni durante lo studio e 
l'apprendimento. Le immagini creano un'impressione duratura nella memoria, rendendo più semplice 
richiamare il concetto quando necessario. 
Per esempio, se stiamo cercando di ricordare la parola "albero", possiamo associarla a un'immagine 
vivida di un maestoso albero con foglie verdi e rami robusti. Questa immagine distintiva aiuta a creare 
un'associazione visiva ed emotiva con la parola "albero", rendendola più facile da ricordare.
Quando utilizziamo l'associazione di immagini, è importante scegliere immagini che abbiano un 
impatto visivo ed emotivo significativo. Le immagini dovrebbero essere facilmente riconoscibili e 
connesse al concetto che vogliamo memorizzare. Ad esempio, possiamo utilizzare immagini colorate, 
dettagliate e coinvolgenti che catturino l'attenzione e stimolino l'interesse. La scelta delle immagini.


# SPIGAZIONE DEL PROGRAMMA

### FILE .env

**Per utilizzare questo programma**, è necessario creare un file **.env** all'interno del progetto e inserire le variabili con i dati appropriati. Assicurati di seguire queste indicazioni:

1. Crea un file chiamato ".env" nella directory principale del tuo progetto.
2. Apri il file .env con un editor di testo.
3. All'interno del file, inserisci le variabili necessarie seguendo il formato **"NOME_VARIABILE=valore"**.
4. Assicurati di inserire i dati corretti per ciascuna variabile richiesta nel programma.
5. Salva il file .env dopo aver inserito tutte le variabili.

Le varibili da inserire sono:
> CONNECTION_DB = api_key_del_database_MongoDb </br>
> PATH_STATIC =path_global_Static_this_project exemple ="C:\xampp\htdocs\flaskProject\static"</br>
>SESSION_KEY= key_session_flask  </br>
>TOKEN_CHAT_GPT= token_ChatGpt

### FILE app.py

