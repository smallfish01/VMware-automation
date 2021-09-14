#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# Author: Old Farmer
# List VM script

import types
import json
import requests
import urllib3
import string
import random
import sys
import os

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

host = '192.168.13.182'


class Vcenter():

    def get_cookies(self):
        url = 'https://' + host + '/rest/com/vmware/cis/session'

        payload = {}
        files = {}
        headers = {
            'Authorization': 'Basic YWRtaW5pc3RyYXRvckB2c3BoZXJlLmxvY2FsOlRjMTIzNDU2Kigp'
        }

        response = requests.request("POST", url, headers=headers, verify=False, data=payload, files=files)

        if response.status_code != 200:
            print("获取cookie失败")
            os.exit(1)

        token = response.headers['set-cookie'][0:54]
        return token

    def list_vm(self, token):
        url = 'https://' + host + '/rest/vcenter/vm'
        playload = {}
        headers = {
            'Cookie': token1
        }
        response = requests.request("GET", url, headers=headers, verify=False, data=playload)
        # print("response:", response)
        json_str = json.loads(response.text)
        # print("json_str:", json_str)
        # print(len(json_str))
        for x in range(0, len(json_str['value'])):
            # print("x:", x)
            print("vm:", json_str['value'][x]['name'], "status:", json_str['value'][x]["power_state"])


if __name__ == '__main__':
    # print(sys.argv)
    if len(sys.argv) == 1:
        print("参数错误")
        print("脚本使用方法：")
        print("================================================================")
        print("python {} list_vm".format(sys.argv[0]))
#        print("python {} start vm_name1 vm_name2 vm_name(n)".format(sys.argv[0]))
        print("================================================================")
        os._exit(1)

    abc = Vcenter()
    token1 = abc.get_cookies()

    if len(sys.argv) == 2 and sys.argv[1] == "list_vm":
        # print("调用:abc.list_vm(token1)")
        abc.list_vm(token1)
 
