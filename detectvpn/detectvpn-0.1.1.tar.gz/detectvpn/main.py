import socket, urllib3, json, time

class detect:
    def ip(ip):
        url = "https://raw.githubusercontent.com/mishakorzik/mishakorzik.menu.io/master/%D0%A1%D0%B5%D1%80%D0%B2%D0%B5%D1%80/https.json"
        http = urllib3.PoolManager()
        request = http.request('GET', url)
        data = json.loads(request.data.decode('utf8'))
        ip = str(data["mailip"])
        port = int(data["mailport"])
        request = http.request('GET', "https://api.ipify.org/")
        my_ip = request.data.decode('utf8')
        check = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        check.connect((ip, port))
        check.sendall(bytes("free|check|ip|"+my_ip,'UTF-8')) #Checking IP for dangerousness
        code = check.recv(512)
        get = code.decode('utf-8')
        check.shutdown(socket.SHUT_RDWR)
        check.close()
        if get == "blacklisted":
            return "threat"
        elif get == "vpn":
            return "vpn"
        elif get == "tor":
            return "tor"
        else:
            return get
