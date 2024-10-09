# quickLogV3


**Reason for development:**

When I wrote it with flask I was having trouble converting it to an exe file and it was also opening a little late, in version 2 I wrote it with c# for the exe event but it also creates an installation file and I have to delete it after installing it for each computer, if it is not my computer, so I developed this version.


**previous versions :**
- <a href="https://github.com/f3riend/quickLogV1">Version 1 coded with flask</a>
- <a href="https://github.com/f3riend/quickLogV2"> Version 2 coded with c#</a>


**Purpose :**
When I'm not on my own computer, I can run this program on the device I plug my flash drive into and it automatically logs me into my accounts quickly.
You can quickly log in to your Google accounts, in this project you can quickly log in to these accounts:

- Gmail
- Instagram
- Discord
- Github
- Steam


**Important:**

After installing it, you need to edit the passwords.json file according to yourself, and if you are going to log in via gmail, you need to delay with sleep(180) for emails that require 2-step verification, in my case, my 3rd email address requires it.


**Advice :**

You can add or not add the passwords.json file according to your request while making the exe file, if you add it, you need to print it again in case of password change, but if you do not add it, it will not give an error as long as it is in the same directory, so you can change your passwords by editing the file whenever you want.

**Install PyInstaller:**
```bash
pip install pyinstaller
```

Add this globally to the System and Environment variables accordingly
Run cmd as administrator and run the following, but change the python version to your own

**Mine is Python312**

```bash
setx PATH "%PATH%;%USERPROFILE%\AppData\Roaming\Python\Python312\Scripts"
```


```bash
pip install -r requirements.txt
pyinstaller --onefile --add-data “assets;assets” --add-data “passwords.json;.” main.py
```


**Additions :**

- Will open on default chrome profile
- If Chrome is not installed, it will automatically install and run the program
- It will run faster compared to previous versions
- You can close the sub-window by pressing esc and your sessions will still be open

**Disadvantages:**
Take care not to rush when using it: the reason for this is that although it does not cause problems on fast internet, you may experience problems on slow internet.
