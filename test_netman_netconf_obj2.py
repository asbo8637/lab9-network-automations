import unittest
import pandas as pd
from netmiko import ConnectHandler
import time

class TestNetmanNetconf(unittest.TestCase):
    @classmethod
    def setUpClass(my_class):
        my_class.info = pd.read_csv('info.csv')

    def get_device(self, router_name):
        device = {
            'device_type': 'cisco_ios',
            'host': self.info[self.info['Router'] == router_name]['Mgmt IP'].values[0],
            'username': self.info[self.info['Router'] == router_name]['Username'].values[0],
            'password': self.info[self.info['Router'] == router_name]['Password'].values[0],
            'secret': self.info[self.info['Router'] == router_name]['Password'].values[0],
        }
        return device

    def test_loopback_r3(self):
        device = self.get_device('R3')
        with ConnectHandler(**device) as net_connect:
            net_connect.enable()
            output = net_connect.send_command('show ip interface brief | include Loopback99')
            found = False
            for line in output.splitlines():
                if 'Loopback99' in line and '10.1.3.1' in line:
                    found = True
            self.assertTrue(found, f"Loopback99 with IP 10.1.3.1 not found on R3. Output: {output}")

    def test_single_area_r1(self):
        device = self.get_device('R1')
        with ConnectHandler(**device) as net_connect:
            net_connect.enable()
            output = net_connect.send_command('show running-config | include area')
            areas = set()
            for line in output.splitlines():
                if 'area' in line:
                    parts = line.split()
                    if 'area' in parts:
                        idx = parts.index('area')
                        if idx+1 < len(parts):
                            areas.add(parts[idx+1])
            self.assertEqual(len(areas), 1, f"FAILURE! R1 is configured for multiple areas")

    def test_ping_r2_to_r5(self):
        r2 = self.get_device('R2')
        r5 = self.get_device('R5')
        ip5 = self.info[self.info['Router'] == 'R5']['Loopback IP'].values[0]
        with ConnectHandler(**r2) as net_connect:
            net_connect.enable()
            output = net_connect.send_command(f'ping {ip5}')
            success = False
            for line in output.splitlines():
                if 'Success rate is' in line:
                    if '0 percent' not in line:
                        success = True
            self.assertTrue(success, f"FAILURE: Ping from R2 to R5's loopback failed. Output: {output}")

if __name__ == '__main__':
    unittest.main()
