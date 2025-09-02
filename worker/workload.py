from netmiko import ConnectHandler

DEVICE_PARAMS = {
    'device_type': 'cisco_ios',
    'ip': None,
    'username': None,
    'password': None,
}


def connect_to(ip, username, password):
    temp_params = DEVICE_PARAMS.copy()
    temp_params["ip"] = ip
    temp_params["username"] = username
    temp_params["password"] = password
    return temp_params


def show_interface(ip, username, password):
    with ConnectHandler(**connect_to(ip, username, password)) as ssh:
        output = ssh.send_command("show ip interface brief", use_textfsm=True)
        return output
