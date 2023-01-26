# -*- encoding: utf-8 -*-
#@Author  :   Arthals
#@File    :   TreeholeNotifier.py
#@Time    :   2023/01/26 15:49:20
#@Contact :   zhuozhiyongde@126.com
#@Software:   Visual Studio Code

import requests
import datetime
import time
import json
import sys
import os
import re


def log(*args):
    # trans args to string
    msg = [str(arg) for arg in args].join(' ')
    print(datetime.datetime.now(), '\t', msg)


class TreeholeSpider:

    def __init__(self):
        self.url = "https://treehole.pku.edu.cn/api"

    def login(self, uid, password):
        try:
            login_url = self.url + "/login"
            self.login_headers = {
                "Accept": "application/json, text/plain, */*",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
                "Connection": "keep-alive",
                "Content-Length": "42",
                "Content-Type": "application/json",
                "DNT": "1",
                "Host": "treehole.pku.edu.cn",
                "Origin": "https://treehole.pku.edu.cn",
                "Referer": "https://treehole.pku.edu.cn/web/login",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "User-Agent":
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
                "sec-ch-ua": 'Chromium";v="109", "Not_A Brand";v="99"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "macOS"
            }
            login_data = {"uid": uid, "password": password}
            res = requests.post(url=login_url,
                                data=json.dumps(login_data),
                                headers=self.login_headers,
                                allow_redirects=True)

            # Login Error
            # {'code': 40001, 'message': '2用户名或密码错误-来自上游IAAA的错误信息', 'success': False, 'timestamp': 1674732171}
            if (res.json()["success"] is False):
                log('Login Failed - Authorization Error', res.json())
                raise RuntimeError("Login Error")

            # HTTP Error
            elif (res.status_code != 200):
                log('Login Failed - HTTP Error', res.status_code, res.text)
                raise RuntimeError("HTTP Error")

            # Login Success
            # print(res.json())
            self.token = res.json()["data"]["jwt"]
            return True

        except RuntimeError:
            return False

        except TimeoutError as e:
            log('Login Failed - Timeout Error', repr(e))
            return False

        except Exception as e:
            log('Login Failed - Unknown Error', repr(e))
            return False

    def save_token(self, token):
        self.token = token

    def get_treehole_comments(self, tid):
        '''
        Returns:
            {
                'misc':{}
                'data':[
                    {
                        'cid': 'cid',
                        'pid': 'pid',
                        'text': 'text with alias',
                        'timestamp': 'timestamp',
                        'hidden': 'hidden',
                        'tag': 'tag',
                        'islz': 'islz',
                        'name': 'alias'
                    }
                ]
            }
        '''
        try:
            comments_url = self.url + f"/pku_comment/{tid}?limit=50000"
            if (self.token is None):
                log('Get Treehole Comments Error - Token is None')
                raise Exception("Token is None")

            self.get_headers = {
                "Accept":
                'application/json, text/plain, */*',
                "Accept-Encoding":
                'gzip, deflate, br',
                "Accept-Language":
                'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
                "Authorization":
                'Bearer ' + self.token,
                "Connection":
                'keep-alive',
                "Cookie":
                f'hb_MA-B701-2FC93ACD9328_source=entryhz.qiye.163.com; pku_token={self.token}',
                "DNT":
                '1',
                "Host":
                'treehole.pku.edu.cn',
                "Referer":
                'https://treehole.pku.edu.cn/web/',
                "sec-ch-ua":
                '"Chromium";v="109", "Not_A Brand";v="99"',
                "sec-ch-ua-mobile":
                '?0',
                "sec-ch-ua-platform":
                '"macOS"',
                "Sec-Fetch-Dest":
                'empty',
                "Sec-Fetch-Mode":
                'cors',
                "Sec-Fetch-Site":
                'same-origin',
                "User-Agent":
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            }

            res = requests.get(url=comments_url,
                               headers=self.get_headers,
                               timeout=5)
            # Token Error
            if (res.status_code == 401):
                log(
                    'Get Treehole Comments Error - HTTP Error 401, maybe token error',
                )
                raise RuntimeError("Token Error")

            elif (res.status_code != 200):
                log('Get Treehole Comments Error - HTTP Error',
                    res.status_code, res.text)
                raise RuntimeError("HTTP Error")

            return res.json()["data"]

        except RuntimeError:
            return False

        except TimeoutError as e:
            log('Get Treehole Comments Error - Timeout Error', repr(e))
            return False

        except Exception as e:
            log('Get Treehole Comments Error - Unknown Error', repr(e))
            return False

    def save_treehole_comments(self, tid):
        try:
            if (self.token is None):
                log('Save Treehole Comments Error - Token is None')
                raise RuntimeError("Token is None")
            comments = self.get_treehole_comments(tid)

            if (comments is False):
                return False

            with open(f"{tid}_comments.json", "w") as f:
                f.write(json.dumps(comments, indent=4, ensure_ascii=False))
        except RuntimeError:
            return False

    def search_keywords(self, keywords, ignore_pattern=None):
        try:
            if (self.token is None):
                log('Search Keywords Error - Token is None')
                raise RuntimeError("Token is None")

            self.get_headers = {
                "Accept":
                'application/json, text/plain, */*',
                "Accept-Encoding":
                'gzip, deflate, br',
                "Accept-Language":
                'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
                "Authorization":
                'Bearer ' + self.token,
                "Connection":
                'keep-alive',
                "Cookie":
                f'hb_MA-B701-2FC93ACD9328_source=entryhz.qiye.163.com; pku_token={self.token}',
                "DNT":
                '1',
                "Host":
                'treehole.pku.edu.cn',
                "Referer":
                'https://treehole.pku.edu.cn/web/',
                "sec-ch-ua":
                '"Chromium";v="109", "Not_A Brand";v="99"',
                "sec-ch-ua-mobile":
                '?0',
                "sec-ch-ua-platform":
                '"macOS"',
                "Sec-Fetch-Dest":
                'empty',
                "Sec-Fetch-Mode":
                'cors',
                "Sec-Fetch-Site":
                'same-origin',
                "User-Agent":
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
            }

            # polyfill the sb api
            for page in range(1, 10):
                search_url = self.url + f"/pku_hole?page={page}&limit=1000&keyword={keywords}"
                res = requests.get(url=search_url,
                                   headers=self.get_headers,
                                   timeout=5)
                # Token Error
                if (res.status_code == 401):
                    log(
                        'Search Keywords Error - HTTP Error 401, maybe token error',
                    )
                    raise RuntimeError("Token Error")

                # HTTP Error
                elif (res.status_code != 200):
                    log('Search Keywords Error - HTTP Error', res.status_code,
                        res.text)
                    raise RuntimeError("HTTP Error")

                res = res.json()["data"]["data"]
                for hole in res:
                    if re.search(keywords, hole["text"],
                                 re.IGNORECASE) is not None:
                        if ignore_pattern is not None:
                            if re.search(ignore_pattern, hole["text"]) is None:
                                continue
                        return hole["pid"]
            return None

        except RuntimeError:
            return False

        except TimeoutError as e:
            log('Search Keywords Error - Timeout Error', repr(e))
            return False

        except Exception as e:
            log('Search Keywords Error - Unknown Error', repr(e))
            return False


class TreeholeUpdater():

    def __init__(self, config: dict):
        self.spider = TreeholeSpider()
        if (config.get("token") is not None):
            print("Init with token")
            self.spider.save_token(config.get("token"))
        else:
            print("Init with uid and password")
            self.spider.login(config.get("uid"), config.get("password"))

    def get_watch_list(self):
        if (not os.path.exists("watch_list.json")):
            with open("watch_list.json", "w") as f:
                empty_watch_list = {"watch_list": []}
                f.write(
                    json.dumps(empty_watch_list, indent=4, ensure_ascii=False))
        with open("watch_list.json", "r") as f:
            self.watch_list = json.load(f)["watch_list"]

    def check_update(self):
        self.get_watch_list()
        updated_holes = []
        for hole in self.watch_list:
            tid = hole["tid"]
            comments = self.spider.get_treehole_comments(tid)['data']
            last_comment_timestamp = max(
                [comment['timestamp'] for comment in comments])
            if last_comment_timestamp > hole["last_update"]:
                print(
                    "detected treehole update: ",
                    hole.get("nick")
                    if hole.get("nick") is not None else hole["tid"])
                hole["last_update"] = last_comment_timestamp
                updated_holes.append(hole)
            time.sleep(0.5)

        with open("watch_list.json", "w") as f:
            output = {"watch_list": self.watch_list}
            f.write(json.dumps(output, indent=4, ensure_ascii=False))

        return updated_holes

    def get_watch_keywords(self):
        if (not os.path.exists("watch_keywords.json")):
            with open("watch_keywords.json", "w") as f:
                empty_watch_keywords = {"watch_keywords": []}
                f.write(
                    json.dumps(empty_watch_keywords,
                               indent=4,
                               ensure_ascii=False))
        with open("watch_keywords.json", "r") as f:
            self.watch_keywords = json.load(f)["watch_keywords"]

    def check_update_with_keywords(self):
        self.get_watch_keywords()
        updated_keywords = []
        for keyword in self.watch_keywords:
            if keyword.get("ignore_pattern") is None:
                tid = self.spider.search_keywords(keyword["keyword"])

            elif keyword.get("last_hole") is None:
                keyword["last_hole"] = 0

            elif keyword["ignore_pattern"]:
                tid = self.spider.search_keywords(keyword["keyword"],
                                                  keyword["ignore_pattern"])
            else:
                tid = self.spider.search_keywords(keyword["keyword"])

            if tid is not None:
                if (tid > keyword["last_hole"]):
                    keyword["last_hole"] = tid
                    print("detected keywords update: ",
                          f'keyword: [{keyword["keyword"]}]',
                          f', last_hole: [#{keyword["last_hole"]}]')
                    updated_keywords.append(keyword)

            time.sleep(0.5)
        with open("watch_keywords.json", "w") as f:
            output = {"watch_keywords": self.watch_keywords}
            f.write(json.dumps(output, indent=4, ensure_ascii=False))
        return updated_keywords


if __name__ == "__main__":
    # get uid and password from args
    if (len(sys.argv) != 3):
        print("Usage: python3 treehole_updater.py uid password")
        exit(0)
    uid = sys.argv[1]
    password = sys.argv[2]

    config = {
        "uid": uid,
        "password": password,
    }

    updater = TreeholeUpdater(config)
    treehole_update_list = updater.check_update()
    keywords_update_list = updater.check_update_with_keywords()
    if (len(treehole_update_list) == 0 and len(keywords_update_list) == 0):
        log("No update")
        exit(0)
    else:
        log("Update detected")
        with open("flag.txt", "w") as f:
            f.write("Higher Grade!")
