#!/usr/local/bin/python3.7
# -*- coding:utf-8 -*-
import json
import os


def write_head(file_name):
    fo = open(os.getcwd() + "/" + file_name + ".json", "w")
    context = """{
    "msg": "",
    "code": 0,
    "data": ["""
    fo.write(context + "\n")
    return fo


def write_end(fo):
    context = """\t],
    "count": 924,
    "is": true,
    "tip": "操作成功！"
}
    """
    fo.write(context + "\n")
    return fo


def write_records(fo, logs, is_last_logs=False):
    if len(logs) == 0:
        return
    idx = 0
    while idx < len(logs):
        data_dict = logs[idx].to_dict()
        fo.write("\t\t" + json.dumps(data_dict) + ",\n")
        idx = idx + 1

    # 写入最后一条记录
    data_dict = logs[len(logs) - 1].to_dict()
    if is_last_logs:
        fo.write("\t\t" + json.dumps(data_dict) + "\n")
    else:
        fo.write("\t\t" + json.dumps(data_dict) + ",\n")


def write_html(file, logs):
    """
     将替换的字符串写到一个新的文件中，然后将原文件删除，新文件改为原来文件的名字
     :param file: 文件路径
     :param logs: 待写入logs
     :return: None
     """
    template_file = os.path.dirname(__file__) + "/template.html"

    treetable_body = ""
    if len(logs) == 0:
        return
    for idx in range(len(logs)):
        data_tr = logs[idx].to_tr()
        treetable_body = treetable_body + data_tr

    with open(template_file, "r", encoding="utf-8") as f1, open(file, "w", encoding="utf-8") as f2:
        for line in f1:
            if "{{treetable_body}}" in line:
                line = line.replace("{{treetable_body}}", treetable_body)
            f2.write(line)


if __name__ == '__main__':
    print(os.path.dirname(__file__))
    print(__file__)
