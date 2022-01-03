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
    empty_log = {
        "type": "Custom",
        "trace_id": "",
        "span_id": "",
        "p_span_id": "",
        "keyword": "",
        "cost": 0,
        "content": "",
        "status": "END",
        "request": "",
        "response": ""
    }
    fo.write("\t\t" + json.dumps(empty_log) + "\n")
    context = """\t],
    "count": 924,
    "is": true,
    "tip": "操作成功！"
}
    """
    fo.write(context + "\n")
    return fo


def add_records(fo, logs):
    for log in logs:
        fo.write("\t\t" + json.dumps(log) + ",\n")


# if __name__ == '__main__':
#     fo = write_head("test_tree_data")
#     write_end(fo)
