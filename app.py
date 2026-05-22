import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_calendar import calendar
import datetime
import time
import os

# --- 1. CONFIGURAZIONE PAGINA ---
st.set_page_config(
    page_title="IntelliLife - Dashboard Personale",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. FUNZIONE CARICAMENTO CSS DA FILE ESTERNO ---
def local_css(file_name):
    if os.path.exists(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.warning(f"Nota: File di stile '{file_name}' non trovato nella cartella corrente. Verrà usato il tema standard.")

# Carica lo stile separato
local_css("style.css")

# --- 3. ARCHIVIAZIONE DATI LOCALI (FILE CSV - NESSUN DATABASE UTILIZZATO) ---
FILES = {
    "todo": "data_todo.csv",
    "notes": "data_notes.csv",
    "mood": "data_mood.csv",
    "profile": "data_profile.csv"
}

# Genera i file CSV se non esistono ancora
if not os.path.exists(FILES["todo"]):
    pd.DataFrame(columns=["Task", "Scadenza", "Priorità", "Stato"]).to_csv(FILES["todo"], index=False)
if not os.path.exists(FILES["notes"]):
    pd.DataFrame(columns=["Titolo", "Contenuto", "Data"]).to_csv(FILES["notes"], index=False)
if not os.path.exists(FILES["mood"]):
    pd.DataFrame(columns=["Data", "Mood", "Note"]).to_csv(FILES["mood"], index=False)
if not os.path.exists(FILES["profile"]):
    pd.DataFrame(columns=["Username", "Bio"]).to_csv(FILES["profile"], index=False)

def load_csv(key): 
    return pd.read_csv(FILES[key])

def save_csv(df, key): 
    df.to_csv(FILES[key], index=False)

# --- 4. LETTURA DATI PROFILO UTENTE ---
df_prof = load_csv("profile")
if df_prof.empty:
    username = "Ospite"
    user_bio = "La mia Dashboard Personale"
else:
    username = df_prof.iloc[0]["Username"]
    user_bio = df_prof.iloc[0]["Bio"]

# --- 5. NAVIGAZIONE SIDEBAR ---
st.sidebar.markdown("<div style='text-align:center;'><h2>🧠 IntelliLife</h2><p style='color:#818cf8; font-size:14px;'>Smart Management Hub</p></div>", unsafe_allow_html=True)
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Navigazione Canali:",
    ["🏠 Home Center", "✅ Task Manager", "📅 Agenda Digitale", "📝 Note", "⏱️ Focus Timer (Pomodoro)", "📊 Impostazioni"]
)

st.sidebar.markdown("---")
st.sidebar.caption(f"Utente attivo: **{username}**")
st.sidebar.caption(f"Data di oggi: {datetime.date.today().strftime('%d/%m/%Y')}")


# AREA 1: HOME CENTER
if menu == "🏠 Home Center":
    st.markdown(f"""
    <div class="hero-banner">
        <h1 style='margin:0; font-size:32px;'>🧠 IntelliLife Dashboard</h1>
        <p style='margin:8px 0 0 0; opacity:0.9; font-size:16px;'>Benvenuto nell'hub centrale per la gestione delle tue attività quotidiane.</p>
    </div>
    """, unsafe_allow_html=True)
    
    t_df = load_csv("todo")
    n_df = load_csv("notes")
    
    done_tasks = len(t_df[t_df["Stato"] == "Completato"])
    total_tasks = len(t_df)
    total_notes = len(n_df)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"<div class='premium-card'><h3>Task Completati</h3><p>✅ {done_tasks} / {total_tasks}</p></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='premium-card'><h3>Note In Archivio</h3><p>📝 {total_notes}</p></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='premium-card'><h3>Efficienza Task</h3><p>📊 {int((done_tasks/total_tasks)*100) if total_tasks > 0 else 0}%</p></div>", unsafe_allow_html=True)


# AREA 2: TASK MANAGER
elif menu == "✅ Task Manager":
    st.header("✅ Registro Attività e Task", divider="violet")
    st.caption("Pianifica le tue attività, imposta scadenze e assegna le priorità.")
    
    t_df = load_csv("todo")
    
    with st.expander("➕ Inserisci una Nuova Attività", expanded=True):
        c1, c2, c3 = st.columns([2, 1, 1])
        with c1:
            t_name = st.text_input("Nome dell'attività:", placeholder="Compilare documentazione...")
        with c2:
            t_date = st.date_input("Scadenza termine:", datetime.date.today())
        with c3:
            t_prior = st.selectbox("Livello Criticità:", ["Bassa", "Media", "Alta"])
            
        if st.button("Salva Attività", use_container_width=True):
            if t_name:
                new_task = pd.DataFrame([[t_name, t_date.strftime("%Y-%m-%d"), t_prior, "In Corso"]], columns=["Task", "Scadenza", "Priorità", "Stato"])
                t_df = pd.concat([t_df, new_task], ignore_index=True)
                save_csv(t_df, "todo")
                st.toast("Attività registrata correttamente!", icon="💾")
                st.rerun()

    st.markdown("### 📋 Elenco Attività Correnti")
    if t_df.empty:
        st.info("Nessuna attività programmata al momento.")
    else:
        for idx, row in t_df.iterrows():
            col_t, col_p, col_a, col_e = st.columns([3, 1, 1, 1])
            with col_t:
                if row["Stato"] == "Completato":
                    st.markdown(f"~~{row['Task']}~~  *(Scadenza: {row['Scadenza']})*")
                else:
                    st.markdown(f"**{row['Task']}** *(Scadenza: {row['Scadenza']})*")
            with col_p:
                p_emoji = "🔴" if row["Priorità"] == "Alta" else ("🟡" if row["Priorità"] == "Media" else "🟢")
                st.markdown(f"{p_emoji} {row['Priorità']}")
            with col_a:
                if row["Stato"] == "In Corso":
                    if st.button("Spunta", key=f"check_{idx}", type="primary", use_container_width=True):
                        t_df.at[idx, "Stato"] = "Completato"
                        save_csv(t_df, "todo")
                        st.rerun()
                else:
                    st.caption("Eseguito 🎉")
            with col_e:
                if st.button("Elimina", key=f"del_t_{idx}", use_container_width=True):
                    t_df = t_df.drop(idx)
                    save_csv(t_df, "todo")
                    st.rerun()


# AREA 3: AGENDA DIGITALE
elif menu == "📅 Agenda Digitale":
    st.header("📅 Vista Calendario", divider="blue")
    st.caption("Mappatura visiva automatica delle scadenze basata sulle tue attività.")
    
    t_df = load_csv("todo")
    events = []
    
    for idx, row in t_df.iterrows():
        color_map = "#ef4444" if row["Priorità"] == "Alta" else ("#f59e0b" if row["Priorità"] == "Media" else "#10b981")
        if row["Stato"] == "Completato": color_map = "#6b7280"
        
        events.append({
            "title": f"[{row['Priorità']}] {row['Task']}",
            "start": row["Scadenza"],
            "end": row["Scadenza"],
            "backgroundColor": color_map,
            "borderColor": color_map
        })
        
    cal_options = {
        "headerToolbar": {"left": "today prev,next", "center": "title", "right": "dayGridMonth,timeGridWeek"},
        "initialView": "dayGridMonth",
        "selectable": True
    }
    
    calendar(events=events, options=cal_options)


# AREA 4: SMART NOTES
elif menu == "📝 Note":
    st.header("📝 Blocco Note Digitale", divider="orange")
    st.caption("Crea, cataloga e organizza i tuoi pensieri.")
    
    n_df = load_csv("notes")
    col_input, col_view = st.columns([1, 1.3])
    
    with col_input:
        st.markdown("### 📥 Nuova Annotazione")
        n_title = st.text_input("Titolo Nota:")
        n_content = st.text_area("Contenuto / Dettagli:", height=180)
        
        if st.button("Archivia Nota", use_container_width=True):
            if n_title and n_content:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                new_note = pd.DataFrame([[n_title, n_content, timestamp]], columns=["Titolo", "Contenuto", "Data"])
                n_df = pd.concat([n_df, new_note], ignore_index=True)
                save_csv(n_df, "notes")
                st.toast("Nota inserita nello schedario!", icon="💾")
                st.rerun()
                
    with col_view:
        st.markdown("### 📂 Note Schedulate")
        if n_df.empty:
            st.info("Nessuna nota salvata nell'archivio locale.")
        else:
            for idx, row in n_df.iterrows():
                st.markdown(f"""
                <div class="custom-note">
                    <h4 style='margin:0 0 8px 0; color:#f3f4f6;'>📌 {row['Titolo']}</h4>
                    <p style='margin:0 0 10px 0; color:#d1d5db; font-size:14px; white-space: pre-wrap;'>{row['Contenuto']}</p>
                    <small style='color:#9ca3af;'><i>Registrato: {row['Data']}</i></small>
                </div>
                """, unsafe_allow_html=True)
                # RIMOSSO IL PARAMETRO size="small" CHE GENERAVA L'ERRORE NELLA FOTO
                if st.button("Elimina Nota", key=f"del_n_{idx}", use_container_width=True):
                    n_df = n_df.drop(idx)
                    save_csv(n_df, "notes")
                    st.rerun()


# AREA 5: FOCUS TIMER (POMODORO)
elif menu == "⏱️ Focus Timer (Pomodoro)":
    st.header("⏱️ Focus Timer", divider="green")
    st.caption("Fissa una sessione di lavoro continuo senza distrazioni.")
    
    col_timer, col_info = st.columns([1, 1])
    
    with col_timer:
        st.markdown("### ⏳ Avvia Sessione")
        timer_duration = st.slider("Seleziona Minuti Sessione:", min_value=1, max_value=60, value=25)
        
        if st.button("🚀 Inizia Conto alla Rovescia", use_container_width=True):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            total_seconds = timer_duration * 60
            for i in range(total_seconds):
                time.sleep(1)
                pct_complete = int(((i + 1) / total_seconds) * 100)
                progress_bar.progress(pct_complete)
                
                mins_left = (total_seconds - i - 1) // 60
                secs_left = (total_seconds - i - 1) % 60
                # Sostituito il blocco metriche/omini con testo standard pulito
                status_text.markdown(f"<h2 style='text-align: center; color: #10b981;'>Tempo Rimanente: {mins_left:02d}:{secs_left:02d}</h2>", unsafe_allow_html=True)
                
            st.balloons()
            st.success("🎉 Sessione Completata! Fai una breve pausa.")
            
    with col_info:
        st.markdown("""
        ### 💡 Come funziona?
        1. Scegli un'attività da portare a termine.
        2. Avvia il timer (consigliati 25 minuti).
        3. Lavora concentrato al massimo finché il tempo non scade.
        """)


# AREA 6: IMPOSTAZIONI & REPORT
elif menu == "📊 Impostazioni":
    st.header("📊 Statistiche & Configurazione", divider="red")
    st.caption("Modifica le tue preferenze ed esamina l'andamento delle attività.")
    
    m_df = load_csv("mood")
    t_df = load_csv("todo")
    
    tab_profile, tab_mood, tab_charts, tab_system = st.tabs(["👤 Profilo Utente", "🧠 Mood Journal", "📈 Report Grafici", "⚙️ Gestione Sistema"])
    
    with tab_profile:
        st.markdown("### ⚙️ Impostazioni Identità Semplificate")
        new_user = st.text_input("Nome Utente visualizzato:", value=username)
        new_bio = st.text_input("Breve descrizione / Bio:", value=user_bio)
        
        if st.button("Salva Impostazioni Profilo"):
            prof_df = pd.DataFrame([[new_user, new_bio]], columns=["Username", "Bio"])
            save_csv(prof_df, "profile")
            st.success("Profilo aggiornato con successo!")
            st.rerun()
            
    with tab_mood:
        st.markdown("### 💭 Diario Emotivo dell'Umore")
        current_mood = st.select_slider(
            "Indica il tuo livello di energia mentale attuale:",
            options=["Livello Minimo 🥱", "Sottotono 😐", "Stabile / Neutro 🙂", "Ottimo Focus 🚀", "Massima Energia 🔥"]
        )
        mood_notes = st.text_input("Note opzionali sui tuoi pensieri attuali:")
        
        if st.button("Registra Stato Odierno"):
            today_str = datetime.date.today().strftime("%Y-%m-%d")
            if not m_df.empty and today_str in m_df["Data"].values:
                m_df.loc[m_df["Data"] == today_str, ["Mood", "Note"]] = [current_mood, mood_notes]
            else:
                new_m_row = pd.DataFrame([[today_str, current_mood, mood_notes]], columns=["Data", "Mood", "Note"])
                m_df = pd.concat([m_df, new_m_row], ignore_index=True)
            save_csv(m_df, "mood")
            st.success("Stato d'animo archiviato correttamente!")
            st.rerun()

    with tab_charts:
        st.markdown("### 📈 Visualizzazione Grafica della Produttività")
        if t_df.empty and m_df.empty:
            st.info("Inserisci dei task o registra il tuo mood per visualizzare l'analisi statistica in tempo reale.")
        else:
            cg1, cg2 = st.columns(2)
            with cg1:
                if not t_df.empty:
                    fig_p = px.pie(t_df, names="Stato", title="Rapporto Task Eseguiti vs In Corso", color_discrete_sequence=["#4f46e5", "#10b981"])
                    st.plotly_chart(fig_p, use_container_width=True)
            with cg2:
                if not m_df.empty:
                    fig_l = px.line(m_df, x="Data", y="Mood", title="Andamento dei Livelli di Energia nel Tempo", markers=True, line_shape="spline")
                    fig_l.update_traces(line_color='#7c3aed')
                    st.plotly_chart(fig_l, use_container_width=True)

    with tab_system:
        st.markdown("### 💾 Esportazione Dati e Ripristino")
        st.download_button(label="📥 Scarica Report Task (CSV)", data=t_df.to_csv(index=False), file_name="backup_tasks.csv", mime="text/csv")
        
        st.markdown("---")
        if st.button("⚠️ Ripristina Stato di Fabbrica (Cancella tutto)", type="primary"):
            for f in FILES.values():
                if os.path.exists(f): os.remove(f)
            st.warning("Tutti i dati memorizzati localmente sono stati rimossi.")
            st.stop()