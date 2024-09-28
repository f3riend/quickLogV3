from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tkinter import Tk, Canvas, Button, PhotoImage, messagebox
from pynput import keyboard
from pathlib import Path
from icecream import ic
from time import sleep
import subprocess
import pyautogui
import winreg
import socket
import json
import sys
import os




OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / "assets"

def relative_to_assets(path: str) -> Path:
    # Dosya yolunun doğruluğunu kontrol eden fonksiyon
    full_path = ASSETS_PATH / Path(path)
    if not os.path.exists(full_path):
        messagebox.showerror("Dosya Bulunamadı", f"Resim dosyası bulunamadı: {full_path}")
        return None
    return full_path

# Pencere boyutları
width = 400
height = 225


def isChromeInstalled():
    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    ]
    
    for path in chrome_paths:
        if os.path.exists(path):
            return True
    return False


def checkInternet():
    try:
        socket.create_connection(("8.8.8.8", 53))
        ic("Network connection succsessfull")
        return True
    except OSError:
        ic("Network connection unsuccsessfull")
        return False



if not  checkInternet():
    messagebox.showinfo("Internet","Please connect to internet")
    sys.exit()



if not isChromeInstalled():
    os.system("winget install -e --id Google.Chrome")
    messagebox.showinfo("Quick Log","Chrome downloaded...")



class LoginSystem:
    def __init__(self) -> None:
        self.gmailPath = "https://accounts.google.com/v3/signin/identifier?authuser=0&continue=https%3A%2F%2Fmyaccount.google.com%2F%3Fpli%3D1&ec=GAlAwAE&hl=tr&service=accountsettings&flowName=GlifWebSignIn&flowEntry=AddSession&dsh=S1292135306%3A1719765769885536&ddm=0"
        self.githubPath = "https://github.com/login"
        self.instagramPath = "https://www.instagram.com/"
        self.steamPath = "https://store.steampowered.com/login/?redir=&redir_ssl=1&snr=1_4_600__global-header"
        self.discordPath = "https://discord.com/login"

        self.username = os.getlogin()
        self.profilePath = f"C:/Users/{self.username}/AppData/Local/Google/Chrome/User Data"

        self.options = Options()
        self.options.add_experimental_option("detach", True)
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.options.add_argument(f"user-data-dir={self.profilePath}")

        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=self.options)
        self.driver.maximize_window()

    def open_new_tab(self, url):
        self.driver.execute_script(f"window.open('{url}', '_blank');")

    def loginToGmail(self, email, password):
        try:
            self.open_new_tab(self.gmailPath)
            self.driver.switch_to.window(self.driver.window_handles[-1])

            emailBox = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="identifierId"]')))
            emailBox.send_keys(email)
            self.driver.find_element(By.XPATH, '//*[@id="identifierNext"]/div/button').click()

            passwordBox = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input')))
            passwordBox.send_keys(password)
            self.driver.find_element(By.XPATH, '//*[@id="passwordNext"]/div/button').click()

            sleep(2)

            WebDriverWait(self.driver, 10).until(EC.url_contains("myaccount.google.com"))
        except Exception as e:
            ic("Something went wrong", e)

    def loginToGithub(self, email, password):
        try:
            self.open_new_tab(self.githubPath)
            self.driver.switch_to.window(self.driver.window_handles[-1])

            emailBox = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="login_field"]')))
            emailBox.send_keys(email)

            passwordBox = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="password"]')))
            passwordBox.send_keys(password)

            self.driver.find_element(By.XPATH, '//*[@id="login"]/div[4]/form/div/input[13]').click()

        except Exception as e:
            ic("Something went wrong", e)

    def loginToInstagram(self, email, password):
        try:
            self.open_new_tab(self.instagramPath)
            self.driver.switch_to.window(self.driver.window_handles[-1])

            emailBox = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="loginForm"]/div/div[1]/div/label/input')))
            emailBox.send_keys(email)

            passwordBox = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="loginForm"]/div/div[2]/div/label/input')))
            passwordBox.send_keys(password)

            self.driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[3]/button').click()
        except Exception as e:
            ic("Something went wrong", e)

    def loginToSteam(self, email, password):
        try:
            self.open_new_tab(self.steamPath)
            self.driver.switch_to.window(self.driver.window_handles[-1])

            emailBox = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="responsive_page_template_content"]/div[3]/div[1]/div/div/div/div[2]/div/form/div[1]/input')))
            emailBox.send_keys(email)

            passwordBox = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="responsive_page_template_content"]/div[3]/div[1]/div/div/div/div[2]/div/form/div[2]/input')))
            passwordBox.send_keys(password)

            self.driver.find_element(By.XPATH, '//*[@id="responsive_page_template_content"]/div[3]/div[1]/div/div/div/div[2]/div/form/div[4]/button').click()
        except Exception as e:
            ic("Something went wrong", e)

    def loginToDiscord(self, email, password):
        try:
            self.open_new_tab(self.discordPath)
            self.driver.switch_to.window(self.driver.window_handles[-1])

            emailBox = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="uid_10"]')))
            emailBox.send_keys(email)

            passwordBox = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="uid_12"]')))
            passwordBox.send_keys(password)

            self.driver.find_element(By.XPATH, '//*[@id="app-mount"]/div[2]/div[1]/div[1]/div/div/div/div/form/div[2]/div/div[1]/div[2]/button[2]').click()
        except Exception as e:
            ic("Something went wrong", e)


def read_passwords():
    try:
        # MEIPASS kontrolü
        if getattr(sys, 'frozen', False):
            # Uygulama PyInstaller ile paketlenmişse
            passwords_file = os.path.join(sys._MEIPASS, "passwords.json")
        else:
            # Geliştirme sırasında
            passwords_file = "passwords.json"
        
        with open(passwords_file, "r") as file:
            passwords = json.load(file)
            return passwords
    except Exception as e:
        print(f"Şifreler okunamadı: {str(e)}")
        return None
    


data = read_passwords()
loginSystem = LoginSystem()


# Pencere konumu
locX = 0
locY = pyautogui.size().height - height  # Ekranın altına yerleştir

# Pencere oluşturuluyor
window = Tk()
window.geometry(f"{width}x{height}+{locX}+{locY}")
window.configure(bg="#FFFFFF")

# Başlık çubuğunu gizlemek ve her zaman en üstte olmasını sağlamak için
window.overrideredirect(True)  # Başlık çubuğunu kaldır
window.attributes("-topmost", True)  # Her zaman üstte olmasını sağla

# Tuval oluşturuluyor
canvas = Canvas(window, bg="#FFFFFF", height=height, width=width, bd=0, highlightthickness=0, relief="ridge")
canvas.place(x=0, y=0)

# Metin öğeleri oluşturuluyor
canvas.create_text(140.0, 45.0, anchor="nw", text="QUICK LOG", fill="#D9D9D9", font=("RobotoRoman Medium", 24 * -1))
canvas.create_text(16.0, 208.0, anchor="nw", text="designed and developed by f3riend", fill="#D9D9D9", font=("Inter Light", 12 * -1))

# Her buton için ayrı tıklama fonksiyonları
def button_1_clicked():
    emails = data.get('email')
    if emails:
        for key, value in emails.items():
            loginSystem.loginToGmail(value.get('username'), value.get('pass'))

def button_2_clicked():
    instagram = data.get('instagram')
    if instagram:
        loginSystem.loginToInstagram(instagram.get('username'), instagram.get('pass'))

def button_3_clicked():
    github = data.get('github')
    if github:
        loginSystem.loginToGithub(github.get('username'), github.get('pass'))

def button_4_clicked():
    discord = data.get('discord')
    if discord:
        loginSystem.loginToDiscord(discord.get('username'), discord.get('pass'))

def button_5_clicked():
    steam = data.get('steam')
    if steam:
        loginSystem.loginToSteam(steam.get('username'), steam.get('pass'))

# Buton oluşturma fonksiyonu
def create_button(image_path, x, y, width, height, command):
    # Resim yolu çözülüyor
    image_path_resolved = relative_to_assets(image_path)
    if image_path_resolved:
        try:
            # Resim yüklendi
            image = PhotoImage(file=image_path_resolved)
            button = Button(image=image, borderwidth=0, highlightthickness=0, command=command, relief="flat", bg="white", activebackground="white")
            button.image = image  # Butonun referansını tutmak için
            button.place(x=x, y=y, width=width, height=height)  # Buton yerleştiriliyor
        except Exception as e:
            messagebox.showerror("Yükleme Hatası", f"Resim yüklenemedi: {image_path_resolved}\nHata: {str(e)}")
    else:
        print(f"Resim dosyası bulunamadı: {image_path}")

# Butonlar oluşturuluyor
create_button("image_1.png", 139.0, 158.0, 30.0, 30.0, button_1_clicked)
create_button("image_2.png", 185.0, 158.0, 30.0, 30.0, button_2_clicked)
create_button("image_3.png", 231.0, 158.0, 30.0, 30.0, button_3_clicked)
create_button("image_4.png", 277.0, 158.0, 30.0, 30.0, button_4_clicked)
create_button("image_5.png", 93.0, 158.0, 30.0, 30.0, button_5_clicked)



def onPressed(key):
    try:
        # Check if the ESC key is pressed
        if key == keyboard.Key.esc:
            print("ESC pressed, closing window.")
            window.destroy()
    except Exception as e:
        print(f"Error: {e}")


# Pencereyi yeniden boyutlandırmayı kapatıyoruz
window.resizable(False, False)

with keyboard.Listener(on_press=onPressed) as listener:
    # Run the Tkinter main loop
    window.mainloop()
    listener.join()
