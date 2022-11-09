import hvac


class Kubernetes():
    def login_kubernetes(self):
        client = hvac.Client