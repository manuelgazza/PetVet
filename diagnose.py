def diagnostica_acidosi_metabolica(pH, HCO3, pCO2):
    # Valori di riferimento
    HCO3_rif = 27.0  # Valore di riferimento per HCO3- in mmol/L
    pCO2_rif = 47.0  # Valore di riferimento per pCO2 in mmHg

    diagnosi = ""

    print("IN DIAGNOSI")

    # Controllo iniziale per Acidosi Metabolica Semplice
    if pH < 7.40 and HCO3 < HCO3_rif:
        delta_HCO3 = HCO3_rif - HCO3  # Diminuzione di HCO3- rispetto al valore di riferimento
        delta_pCO2_attesa = delta_HCO3 * 1.2  # Diminuzione attesa di pCO2 per compensazione
        pCO2_compensata = pCO2_rif - delta_pCO2_attesa  # Valore atteso di pCO2 compensata

        # Definizione del range compensato (dal valore compensato meno 4 mmHg al valore compensato)
        range_compensato_min = pCO2_compensata - 4
        range_compensato_max = pCO2_compensata

        # Calcolo della diminuzione reale di pCO2
        delta_pCO2_reale = pCO2_rif - pCO2

        # Calcolo della diminuzione per mmol/L di HCO3-
        if delta_HCO3 != 0:
            diminuzione_per_mmol = delta_pCO2_reale / delta_HCO3
        else:
            diminuzione_per_mmol = 0

        # Determinazione della diagnosi
        if 43 <= pCO2 <= 47:
            diagnosi = "Acidosi Metabolica Semplice"
        elif range_compensato_min <= pCO2 <= range_compensato_max:
            diagnosi = "Acidosi Metabolica Compensata"
        elif diminuzione_per_mmol > 1.2:
            diagnosi = "Disturbo Misto con Acidosi Metabolica e Alcalosi Respiratoria"
        else:
            diagnosi = "Risultati non conclusivi, richiede ulteriore valutazione"
    else:
        diagnosi = "I valori inseriti non soddisfano i criteri per un'Acidosi Metabolica secondo la definizione iniziale."

    return diagnosi


