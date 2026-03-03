# Import
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

ItemDaCercare = "One Piece"
NumeroPagine = 3


# Apro chrome
driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://www.lafeltrinelli.it/")

wait = WebDriverWait(driver, 20)

# Chiudo popup cookie se presente
try:
    cookie_btn = wait.until(
        EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
    )
    cookie_btn.click()
except:
    pass

# Cerco TUTTI gli input con id inputSearch
inputs = wait.until(
    EC.presence_of_all_elements_located((By.ID, "inputSearch"))
)

# Prendo solo quello visibile
barra_ricerca = None
for inp in inputs:
    if inp.is_displayed():
        barra_ricerca = inp
        break

if barra_ricerca is None:
    print("Nessuna barra visibile trovata")
    driver.quit()
    exit()

# Scrivo e premo invio
barra_ricerca.send_keys(ItemDaCercare)
barra_ricerca.send_keys(Keys.ENTER)

# Attendo caricamento risultati
wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))

print("Ricerca item completata")

# ----------------------------------------------------------------------------------------------------------------
# Salvo lista completa prodotti pagina
# Cerco nel contenitore i vari prodotti e li divido in una lista per prodotto
# Estraggo il contenitore del prezzo e del nome per ogni prodotto nella lista
# Dal contenitore estraggo il testo del prezzo e del nome

dati = []
i = 0
while i < NumeroPagine: 
    wait.until(EC.presence_of_element_located((By.XPATH, "//ul[@class='cc-listing-items']")))
    print("Contenitore prodotti trovato")
    ContenitoreListaProdotti = driver.find_element(By.XPATH, "//ul[@class = 'cc-listing-items']")

    wait.until(EC.presence_of_element_located((By.XPATH, "//li[contains(@class,'cc-product-list-item')]")))
    ListaProdotti = ContenitoreListaProdotti.find_elements(By.XPATH, ".//li[@class='cc-product-list-item']")
    print("Numero prodotti trovati:", len(ListaProdotti))
    
    for prodotto in ListaProdotti:
        
        ContenitoreTitoloItem = WebDriverWait(prodotto, 5).until(
                lambda x: x.find_element(By.XPATH, ".//a[contains(@class,'cc-title')]"))
        Titolo = ContenitoreTitoloItem.text
        print(Titolo)

        ContenitorePrezzoItem = prodotto.find_element(By.XPATH, ".//span[contains(@class,'cc-price')]")
        Prezzo = ContenitorePrezzoItem.text


    # Inserisco titolo e prezzo nella lista dati

        dati.append({
                        "Titolo": Titolo,
                        "Prezzo": Prezzo
                    })
    PaginaSuccessiva = driver.find_element(By.XPATH, "//a[@class='cc-pagination-direct cc-pagination-next']")
    PaginaSuccessiva.click()
    i+=1
    
# Trasformo la lista in un data frame 

TabellaItem = pd.DataFrame(dati)
TabellaItem.to_excel("Estrazione_OnePiece.xlsx", index=False)

