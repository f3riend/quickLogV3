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
import socket
import json
import sys
import os


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / "assets"


def relative_to_assets(path: str) -> Path:
    full_path = ASSETS_PATH / Path(path)
    if not full_path.exists():
        messagebox.showerror("Dosya Bulunamadı", f"Resim dosyası bulunamadı: {full_path}")
    return full_path


def is_chrome_installed():
    chrome_paths = [
        r"/usr/bin/google-chrome",
        r"/usr/local/bin/google-chrome",
    ]
    return any(os.path.exists(path) for path in chrome_paths)


def check_internet():
    try:
        socket.create_connection(("8.8.8.8", 53))
        ic("Network connection successful")
        return True
    except OSError:
        ic("Network connection unsuccessful")
        return False


def read_passwords():
    try:
        passwords_file = os.path.join(sys._MEIPASS, "passwords.json") if getattr(sys, 'frozen', False) else "passwords.json"
        with open(passwords_file, "r") as file:
            return json.load(file)
    except Exception as e:
        print(f"Şifreler okunamadı: {str(e)}")
        return None


def login_to_platform(url, email_xpath, password_xpath, next_button_xpath, email, password):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            try:
                self.open_new_tab(url)
                self.driver.switch_to.window(self.driver.window_handles[-1])

                emailBox = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, email_xpath)))
                emailBox.send_keys(email)
                self.driver.find_element(By.XPATH, next_button_xpath).click()

                passwordBox = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, password_xpath)))
                passwordBox.send_keys(password)
                self.driver.find_element(By.XPATH, next_button_xpath).click()

                sleep(2)
                WebDriverWait(self.driver, 10).until(EC.url_contains("myaccount.google.com"))
                func(self, *args, **kwargs)

            except Exception as e:
                ic(f"Login failed for {url}", e)
        return wrapper
    return decorator


class LoginSystem:
    def __init__(self) -> None:
        self.username = os.getlogin()
        self.profile_path = f"/home/{self.username}/.config/google-chrome/Default/"
        self.options = Options()
        self.options.add_experimental_option("detach", True)
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_experimental_option('useAutomationExtension', False)
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.options.add_argument("--disable-popup-blocking")
        self.options.add_argument("--disable-save-password-bubble")
        self.options.add_argument(f"user-data-dir={self.profile_path}")
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=self.options)
        self.driver.maximize_window()

    def open_new_tab(self, url):
        self.driver.execute_script(f"window.open('{url}', '_blank');")

    @login_to_platform("https://accounts.google.com/v3/signin/identifier", 
                        '//*[@id="identifierId"]', 
                        '//*[@id="password"]/div[1]/div/div[1]/input', 
                        '//*[@id="identifierNext"]/div/button', 
                        'gmail_email', 'gmail_password')
    def login_to_gmail(self, email, password):
        pass

    @login_to_platform("https://github.com/login", 
                        '//*[@id="login_field"]', 
                        '//*[@id="password"]', 
                        '//*[@id="login"]/div[4]/form/div/input[13]', 
                        'github_email', 'github_password')
    def login_to_github(self, email, password):
        pass

    @login_to_platform("https://www.instagram.com/", 
                        '//*[@id="loginForm"]/div/div[1]/div/label/input', 
                        '//*[@id="loginForm"]/div/div[2]/div/label/input', 
                        '//*[@id="loginForm"]/div/div[3]/button', 
                        'instagram_email', 'instagram_password')
    def login_to_instagram(self, email, password):
        pass

    @login_to_platform("https://store.steampowered.com/login/?redir=&redir_ssl=1&snr=1_4_600__global-header", 
                        '//*[@id="responsive_page_template_content"]/div[3]/div[1]/div/div/div/div[2]/div/form/div[1]/input', 
                        '//*[@id="responsive_page_template_content"]/div[3]/div[1]/div/div/div/div[2]/div/form/div[2]/input', 
                        '//*[@id="responsive_page_template_content"]/div[3]/div[1]/div/div/div/div[2]/div/form/div[4]/button', 
                        'steam_email', 'steam_password')
    def login_to_steam(self, email, password):
        pass

    @login_to_platform("https://discord.com/login", 
                        '//*[@id="uid_7"]', 
                        '//*[@id="uid_9"]', 
                        '//*[@id="app-mount"]/div[2]/div[1]/div[1]/div/div/div/div/form/div[2]/div/div[1]/div[2]/button[2]', 
                        'discord_email', 'discord_password')
    def login_to_discord(self, email, password):
        pass


def on_press(key, window):
    if key == keyboard.Key.esc:
        print("ESC pressed, closing window.")
        window.destroy()


def create_button(image_path, x, y, width, height, command, window):
    try:
        image = PhotoImage(file=relative_to_assets(image_path))
        button = Button(image=image, borderwidth=0, highlightthickness=0, command=command, relief="flat", bg="white", activebackground="white")
        button.image = image
        button.place(x=x, y=y, width=width, height=height)
    except Exception as e:
        messagebox.showerror("Yükleme Hatası", f"Resim yüklenemedi: {image_path}\nHata: {str(e)}")


def main():
    if not check_internet():
        messagebox.showinfo("Internet", "Please connect to the internet")
        sys.exit()

    if not is_chrome_installed():
        messagebox.showinfo("Chrome", "Chrome is not installed. Please install it.")
        sys.exit()

    data = read_passwords()
    login_system = LoginSystem()

    locX, locY = 0, pyautogui.size().height - 225

    window = Tk()
    window.geometry("400x225+{}+{}".format(locX, locY))
    window.configure(bg="#FFFFFF")
    window.overrideredirect(True)
    window.attributes("-topmost", True)

    canvas = Canvas(window, bg="#FFFFFF", height=225, width=400, bd=0, highlightthickness=0, relief="ridge")
    canvas.place(x=0, y=0)
    canvas.create_text(140.0, 45.0, anchor="nw", text="QUICK LOG", fill="#D9D9D9", font=("RobotoRoman Medium", 24 * -1))
    canvas.create_text(16.0, 208.0, anchor="nw", text="designed and developed by f3riend", fill="#D9D9D9", font=("Inter Light", 12 * -1))

    button_actions = {
        'gmail': lambda: login_system.login_to_gmail(data['email']['username'], data['email']['pass']),
        'instagram': lambda: login_system.login_to_instagram(data['instagram']['username'], data['instagram']['pass']),
        'github': lambda: login_system.login_to_github(data['github']['username'], data['github']['pass']),
        'discord': lambda: login_system.login_to_discord(data['discord']['username'], data['discord']['pass']),
        'steam': lambda: login_system.login_to_steam(data['steam']['username'], data['steam']['pass']),
    }

    button_positions = [
        ("image_1.png", 139.0, 158.0, 30.0, 30.0, button_actions['gmail']),
        ("image_2.png", 185.0, 158.0, 30.0, 30.0, button_actions['instagram']),
        ("image_3.png", 231.0, 158.0, 30.0, 30.0, button_actions['github']),
        ("image_4.png", 277.0, 158.0, 30.0, 30.0, button_actions['discord']),
        ("image_5.png", 93.0, 158.0, 30.0, 30.0, button_actions['steam']),
    ]

    for image_path, x, y, width, height, command in button_positions:
        create_button(image_path, x, y, width, height, command, window)

    window.resizable(False, False)

    with keyboard.Listener(on_press=lambda key: on_press(key, window)) as listener:
        window.mainloop()
        listener.join()


if __name__ == "__main__":
    main()
