
import unittest
import pandas as pd
from ncclient import manager

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
        row = self.info[self.info['Router'] == 'R3']
        ip = row['Mgmt IP'].values[0]
        user = row['Username'].values[0]
        pwd = row['Password'].values[0]
        with manager.connect(
            host=ip,
            port=22,
            username=user,
            password=pwd,
            hostkey_verify=False,
            device_params={'name': 'iosxr'},
            allow_agent=False,
            look_for_keys=True
        ) as m:
            filter_xml = '''<filter><interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces"/></filter>'''
            reply = m.get(filter_xml)
            xml_str = str(reply.xml)
            self.assertIn('Loopback99', xml_str)
            self.assertIn('10.1.3.1', xml_str)

    def test_single_area_r1(self):
        device = self.get_device('R1')
        with ConnectHandler(**device) as net_connect:
            net_connect.enable()
            output = net_connect.send_command('show running-config | include area')
            areas = set()
            import unittest
            import pandas as pd
            from ncclient import manager

            class TestNetmanNetconf(unittest.TestCase):
                @classmethod
                def setUpClass(cls):
                    cls.info = pd.read_csv('info.csv')

                def netconf_connect(self, router_name):
                    row = self.info[self.info['Router'] == router_name]
                    ip = row['Mgmt IP'].values[0]
                    user = row['Username'].values[0]
                    pwd = row['Password'].values[0]
                    return manager.connect(
                        host=ip,
                        port=22,
                        username=user,
                        password=pwd,
                        hostkey_verify=False,
                        device_params={'name': 'iosxr'},
                        allow_agent=False,
                        look_for_keys=True
                    )

                def test_loopback_r3(self):
                    with self.netconf_connect('R3') as m:
                        filter_xml = '''<filter><interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces"/></filter>'''
                        reply = m.get(filter_xml)
                        xml_str = str(reply.xml)
                        self.assertIn('Loopback99', xml_str)
                        self.assertIn('10.1.3.1', xml_str)

                def test_single_area_r1(self):
                    with self.netconf_connect('R1') as m:
                        filter_xml = '''<filter><ospf xmlns="urn:ietf:params:xml:ns:yang:ietf-ospf"/></filter>'''
                        reply = m.get(filter_xml)
                        xml_str = str(reply.xml)
                        areas = xml_str.count('area')
                        self.assertEqual(areas, 1, f"FAILURE! R1 is configured for multiple areas")

                def test_ping_r2_to_r5(self):
                    with self.netconf_connect('R2') as m:
                        filter_xml = '''<filter><interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces"/></filter>'''
                        reply = m.get(filter_xml)
                        xml_str = str(reply.xml)
                        r5 = self.info[self.info['Router'] == 'R5']
                        ip5 = r5['Loopback IP'].values[0]
                        self.assertIn(ip5, xml_str)

            if __name__ == '__main__':
                unittest.main()
