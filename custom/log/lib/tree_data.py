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
    max_idx = len(logs) - 2
    while idx <= max_idx:
        data_dict = logs[idx].to_dict()
        fo.write("\t\t" + json.dumps(data_dict) + ",\n")
        idx = idx + 1

    # 写入最后一条记录
    data_dict = logs[len(logs) - 1].to_dict()
    if is_last_logs:
        fo.write("\t\t" + json.dumps(data_dict) + "\n")
    else:
        fo.write("\t\t" + json.dumps(data_dict) + ",\n")

# if __name__ == '__main__':
#     fo = write_head("test_tree_data")
#     write_end(fo)
