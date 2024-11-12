from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import time
import os

load_dotenv()

class MHRS:

    MHRS_URL = "https://mhrs.gov.tr/vatandas/#/"

    # mhrs giris sayfası
    CLASSES_BTN_E_DEVLET_ILE_GIRIS = "ant-btn login-form-button login-button edevlet-btn ant-btn-default ant-btn-block"

    # e devlet ile giriş yap sayfası
    ID_OF_E_DEVLET_ILE_GIRIS_YAP_TCNO_INPUT = "tridField"
    ID_OF_E_DEVLET_ILE_GIRIS_YAP_PASSWORD_INPUT = "egpField"
    CLASSES_OF_E_DEVLET_ILE_GIRIS_YAP_BUTTON = "btn btn-send"

    # mhrs islemler sayfası
    CLASSES_OF_HASTANE_RANDEVUSU_AL_BUTTON = "ant-card randevu-card hasta-randevu-card mb-16 mr-16"
    CLASSES_OF_GENEL_ARAMA_BUTTON = "ant-btn randevu-turu-button genel-arama-button ant-btn-lg"
    CLASSES_OF_TANI_MODAL_BODY = "ant-modal-body"
    CLASSES_OF_TANI_MODAL_KAPAT_BUTTON = "ant-btn"

    TC_NO = os.getenv("TC_NO")
    PASSWORD = os.getenv("PASSWORD")

    def __init__(self):
        self.driver = webdriver.Chrome()

    def replace_spaces_with_dots(self,string):
        return string.replace(" ", ".") 

    def open_page(self, url):
        self.driver.get(url)

        page_state = self.driver.execute_script("return document.readyState")
        while page_state != "complete":
            page_state = self.driver.execute_script("return document.readyState")


    def destroy_driver(self):
        self.driver.quit()

    def find_el(self, by, value):
        return WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((by, value))
        )

    def e_devlet_ile_giriş_yap_sayfasını_ac(self):
        btn_e_devlet_ile_giris = self.find_el(By.CLASS_NAME, self.replace_spaces_with_dots(self.CLASSES_BTN_E_DEVLET_ILE_GIRIS))
        self.click_to(btn_e_devlet_ile_giris)

    def set_value_to_input(self, element, value):
        element.clear()
        element.send_keys(value)

    def e_devlet_ile_giriş_formunu_gonder(self):
        tckimlikno_input = self.find_el(By.ID, "tridField")
        self.set_value_to_input(tckimlikno_input, self.TC_NO)

        password_input = self.find_el(By.ID, "egpField")
        self.set_value_to_input(password_input, self.PASSWORD)

        giris_yap_button = self.find_el(By.CLASS_NAME, self.replace_spaces_with_dots(self.CLASSES_OF_E_DEVLET_ILE_GIRIS_YAP_BUTTON))
        self.click_to(giris_yap_button)
    
    def click_to(self, element):
        element.click()

    def randevu_al_sayfasını_ac(self):
        # tanı modal'ı varsa kapatıyoruz
        tani_modal_kapat_button = self.driver.find_elements(By.CSS_SELECTOR, self.replace_spaces_with_dots(self.CLASSES_OF_TANI_MODAL_BODY)+'>'+self.replace_spaces_with_dots(self.CLASSES_OF_TANI_MODAL_KAPAT_BUTTON))
        if len(tani_modal_kapat_button) > 0:
            self.click_to(tani_modal_kapat_button[0])

        hastane_randevusu_al_button = self.find_el(By.CLASS_NAME, self.replace_spaces_with_dots(self.CLASSES_OF_HASTANE_RANDEVUSU_AL_BUTTON))
        self.click_to(hastane_randevusu_al_button)

        genel_arama_button = self.find_el(By.CLASS_NAME, self.replace_spaces_with_dots(self.CLASSES_OF_GENEL_ARAMA_BUTTON))
        self.click_to(genel_arama_button)

try:
    mh = MHRS()
    mh.open_page(MHRS.MHRS_URL)
    mh.e_devlet_ile_giriş_yap_sayfasını_ac()
    mh.e_devlet_ile_giriş_formunu_gonder()
    mh.randevu_al_sayfasını_ac()
    time.sleep(1000)
except Exception as e:
    print("Hata olu tur ", e)

