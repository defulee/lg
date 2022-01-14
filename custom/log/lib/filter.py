#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import re


class Filter:
    def __init__(self, log_file, trace_id):
        self.log_file = log_file
        self.trace_id = trace_id
        self.lines = []

    def match_log_start(self, line):
        pattern = r'(^\d{4}[\D]\d{1,2}[\D]\d{1,2} \d{2}:\d{2}:\d{2}[\D]\d{3} (DEBUG|INFO|ERROR|WARN) )'
        return re.search(pattern, line)

    def parse_trace_id(self, log):
        return str.split(log, ",")[1]

    def filter(self):
        last_trace_id = None
        fr = open(self.log_file, "r")
        while True:
            line = fr.readline()
            if not line:  # 等价于if line == "":
                break
            is_new_log = self.match_log_start(line)
            if is_new_log:
                trace_id = self.parse_trace_id(line)
                if trace_id == self.trace_id:
                    self.lines.append(line)
                last_trace_id = trace_id
            elif last_trace_id is not None and last_trace_id == self.trace_id:
                # 原log，新行，如 error log
                self.lines.append(line)
