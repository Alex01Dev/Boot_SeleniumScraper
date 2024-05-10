#para instalar automaticamente chromedriver
from webdriver_manager.chrome import ChromeDriverManager
#driver de selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
#para modificar las opciones de webdriver en chrome
from selenium.webdriver.chrome.options import Options
#para definir el tipo de busqueda del elemento
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait #para esperar por los elementos de selenium
from selenium.webdriver.support import expected_conditions as ec # para condiciones en selenium
from selenium.common.exceptions import TimeoutException #excepcion de timeout en selenium
from selenium.webdriver.common.keys import Keys #para pulsar teclas especiales (ej: AvPág)
from config_instagram import * #importar las credenciales de instagram
import time
import sys
import pickle #para cargar/guardar las cookies
import os
import wget #para descargar archivos


def cursor_arriba(n=1):
    #Sube el cursosr n veces
    print(f'\033[{n}A', end="")

def raya():
    #Escribe tantos guiones como ancha es la terminal
    print('-'*os.get_terminal_size().columns)


def init_chrome():
    ruta_chromedriver = ChromeDriverManager().install()
    s = Service(ruta_chromedriver)
    options = Options(); #instanciamos las opciones de Chrome
    user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36",
    #options.add_argument("--headless=new") #ejecutar chrome sin abrir la ventana
    options.add_argument(f"user-agent={user_agent}") #define un user agent personalizado
    options.add_argument("--window-size=970,1080") #para configurar el alto y ancho de ventana
    options.add_argument("--disable-web-security")#desahabilita la politica del mismo origen o Same Origin Policy
    options.add_argument("--disable-extensions") #para que no cargue las extensiones de chrome
    #options.add_argument("--disable-notifications") #para bloquear las notificaciones de chrome
    options.add_argument("--ignore-certificate-errors") #para ignorar el aviso de "Su conexion no es privada"
    options.add_argument("--no-sandbox") #deshabilita el modo sanbox
    options.add_argument("--allow-running-insecure-content") # desactiva el aviso de "contenido no seguro"
    options.add_argument("--no-default-browser-check") #Evita el aviso de que Chrome no es el navegador por defecto
    options.add_argument("--no-first-run") # evita la ejecucion de ciertas tareas que sea realizan la primera vez que se ejecute Chrome
    options.add_argument("--no-proxy-server") #para no usar proxy, sino conexiones directas
    options.add_argument("--disable-blink-features=AutomationControlled") # evita que selenium sea detectado en el navegador, quitamos un filtro de deteccion de bot

    #PARAMETROS A OMITIR EN EL INICIO DE CHROMEDRIVER
    exp_opt = [

        'enable-automation', #para que no se muestre la notificacion "Un Software automatizado de pruebas esta controlado chrome"
        'ignore-certificate-errors', #para ignorar errores de certificados (a veces estan caducados)
        'enable-logging' #para que no se muestre en la terminal "DevTools listening on...."
        ]

    options.add_experimental_option("excludeSwitches", exp_opt) #recibe una lista, no un diccionario

    #PARAMETROS QUE DEFINEN PREFERENCIAS DE CHROMEDRIVER
    prefs = {
        "profile.default_content_setting_values.notifications": 2, #notificaiones:0=preguntar|1=permitir|2=no permitir
        "intl.accept_languages": ["es-ES", "es"], #para definir el idioma del navegador
        "credentials_enable_service": False #para evitar que el Chrome nos pregunte si queremos guardar la contraseña al loguearnos

        }
    options.add_experimental_option("prefs", prefs) #no recibe una lista, si no un diccionario

    s= Service(ruta_chromedriver)
    driver = webdriver.Chrome(service=s, options=options)
    driver.set_window_position(0,0)

    return driver

#FUNCION PARA LOGIN EN INSTAGRAM

def login_instagram():
    #Realiza login en Instagram, si es posible por cookies y si no desde cero

    #Comprobamos si existe el archivo  de cookies
    # print("Login en INSTAGRAM por cookies");
    # if os.path.isfile("instagram.cookies"):
    #     cookies = pickle.load(open,("instagram.cookies", "rb")) #leer archivo en modo lectura binaria
    #     #cargamos robots.txt del dominio instagram.com
    #     driver.get("https://www.instagram.com/robots.txt")
    #     #Recorremos el objeto cookies y la añadimos al driver
    #     for cookie in cookies:
    #         driver.add_cookie(cookie)
    #     #Comprobamos si el login por cookies funciona
    #     driver.get("https://www.instagram.com/")
    #     try:
    #         elemento = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, "article")))
    #         print(" LOGIN POR COOKIES: OK")
    #     except:
    #         print(' ERROR: El feed de noticias no se ha cargado')
    #     return "ERROR"
    
    #abrimos pagina desde instagram
    print('Login en INSTAGRAM desde CERO')
    driver.get("https://www.instagram.com/")
    #Esperemos que este disponible el boton de 'Permitir Cookies'
    #elemento = driver.find_element(By.XPATH, "//button[contains(text(), 'Permitir cookies')]")
    #para que haga click en el boton
    #elemento.click();
    #PARA PODER ESCRIBIR TEXTO EN UN CONTENEDOR
    #forma para ingresar los elementos rapido sin tiempo de esperar para ingresar
    #elemento = driver.find_element(By.NAME, "username")
    #elemento = driver.find_element(By.NAME, "password")

    try:
        #la funcion va espera hasta que elemento exista
        elemento = wait.until(ec.visibility_of_element_located((By.NAME, "username"))) #metodo recibe un argumento, el cual es la condicion que se tiene que cumplir para finalizar la espera
    except TimeoutException:
        print('ERROR: Elemento "username" no disponible')
        return "ERROR"
    elemento.send_keys(USER_IG); #ELEMENTO PARA ESCRIBIR
    elemento = wait.until(ec.visibility_of_element_located((By.NAME, "password")))
    elemento.send_keys(PASS_IG)
    elemento = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))) #se busca el boton para dar clic por el tipo de boton que es
    #elemento =  wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, "password")))
    elemento.click();
    #forma para que de clic en lugar de buscar por el type si no por el texto que debe coincidir para que los busque utilizando xpath
    #elemento = wait.until(ec.visibility_of_element_located((By.XPATH, "//div[contains(text(), 'Iniciar')]")))
    #elemento = wait.until(ec.element_to_be_clickable((By.XPATH, "//button[text()='Guardar información']")))
    #elemento.click();
    try:
        elemento = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, "article")))
        print(" LOGIN DESDE CERO: OK")
    except:
        print(' ERROR: El feed de noticias no se ha cargado')
        return "ERROR"
    #Guardamos las cookies
    # cookies = driver.get_cookie()
    # pickle.dump(cookies, open("instagram.cookies", "wb"))#objeto que queremos guardar, archivo donde queremos guardalos, modo de apertura escrituraBinario
    # print("     Cookies Guardadas:)")
    # return "OK"

#MAIN
if __name__ == '__main__':
    #Modo de uso de la manera de usar el programa 
    modo_de_uso = f'Modo de uso:\n'
    modo_de_uso += f' {os.path.basename(sys.executable)} {sys.argv[0]} hashtag [minimo]\n\n' #indicar que el usuario que aqui va el hasgtag de las fotos que quiero, igual si quieres el minimo de fotos
    modo_de_uso += f'   opciones: \n'
    modo_de_uso += f'       minimo : Minimo de descargars a realizar (por defecto 300)\n\n'
    modo_de_uso += f'Ejemplos: \n'
    modo_de_uso += f'   {os.path.basename(sys.executable)} {sys.argv[0]} cats\n'
    modo_de_uso += f'   {os.path.basename(sys.executable)} {sys.argv[0]} superman 100\n'

    #FUNCION PARA DESCARGAR FOTOS EN INSTAGRAM
    def descargar_fotos_instagram(hashtag,minimo):
        #Descargar las fotos del hashtag indicado
        #Realizamos la peticion
        print(f'Buscando por hashtag #{hashtag}')
        driver.get(f'https://www.instagram.com/explore/tags/{hashtag}')
        
        #1.-elemento = driver.find_element(By.CSS_SELECTOR, "html")

        url_fotos = set() #conjunto vacio en el que iremos añadiendo los enlaces de las fotos

        #Realizamos Scroll de la pagina
        while len(url_fotos) < minimo: #con la primer version es con for y es for n in range(30)
            #1.-elemento.send_keys(keys.PAGE_DOWN)
            #Realizar scroll con javascript
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            # 1.- time.sleep(0.5)
            elementos = driver.find_elements(By.CSS_SELECTOR, 'div._aagv')
            #recorremos los elementos encontramos y añadimos las url de las fotos al conjunto
            for elemento in elementos:
                try:
                    url = elemento.find_element(By.CSS_SELECTOR, "img").get_attribute("src")
                    url_fotos.add(url)
                except:
                    pass
            print(f'    Total Fotos: {len(url_fotos)}')
            cursor_arriba();
        #crear una carpeta para que ahi se descarguen las fotos con el nombre de la carpeta
        #si no existe la carpeta la creamos
        if not os.path.exists(hashtag):
            os.mkdir(hashtag)
        #Descargamos las fotos del conjunto
        n = 0; #numero de foto en curso
        for url_foto in url_fotos:
            n+=1
            print(f'    Descargando {n} de {len(url_fotos)}')
            nombre_del_archivo = wget.download(url_foto, hashtag); #enlace de descarga, la carpeta donde descargarla
            cursor_arriba();
            print(f'\33[K descargado {nombre_del_archivo}')
            print()
        return len(url_fotos);



    #CONTROL DE PARAMETROS
    if len(sys.argv) == 1 or len(sys.argv) > 3: #si el numero de arg que se pasan al programa es 1 o si el numero de argv es mayor que 3
        print(modo_de_uso)
        sys.exit(1)
    elif len(sys.argv) == 3: #numero de argv sea 3 tanto como puso el hasghtag y la cantidad
        if sys.argv[2].isdigit(): #si al parametro que es el minimo, isdigit: metodo de string que indica si todo el contenido es un numero
            MINIMO = int(sys.argv[2]) #constante minimo que convertimos el string en entero
        else:
            print(f'ERROR: {sys.argv[2]} no es un numero')
            sys.exit(1);
    else: #en caso del que usuario solo haya indicado el hasghtag y no el minimo de fotos
        MINIMO = 300 
    HASHTAG = sys.argv[1].strip('#') #en caso de que el usuario indico el hashtag con el # se lo quitamos

    #iniciamos selenium
    driver = init_chrome();
    #Configuramos el tiempo de espera para cargar los elementos
    wait = WebDriverWait(driver, 10); #Tiempo de espera hasta que el elemento esta disponible, tiempo maximo de espera
    #nos logueamos en instagram
    res = login_instagram();
    time.sleep(9)
    #por si se produce un error en el login
    if res == "ERROR":
        input("Pulsa ENTER para salir...") #pausa para estudiar el error
        driver.quit();
        sys.exit(1) #salir del programa
    raya()
    time.sleep(5)
    #Descargar las fotos del hashtag y minimo
    res = descargar_fotos_instagram(HASHTAG, MINIMO)
    print(f'Se han descargado {res} fotos.....')
    raya();
    input("Pulsa ENTER para salir"); 
    driver.quit();

#HACER FUNCION RANDOM para los tiempos