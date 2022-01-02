# -*- coding:utf-8 -*-

import re

def parseDate(l):
    patternForTime = r'(^\d{4}[\D]\d{1,2}[\D]\d{1,2} \d{2}:\d{2}:\d{2}[\D]\d{3} (DEBUG|INFO|ERROR|WARN) )'

    for i in l:
        m = re.search(patternForTime, i)
        if m:
            print(m.group(1))

if __name__ == '__main__':
    l = ['永康市雅致医疗器械有限公司', '郑云燕', 'II类:6863-16-定制式义齿',   '原料药', '津20170006', '2022/7/24', \
         '永康市雅致医疗器械有限公司2022-01-02 12:00:02.395', '2022-01-02 12:00:02.394 DEBUG ', '2022-01-02 12:00:02.397 DEBUG', '2022-01-02 12:00:02.396 ERROR ']

    parseDate(l)