from flask import Flask, jsonify, request
import os
from openai import OpenAI
from diagnose import diagnostica_acidosi_metabolica
from dotenv import load_dotenv

# Carica le variabili d'ambiente dal file .env
load_dotenv()

# Inizializza il client OpenAI
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Recupera l'assistant
assistant = client.beta.assistants.retrieve("asst_Fyhh8BRuuABdapoqsxjGbZFR")

app = Flask(__name__)

@app.route('/')
def ricevi_messaggio():
    # Ottieni i parametri come stringhe
    pH_str = request.args.get('pH')
    pCO2_str = request.args.get('pCO2')
    HCO3_str = request.args.get('HCO3')

    # Stampa i parametri per il debug
    print(f"Ricevuto pH: {pH_str}, pCO2: {pCO2_str}, HCO3: {HCO3_str}")

    # Converti i parametri in float
    try:
        pH = float(pH_str)
        pCO2 = float(pCO2_str)
        HCO3 = float(HCO3_str)
    except (TypeError, ValueError) as e:
        return jsonify({'errore': 'Parametri non validi o mancanti'}), 400

    # Calcola la diagnosi
    diagnosi = diagnostica_acidosi_metabolica(pH, HCO3, pCO2)

    # Crea un nuovo thread OpenAI
    empty_thread = client.beta.threads.create()

    # Invia il messaggio al thread
    message = client.beta.threads.messages.create(
        thread_id=empty_thread.id,
        role="user",
        content="E' stata effettuata un'analisi del sangue di un animale. I valori di pH, HCO3- e pCO2 sono i seguenti: pH = " + str(pH) + ", HCO3- = " + str(HCO3) + ", pCO2 = " + str(pCO2) + ". La diagnosi che ho fatto è la seguente: " + diagnosi + ". Secondo te è corretta?"
    )

    # Esegui l'assistant
    run = client.beta.threads.runs.create_and_poll(
        thread_id=empty_thread.id,
        assistant_id=assistant.id,
        instructions="Stai parlando con un veterinario in cerca di conferma per una diagnosi importante, cerca di andare al sodo e non dare risposte troppo lunghe. Se non sei sicuro di una diagnosi, non darla."
    )

    # Ottieni la risposta dell'assistant
    assistant_response = ""
    if run.status == 'completed':
        messages = client.beta.threads.messages.list(
            thread_id=empty_thread.id
        )
        assistant_response = messages.data[0].content[0].text.value
    else:
        assistant_response = f"Errore: {run.status}"

    # Restituisce un JSON con i valori ricevuti, la diagnosi e la risposta dell'assistant
    return jsonify({
        'ph': pH,
        'pco2': pCO2,
        'hco3': HCO3,
        'diagnosi': diagnosi,
        'assistant_response': assistant_response
    })

if __name__ == "__main__":
    app.run(host='localhost', port=5000)
