import requests 
from bs4 import BeautifulSoup 
import pandas as pd 


def get_curva_cupon_cero(tipoCurva=None,fechaProceso=None,tramoCorto=False):

    URL = "https://www.sbs.gob.pe/app/pu/CCID/Paginas/cc_unacurva.aspx" 
        
    with requests.Session() as req:
        r = req.get(URL) 
        soup = BeautifulSoup(r.content, 'html.parser') 

        vs = soup.find("input", id="__VSTATE").get("value")
        ev_val = soup.find("input", id="__EVENTVALIDATION").get("value")

        data = {
                '__EVENTTARGET': 'cboTipoCurva',
                '__EVENTARGUMENT': '',
                '__LASTFOCUS': '',
                '__VSTATE': vs,
                '__VIEWSTATE': '',     

                '__SCROLLPOSITIONX':'0',
                '__SCROLLPOSITIONY':'100',

                '__EVENTVALIDATION':ev_val,
                'cboTipoCurva': tipoCurva
            }
        r = req.post(URL, data=data)
        soup_post_t_curv = BeautifulSoup(r.content, 'html.parser')

        vs = soup_post_t_curv.find("input", id="__VSTATE").get("value")
        ev_val = soup_post_t_curv.find("input", id="__EVENTVALIDATION").get("value")

        data = {
                '__EVENTTARGET': '',
                '__EVENTARGUMENT': '',
                '__LASTFOCUS': '',
                '__VSTATE': vs,
                '__VIEWSTATE': '',     

                '__SCROLLPOSITIONX':'0',
                '__SCROLLPOSITIONY':'64',

                '__EVENTVALIDATION':ev_val,
                'cboTipoCurva': tipoCurva,
                'cboFechas':fechaProceso,           
                'btnConsultar':"Consultar"
            }
        
        if tramoCorto:
            data["chkTramoCorto"] = "on"

        r = req.post(URL, data=data)
        soup_post_result = BeautifulSoup(r.content, 'html.parser')

        tablaCab = soup_post_result.find('table', {'id': 'tablaDetalle'})

        thead = tablaCab.find('thead')    
        lista_columnas = []

        for fila in thead.find_all('tr'):
            celdas = fila.find_all('th',{'class':'APLI_cabeceraTabla2'})
            datos_columna = [celda.text.strip() for celda in celdas]
            if len(datos_columna)>0:
                lista_columnas = datos_columna

        tablaCuerpo = soup_post_result.find('table', {'id': 'tablaCuerpo'})
        tbody = tablaCuerpo.find('tbody')
        datos_tabla = []
        # Iterar sobre las filas de la tabla
        for fila in tbody.find_all('tr'):
            # Obtener los datos de cada celda en la fila
            celdas = fila.find_all('td')
            datos_fila = [celda.text.strip() for celda in celdas]    
            datos_tabla.append(datos_fila)  


        df = pd.DataFrame(datos_tabla, columns=lista_columnas)

        return df    
