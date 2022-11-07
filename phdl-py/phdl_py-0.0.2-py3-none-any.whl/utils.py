import re
import ffmpeg
import requests
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By

from .configlogger import setup_logger
logger = setup_logger()


NAME_DIR = "./pornhub"
ELEMENTS_PSTAR = '//a[contains(@class, "pstar-list-btn")]'
NAME_PSTAR = '//div[@class="userInfo"]//a[@class="bolded"]'


def setup_driver() -> webdriver:
    logger.info("Open Chrome Service Web Driver.")
    service = ChromeService("/usr/bin/chromedriver")
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    options.add_argument("--headless")

    driver = webdriver.Chrome(service=service, options=options)

    return driver


def get_url_m3u8(driver: webdriver, url: str) -> str:
    logger.info(f"Get info page...")

    try:
        driver.get(url)
    except:
        logger.exception("An error occurred while making the request.")

    lista_m3u8 = []
    for i in range(10):
        try:
            lista_m3u8.append(driver.execute_script(f'return media_{i}'))
        except:
            break

    direcciones = []
    for item in lista_m3u8:
        if "1080P" in item and not "urlset" in item:
            direcciones.append((1080, item))
        elif "720P" in item and not "urlset" in item:
            direcciones.append((720, item))
        elif "480P" in item and not "urlset" in item:
            direcciones.append((480, item))

    direcciones.sort(reverse=True)
    first_m3u8_url = direcciones[0][1]

    response = requests.get(first_m3u8_url)
    sufix = response.content.decode('utf-8').split("\n")[2]
    second_m3u8_url = re.sub('master.*', sufix, first_m3u8_url)

    return second_m3u8_url


def get_name(driver: webdriver) -> str:
    elements = driver.find_elements(by=By.XPATH, value=ELEMENTS_PSTAR)
    name = ""

    if elements:
        for element in elements:
            name += f"{element.text}-"
    else:
        name = driver.find_element(by=By.XPATH, value=NAME_PSTAR).text
        name += "-"

    return name.replace(" ", "_")


def get_info_video(filename: Path) -> str:
    video_resolution = ffmpeg.probe(filename)["streams"][0]["height"]
    video_size = filename.stat().st_size / 1024 ** 2
    return f"Video Resolution: {video_resolution}p\tVideo Size : {video_size:.2f} MB\n"


def download_m3u8_to_mp4(url_m3u8: str, filename: Path, overwrite: bool) -> None:

    # Verificamos si el archivo no existe para descargarlo
    if not filename.exists() or overwrite:
        logger.info(f"Download video: {str(filename)}")
        # Definimos la tarea de descarga mediante ffmpeg
        stream = ffmpeg.input(url_m3u8).output(str(filename.absolute()),
                                               codec="copy",
                                               loglevel="quiet")
        try:
            # Si el archivo existe, y además queremos sobreescribirlo.
            if filename.exists() and overwrite:
                logger.warning(f"Overwrite: {str(filename)}")

            # Intentamos ejecutar la tarea de descarga
            stream.run(capture_stderr=True, overwrite_output=overwrite)

        except ffmpeg._run.Error as e:
            # Si existe un error, lo imprime en pantalla
            print(f"STDOUT:\t{e.stdout}")
            print(f"STDERR:\t{e.stderr}")
    else:
        # Si existe el archivo y no queremos sobreescribirlo, lo saltamos
        logger.warning(f"SKIP! {filename} was already downloaded.")

    # Imprimimos la resolución y el tamaño del archivo
    logger.info(get_info_video(filename))
