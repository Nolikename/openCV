# -*- coding: utf-8
import time
import sys
import uuid
import requests
import jwt


class LogOut(object):

    @classmethod
    def log(cls, msg):
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print("\033[1;32m [QSLTRunner  INFO] {} - {} \033[0m".format(now, msg))

    @classmethod
    def log_debug(cls, msg):
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print("\033[1;37m [QSLTRunner DEBUG] {} - {} \033[0m".format(now, msg))

    @classmethod
    def log_error(cls, msg):
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print("\033[1;31m [QSLTRunner ERROR] {} - {} \033[0m".format(now, msg))


class EptestReporter:

    def __init__(self):
        self.__app_id = "weseeiosperf"
        self.__app_key = "f7d877b6-7d52-482b-8498-0247a36465b7"

    def __make_token(self, timeout_seconds):
        claims = {
            "iss": self.__app_id,
            "iat": int(time.time()) - timeout_seconds,
            "exp": timeout_seconds + int(time.time()),
            "id": str(uuid.uuid1()),
        }
        token = jwt.encode(claims, self.__app_key)
        # return "Bearer " + token
        if isinstance(token, str):
            return "Bearer " + token
        else:
            return "Bearer " + str(token, encoding="utf-8")

    def __make_header(self, timeout_seconds=300):
        headers = {
            'content-type': 'application/json;charset=UTF-8',
            'Authorization': self.__make_token(timeout_seconds)
        }
        return headers

    def get(self, url):
        response = requests.get(url, headers=self.__make_header())
        if response.status_code == 200:
            return response.content
        else:
            LogOut.log_error("请求分层平台后台失败:\nURL:{}\nHTTP CODE:{}\nRESPONSE BODY:{}"
                             .format(url, response.status_code, response.content))
            return False

    def post(self, url, json_dict):

        response = requests.post(url, json=json_dict, headers=self.__make_header())
        print("[response】")
        print(response.content)
        if response.status_code == 200:
            print (response.text.encode('utf-8'))
            return response.content
        else:
            log_dict = json_dict if sys.getsizeof(json_dict) < 1024 * 10 else "too big no print"  # 超过10kb不打印
            LogOut.log_error("请求分层平台后台失败")
            LogOut.log_error("URL:{}".format(url))
            LogOut.log_error("REQUEST BODY:{}".format(log_dict))
            LogOut.log_error("HTTP CODE:{}".format(response.status_code))
            LogOut.log_error("RESPONSE BODY:{}".format(response.text))

            return False

    def post_files(self, url, files):

        response = requests.post(url, files=files)
        LogOut.log("[response: %s]" % (response.content))
        if response.status_code == 200:
            return response.content
        else:
            LogOut.log_error("请求分层平台后台失败")
            LogOut.log_error("URL:{}".format(url))
            LogOut.log_error("上报文件:{}".format(files))
            LogOut.log_error("HTTP CODE:{}".format(response.status_code))
            LogOut.log_error("RESPONSE BODY:{}".format(response.text))

            return False
