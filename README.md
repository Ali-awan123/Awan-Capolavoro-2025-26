# 🧠 IntelliLife - Dashboard Personale

IntelliLife è una dashboard personale intelligente e minimale progettata per centralizzare e ottimizzare la gestione delle attività quotidiane, delle note e dello stato d'animo. L'applicazione offre un'interfaccia scannabile, moderna e ad alte prestazioni, focalizzata interamente sulla produttività e sull'efficienza mentale senza distrazioni.

---

## 🎯 In cosa consiste l'applicazione

L'applicazione si struttura in 6 macro-aree principali navigabili comodamente dalla barra laterale:

1. **🏠 Home Center**
   Un hub centrale che mostra il riepilogo visivo dell'efficienza dei propri task, il numero di note in archivio e un widget per definire il proprio focus della giornata.

2. **✅ Task Manager**
   Un registro attività completo in cui è possibile pianificare nuovi task, impostare scadenze temporali e assegnare tre diversi livelli di criticità (Bassa, Media, Alta). Permette di smarcare le attività o eliminarle in tempo reale.

3. **📅 Agenda Digitale**
   Un calendario interattivo che mappa automaticamente i task inseriti, colorando le scadenze in base alla priorità per un colpo d'occhio immediato.

4. **📝 Note**
   Un blocco note digitale pulito per scrivere, catalogare ed eliminare appunti in modo rapido.

5. **⏱️ Focus Timer (Pomodoro)**
   Un timer di concentrazione basato sulla tecnica dei 25 minuti di lavoro continuo, assistito da una barra di avanzamento e da un contatore testuale fisso e pulito.

6. **📊 Impostazioni**
   Un'area dedicata alla personalizzazione del proprio profilo utente, al tracciamento del proprio livello di energia giornaliero (Mood Journal) e alla visualizzazione di grafici statistici interattivi.

---

## 💾 Gestione dei Dati Locale e Leggera

Il sistema è completamente autonomo e locale: tutte le informazioni vengono salvate e lette in automatico all'interno di semplici file in formato `.csv` (fogli di calcolo testuali) generati direttamente nella cartella del progetto. 

Questo rende l'applicazione:
* **Sicura:** I dati rimangono privati sul tuo computer.
* **Portabile:** Puoi spostare la cartella dove vuoi senza perdere nulla.
* **Leggera:** Non necessita di configurazioni esterne per funzionare.

---

## 🛠️ Tecnologie e Librerie Utilizzate

Per lo sviluppo di questo progetto è stato utilizzato il linguaggio **Python** insieme a un ecosistema di librerie moderne per l'interfaccia web e l'analisi dati:

* **Streamlit:** Il framework principale utilizzato per convertire lo script Python in un'applicazione web interattiva, performante e reattiva.
* **Pandas:** Libreria fondamentale utilizzata per gestire i dataset dei task, delle note e del profilo utente memorizzati nei file CSV.
* **Plotly Express:** Utilizzata per generare i grafici interattivi (grafici a torta per lo stato dei task e grafici a linee per l'andamento del ciclo energetico).
* **Streamlit Calendar:** Componente personalizzato per integrare un calendario completo (FullCalendar) nativamente dentro l'interfaccia.
* **HTML5 / CSS3:** Utilizzati per l'iniezione di stili personalizzati tramite un file `style.css` esterno, garantendo un tema scuro (Dark Mode) premium con gradienti e card animate.

---

---

## 🚀 Come eseguo l'applicazione

1. Mi assicuro di aver installato Python sul mio computer.

2. Installo tutte le librerie necessarie eseguendo nel mio terminale questo comando:
   ```bash
   pip install streamlit pandas plotly streamlit-calendar