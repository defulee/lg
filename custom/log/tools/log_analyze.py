#!/usr/bin/env python3
# -*- coding:utf-8 -*-
### 日志格式化解析工具

import argparse
import re
import subprocess

from custom.log.lib.filter import Filter
from custom.log.lib.log import LogType, Log, LogStatus
from custom.log.lib.tree_data import write_html


def get_args():
    parser = argparse.ArgumentParser()
    parser.description = '参数解析'
    parser.add_argument('-t', '--trace_id', required=True, help='traceId')
    parser.add_argument('-f', '--file', required=True, help='log file')
    args = parser.parse_args()
    return args.file, args.trace_id


def match_log_start(log):
    pattern = r'(^\d{4}[\D]\d{1,2}[\D]\d{1,2} \d{2}:\d{2}:\d{2}[\D]\d{3} (DEBUG|INFO|ERROR|WARN) )'
    return re.search(pattern, log)


def match_log(log_type, keyword):
    for idx in range(len(trace_logs) - 1, -1, -1):
        if trace_logs[idx].type == log_type and trace_logs[idx].keyword == keyword and trace_logs[
            idx].status == LogStatus.Start:
            return idx
    return None


if __name__ == '__main__':
    log_file, trace_id = get_args()
    # -f /Users/defu/Downloads/90a57f7ad8f9a8579a1fccc8ce638377693510f4522f7a09e323f9c035a83ca0-1642661220419000000-1642661400419000000.log -t 6a008032fd10c17586795e2e18f4cfb8
    # log_file = "/Users/defu/Downloads/test.log"
    # trace_id = "f950df6af0ad3adfbcb9613a83cf1f8d"

    trace_logs = []
    last_log = None

    log_filter = Filter(log_file, trace_id)
    log_filter.filter()
    for line in log_filter.lines:
        is_new_log = match_log_start(line)
        if is_new_log:
            # 新 log 行
            log = Log(line)
            if log.keyword == "":
                continue
            print(log.to_dict())
            if log.type == LogType.Unknown:
                continue
            if last_log is None:
                print("新请求")
                last_log = log
                trace_logs.append(last_log)
            else:
                if log.type == LogType.CostTime:
                    last_log.cost = log.cost
                elif log.span_id != last_log.span_id:
                    # 新span有三种可能性：1. 进入孩子节点；2. 进入兄弟节点；3. 回到父亲节点
                    # 1. 进入孩子节点: 当前节点status未到End
                    # 2. 进入兄弟节点：当前节点status为End，新节点和当前节点span_id相同
                    # 3. 回到父亲节点：当前节点status为End，新节点和当前节点span_id不同
                    if last_log.status != LogStatus.End:
                        # 进入孩子节点: 当前节点status未到End
                        print("进入孩子节点")
                        log.pid = last_log.id
                        last_log = log
                        trace_logs.append(last_log)
                    else:
                        # 回到父亲节点：当前节点status为End，新节点和当前节点span_id不同
                        # 当前节点是上一个节点的父节点
                        print("回到父亲节点")
                        idx = match_log(log_type=log.type, keyword=log.keyword)
                        if idx is not None:
                            last_log = trace_logs[idx]
                            last_log.response = log.response
                            last_log.status = log.status
                            last_log.end_time = log.end_time
                else:
                    # 进入兄弟节点：当前节点status为End，新节点和当前节点span_id相同
                    print("进入兄弟节点")
                    log.pid = last_log.pid
                    last_log = log
                    if log.status == LogStatus.End:
                        idx = match_log(log.type, log.keyword)
                        if idx is not None:
                            last_log = trace_logs[idx]
                            last_log.response = log.response
                            last_log.status = LogStatus.End
                            last_log.end_time = log.end_time
                        else:
                            trace_logs.append(last_log)
                    else:
                        trace_logs.append(last_log)
        elif last_log.type == LogType.Error or last_log.type == LogType.Warn or last_log.type == LogType.Custom:
            # 原log，新行，如 error log
            last_log.content = last_log.content + line + "\n"

    if len(trace_logs) > 0:
        target_file = log_file.replace(".log", ".html")
        print("解析后文件：", target_file)
        write_html(target_file, trace_logs)
        subprocess.call(["open", target_file])
