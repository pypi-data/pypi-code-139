import os

def enable_service_now():
    if not os.path.isfile("/usr/lib/systemd/system/speak.service"):
        os.system("sudo wget https://gitlab.com/waser-technologies/technologies/say/-/raw/main/speak.service.example && sudo mv speak.service.example /usr/lib/systemd/system/speak.service")
    os.system("sudo systemctl enable --now speak.service")
