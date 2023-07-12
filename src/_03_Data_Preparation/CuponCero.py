from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import pandas as pd
# Configurar Selenium

options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)  # Cambia esto al controlador de navegador que estés utilizando (por ejemplo, Firefox)


# Cargar la página
url = 'https://www.sbs.gob.pe/app/pu/CCID/Paginas/cc_unacurva.aspx'  # Reemplaza con la URL real
driver.get(url)

lista_cboTipoCurva = Select(driver.find_element(By.ID,'cboTipoCurva'))  # Reemplaza 'id_de_la_lista' con el ID real de la lista desplegable
lista_cboTipoCurva.select_by_visible_text('Curva Cupon Cero Peru Soles Soberana') 

lista_cboFechas = Select(driver.find_element(By.ID,'cboFechas')) 
lista_cboFechas.select_by_visible_text('11/07/2023') 

btnConsultar = driver.find_element(By.ID,'btnConsultar')  # Reemplaza 'id_del_boton' con el ID real del botón
btnConsultar.click()

# Obtener el contenido después de hacer clic en el botón
contenido_html = driver.page_source

# Utilizar BeautifulSoup para analizar el contenido HTML
soup = BeautifulSoup(contenido_html, 'html.parser')

# Encontrar la tabla por su ID
tabla = soup.find('table', {'id': 'tablaCuerpo'})

# Encontrar el cuerpo de la tabla
tbody = tabla.find('tbody')


datos_tabla = []
# Iterar sobre las filas de la tabla
for fila in tbody.find_all('tr'):
    # Obtener los datos de cada celda en la fila
    celdas = fila.find_all('td')
    datos_fila = [celda.text.strip() for celda in celdas]
    datos_tabla.append(datos_fila)   
    # Hacer algo con los datos de la fila
    # ...

cls = ["Sec.","Fecha de Proceso","Periodo (días)","Tasas (%)"] 

# Crear un DataFrame utilizando pandas
df = pd.DataFrame(datos_tabla,columns=cls)


# Cerrar el navegador
driver.quit()

df.head()