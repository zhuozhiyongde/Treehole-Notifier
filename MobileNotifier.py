# -*- encoding: utf-8 -*-
#@Author  :   Arthals
#@File    :   MobileNotifier.py
#@Time    :   2023/01/26 23:06:58
#@Contact :   zhuozhiyongde@126.com
#@Software:   Visual Studio Code

import os

if __name__ == "__main__":
    # check if the file exists
    if os.path.exists("flag.txt"):
        # remove the file
        os.remove("flag.txt")
        exit(1)
    else:
        exit(0)
