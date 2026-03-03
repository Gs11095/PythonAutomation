from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# Avvia browser
driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://www.lafeltrinelli.it/")

wait = WebDriverWait(driver, 20)

# Chiudi popup cookie se presente
try:
    cookie_btn = wait.until(
        EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
    )
    cookie_btn.click()
except:
    pass

# Trova TUTTI gli input con id inputSearch
inputs = wait.until(
    EC.presence_of_all_elements_located((By.ID, "inputSearch"))
)

# Prendi solo quello visibile
barra_ricerca = None
for inp in inputs:
    if inp.is_displayed():
        barra_ricerca = inp
        break

if barra_ricerca is None:
    print("Nessuna barra visibile trovata")
    driver.quit()
    exit()

# Scrivi e premi invio
barra_ricerca.send_keys("One Piece")
barra_ricerca.send_keys(Keys.ENTER)

#  Attendi caricamento risultati
wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))

print("Ricerca completata!")

# Salvo lista completa prodotti pagina
# Cerco nel contenitore i vari prodotti e li divido in una lista per prodotto
# Estraggo il contenitore del prezzo e del nome per ogni prodotto nella lista
# Dal contenitore estraggo il testo del prezzo e del nome
 
ContenitoreListaProdotti = driver.find_element(By.XPATH, "//ul[@class = 'cc-listing-items']")
ListaProdotti = ContenitoreListaProdotti.find_elements(By.XPATH, "//li[@class='cc-product-list-item']")

dati = []

for prodotto in ListaProdotti:
    
    ContenitoreTitoloItem = prodotto.find_element(By.XPATH, "//a[@class='cc-title']")
    Titolo = ContenitoreTitoloItem.text

    ContenitorePrezzoItem = prodotto.find_element(By.XPATH, "//span['cc-price']")
    Prezzo = ContenitorePrezzoItem.text

# Inserisco titolo e prezzo nella lista dati

    dati.append({
                    "Titolo": Titolo,
                    "Prezzo": Prezzo
                })
    
# Trasformo la lista in un data frame 

TabellaItem = pd.DataFrame(dati)
TabellaItem