#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# /Check/tart/Stop VM script
# Version: V1.2
# Author: Jun Yu
# Created: 09/15/2021
import types
import json
import requests
import urllib3
import string
import random
import sys
import os
import time


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

host = 'XX.XX.XX.XX'
# VCenter server IP

def get_cookies():
    url = 'https://' + host + '/rest/com/vmware/cis/session'

    payload = {}
    files = {}
    headers = {
        'Authorization': 'Basic password'
        # VCenter login username and password, generated the username/password by Base64.
        # Usage: username:password, like:administrator@vsphere.local:12345678
        # Example: "Basic dXNlcm5hbWU6cGFzc3dvcmQ="

    }

    response = requests.request("POST", url, headers=headers, verify=False, data=payload, files=files)
    if response.status_code != 200:
        print("获取cookie失败")
        os.exit(1)
    token = response.headers['set-cookie'][0:54]
    return token


class Vcenter():

    def list_vm(self, token):
        url = 'https://' + host + '/rest/vcenter/vm'
        playload = {}
        headers = {
            'Cookie': token1
        }
        response = requests.request("GET", url, headers=headers, verify=False, data=playload)
        json_str = json.loads(response.text)
        for x in range(0, len(json_str['value'])):
            print("vm:", json_str['value'][x]['name'], "status:", json_str['value'][x]["power_state"])

    def start_vm(self, vm_name, token):
        url = 'https://' + host + '/rest/vcenter/vm?filter.names.1={}'.format(vm_name)
        # Get VM name which need start
        payload = {}
        headers = {
            'Cookie': token
        }
        response = requests.request("GET", url, headers=headers, verify=False, data=payload)
        if len(response.json()['value']) == 0:
            print("没有找到vm:{}".format(vm_name))
            os._exit(1)
            # return
        vm_status = response.json()['value'][0]['power_state']
        vm = response.json()['value'][0]['vm']
        if vm_status != "POWERED_ON":
            pass
        else:
            print("vm:{} 运行中,无需开机.".format(vm_name))
            # os._exit(1)
            return

        # start vm
        url = 'https://' + host + '/rest/vcenter/vm/{}/power/start'.format(vm)
        payload = {}
        headers = {
            'Cookie': token
        }
        response = requests.request("POST", url, headers=headers, verify=False, data=payload)
        if response.status_code == 200:
            print("vm:{} is starting...".format(vm_name))
        time.sleep(10)
        url = 'https://' + host + '/rest/vcenter/vm?filter.names.1={}'.format(vm_name)
        response = requests.request("GET", url, headers=headers, verify=False, data=payload)
        json_str = json.loads(response.text)
        for x in range(0, len(json_str['value'])):
            if json_str['value'][x]['power_state'] == 'POWERED_ON':
                print("vm:", json_str['value'][x]['name'], "status:", json_str['value'][x]['power_state'], "已开机.")
            return

    def shutdown_vm(self, vm_name, token):
        url = 'https://' + host + '/rest/vcenter/vm?filter.names.1={}'.format(vm_name)
        payload = {}
        headers = {
            'Cookie': token
        }
        response = requests.request("GET", url, headers=headers, verify=False, data=payload)
        if len(response.json()['value']) == 0:
            print("没有找到vm:{}".format(vm_name))
            os._exit(1)
            # return
        vm_status = response.json()['value'][0]['power_state']
        vm = response.json()['value'][0]['vm']
        if vm_status == "POWERED_OFF":
            print("vm:{} 已关机，无需重复关机".format(vm_name))
            return

        # stop vm
        url = 'https://' + host + '/rest/vcenter/vm/{}/guest/power?action=shutdown'.format(vm)
        payload = {}
        headers = {
            'Cookie': token
        }
        response = requests.request("POST", url, headers=headers, verify=False, data=payload)
        if response.status_code == 200:
            print("vm:{} stopping...".format(vm_name))
        url = 'https://' + host + '/rest/vcenter/vm?filter.names.1={}'.format(vm_name)
        response = requests.request("GET", url, headers=headers, verify=False, data=payload)
        json_str = json.loads(response.text)
        states = (json_str['value'][0]['power_state'])
        result = False
        now_a = time.time()
        while result == False:
            response = requests.request("GET", url, headers=headers, verify=False, data=payload)
            json_str = json.loads(response.text)
            states = (json_str['value'][0]['power_state'])
            if states == "POWERED_OFF":
                print("VM status is", states)
                print("vm:", vm_name, "已关机.")
                result = True
            else:
                print("VM", vm_name, "status is", states, "please wait.")
            time.sleep(5)
            now_b = time.time() - now_a
            if now_b > 60:
                print("VM shutdown error,shutdown process abort.")
                # if a VM server shutdown more than 60s, then abort the process.
                result = True
                os._exit(1)


def error():
    print("参数错误")
    print("脚本使用方法：")
    print("================================================================")
    print("查询VM状态：""python {} list_vm".format(sys.argv[0]))
    print("启动VM：""python {} start vm_name1 vm_name2 vm_name(n)".format(sys.argv[0]))
    print("关闭VM：""python {} shutdown vm_name1 vm_name2 vm_name(n)".format(sys.argv[0]))
    print("================================================================")
    os._exit(1)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        error()
#        print("参数错误")
#        print("脚本使用方法：")
#        print("================================================================")
#        print("查询VM状态：""python {} list_vm".format(sys.argv[0]))
#        print("启动VM：""python {} start vm_name1 vm_name2 vm_name(n)".format(sys.argv[0]))
#        print("关闭VM：""python {} shutdown vm_name1 vm_name2 vm_name(n)".format(sys.argv[0]))
#        print("================================================================")
        os._exit(1)

    abc = Vcenter()
    token1 = get_cookies()

    if len(sys.argv) == 2 and sys.argv[1] == "list_vm":
        abc.list_vm(token1)
    elif len(sys.argv) <= 2 and sys.argv[1] == "start":
        print("Please entry VM name.")
        os._exit(1)
    elif len(sys.argv) >= 3 and sys.argv[1] == "start":
        for vm_name in sys.argv[2:]:
            print(vm_name)
            abc.start_vm(vm_name, token1)
    elif len(sys.argv) <= 2 and sys.argv[1] == "shutdown":
        print("Please entry VM name.")
        os._exit(1)
    elif len(sys.argv) >= 3 and sys.argv[1] == "shutdown":
        for vm_name in sys.argv[2:]:
            print(vm_name)
            abc.shutdown_vm(vm_name, token1)
    else:
        error()
