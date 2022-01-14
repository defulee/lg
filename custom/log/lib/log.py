#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import re
from enum import Enum


class LogType(Enum):
    """日志类型"""
    LogicFlow = "LogicFlow"
    LogicFunction = "LogicFunction"
    ExtensionPoint = "ExtensionPoint"
    DS = "DS"
    Cache = "Cache"
    Warn = "Warn"
    Error = "Error"
    Unknown = "Unknown"

    def desc(self):
        if self == LogType.LogicFlow:
            return "LogicFlow"
        elif self == LogType.LogicFunction:
            return "LogicFunction"
        elif self == LogType.ExtensionPoint:
            return "ExtensionPoint"
        elif self == LogType.DS:
            return "DS"
        elif self == LogType.Cache:
            return "Cache"
        elif self == LogType.Warn:
            return "Warn"
        elif self == LogType.Error:
            return "Error"
        elif self == LogType.Unknown:
            return "Unknown"


class LogStatus(Enum):
    """日志状态"""
    Start = "Start"
    End = "End"

    def desc(self):
        if self == LogStatus.Start:
            return "Start"
        elif self == LogStatus.End:
            return "End"


class Log:
    """日志"""
    keyword_types = [LogType.LogicFlow, LogType.LogicFunction, LogType.ExtensionPoint]

    def __init__(self, line, p_span_id):
        log_type, status = self.parse_log_type(line)
        self.type = log_type
        self.trace_id = self.parse_trace_id(line)
        self.span_id = self.parse_span_id(line)
        self.p_span_id = p_span_id
        self.keyword = self.parse_log_keyword(log_type, line)
        self.status = status
        self.request = self.parse_log_args(log_type, line) if status == LogStatus.Start else ""
        self.response = self.parse_log_args(log_type, line) if status == LogStatus.End else ""
        self.content = self.parse_log_content(log_type, line)

    def parse_trace_id(self, log):
        return str.split(log, ",")[1]

    def parse_span_id(self, log):
        return str.split(str.split(log, ",")[2], "]")[0]

    def is_warn_log(self, log):
        pattern = r'(^\d{4}[\D]\d{1,2}[\D]\d{1,2} \d{2}:\d{2}:\d{2}[\D]\d{3} WARN )'
        return re.search(pattern, log)

    def is_error_log(self, log):
        pattern = r'(^\d{4}[\D]\d{1,2}[\D]\d{1,2} \d{2}:\d{2}:\d{2}[\D]\d{3} ERROR )'
        return re.search(pattern, log)

    def parse_log_type(self, log):
        if "Start execute [LogicFlow] impl" in log:
            return LogType.LogicFlow, LogStatus.Start
        if "End execute [LogicFlow] impl" in log:
            return LogType.LogicFlow, LogStatus.End
        elif "Start execute [LogicFunction] impl" in log:
            return LogType.LogicFunction, LogStatus.Start
        elif "End execute [LogicFunction] impl" in log:
            return LogType.LogicFunction, LogStatus.End
        elif "Start execute [ExtensionPoint] impl" in log:
            return LogType.ExtensionPoint, LogStatus.Start
        elif "End execute [ExtensionPoint] impl" in log:
            return LogType.ExtensionPoint, LogStatus.End
        elif "executeByDB" in log:
            return LogType.DS, LogStatus.End
        elif "Current cache hash key" in log:
            return LogType.Cache, LogStatus.End
        elif self.is_warn_log(log):
            return LogType.Warn, LogStatus.End
        elif self.is_error_log(log):
            return LogType.Error, LogStatus.End
        else:
            return LogType.Unknown, LogStatus.End

    def parse_log_keyword(self, log_type, log):
        if log_type in self.keyword_types:
            pattern = r'(\[|\]|,)'
            return re.sub(pattern, "", str.split(log, " ")[17])
        elif log_type == "Cache":
            # 2022-01-02 12:00:05.701 INFO  [oms-runtime,4061e1c1-5c50-483a-aa57-384391c05592,9f651f15-c168-46e6-8e48-dadcd47f8001] - [ConsumeMessageThread_20] i.t.t.c.p.invoker.TrantorCacheHandler   : Current cache hash key: functionCache:v2:io.terminus.furniture.trade.cache.QueryShopCache, field: 212022
            pattern = r'(\[|\]|,)'
            return re.sub(pattern, "", str.split(str.split(log, " ")[15], ":")[2])
        elif log_type == "executeByDB":
            return ""
        elif log_type in [LogType.Warn, LogType.Error]:
            return str(log_type)
        else:
            return ""

    def parse_log_args(self, log_type, log):
        if log_type in self.keyword_types:
            return str.split(log, "], args: ")[1]
        else:
            return ""

    def parse_log_content(self, log_type, log):
        if log_type == LogType.DS:
            return str.split(log, "executeByDB, ")[1]
        elif log_type == LogType.Error:
            return str.split(log, ":")[4]
        else:
            return ""

    def to_dict(self):
        return {
            "type": self.type.desc(),
            "trace_id": self.trace_id,
            "span_id": self.span_id,
            "p_span_id": self.p_span_id,
            "keyword": self.keyword,
            "status": self.status.desc(),
            "request": self.request,
            "response": self.response,
            "content": self.content
        }
