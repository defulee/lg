#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import re
from enum import Enum


class LogType(Enum):
    """日志类型"""
    Trigger = "Trigger"
    LogicFlow = "LogicFlow"
    LogicFunction = "LogicFunction"
    ExtensionPoint = "ExtensionPoint"
    CostTime = "CostTime"
    DB = "DS"
    ES = "ES"
    Cache = "Cache"
    Warn = "Warn"
    Error = "Error"
    Custom = "Custom"
    Unknown = "Unknown"

    def desc(self):
        if self == LogType.Trigger:
            return "Trigger"
        elif self == LogType.LogicFlow:
            return "Flow"
        elif self == LogType.LogicFunction:
            return "Function"
        elif self == LogType.ExtensionPoint:
            return "Extension"
        elif self == LogType.CostTime:
            return "CostTime"
        elif self == LogType.DB:
            return "DB"
        elif self == LogType.ES:
            return "ES"
        elif self == LogType.Cache:
            return "Cache"
        elif self == LogType.Warn:
            return "Warn"
        elif self == LogType.Error:
            return "Error"
        elif self == LogType.Custom:
            return "Custom"
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


def parse_trace_id(log):
    return str.split(log, ",")[1]


def parse_span_id(log):
    return str.split(str.split(log, ",")[2], "]")[0]


def parse_time(log):
    return str.split(log, " ")[1]


def is_warn_log(log):
    pattern = r'(^\d{4}[\D]\d{1,2}[\D]\d{1,2} \d{2}:\d{2}:\d{2}[\D]\d{3} WARN )'
    return re.search(pattern, log)


def is_error_log(log):
    pattern = r'(^\d{4}[\D]\d{1,2}[\D]\d{1,2} \d{2}:\d{2}:\d{2}[\D]\d{3} ERROR )'
    return re.search(pattern, log)


def is_custom_log(log):
    content = str.split(log, ": ")[1]
    return re.search(r'^\[.*\]', content, re.I | re.M) or content.startswith("TimeWatch-Step")


def parse_log_content(log):
    return log


def parse_log_type(log):
    if "starting trigger: " in log:
        return LogType.Trigger, LogStatus.Start
    elif "finished trigger: " in log:
        return LogType.Trigger, LogStatus.End
    elif "Start execute [LogicFlow] impl" in log:
        return LogType.LogicFlow, LogStatus.Start
    elif "End execute [LogicFlow] impl" in log:
        return LogType.LogicFlow, LogStatus.End
    elif "Start execute [LogicFunction] impl" in log:
        return LogType.LogicFunction, LogStatus.Start
    elif "End execute [LogicFunction] impl" in log:
        return LogType.LogicFunction, LogStatus.End
    elif "Start execute [ExtensionPoint] impl" in log:
        return LogType.ExtensionPoint, LogStatus.Start
    elif "End execute [ExtensionPoint] impl" in log:
        return LogType.ExtensionPoint, LogStatus.End
    elif "End recording total time, function:" in log:
        return LogType.CostTime, LogStatus.End
    elif "executeByDB" in log:
        return LogType.DB, LogStatus.End
    elif "executeDSLByES" in log:
        return LogType.ES, LogStatus.End
    elif "Current cache hash key" in log:
        return LogType.Cache, LogStatus.End
    elif is_warn_log(log):
        return LogType.Warn, LogStatus.End
    elif is_error_log(log):
        return LogType.Error, LogStatus.End
    elif is_custom_log(log):
        return LogType.Custom, LogStatus.End
    else:
        return LogType.Unknown, LogStatus.End


class Log:
    """日志"""
    keyword_types = [LogType.LogicFlow, LogType.LogicFunction, LogType.ExtensionPoint]
    next_id = 1

    def __init__(self, line):
        log_type, status = parse_log_type(line)
        self.type = log_type
        self.trace_id = parse_trace_id(line)
        self.span_id = parse_span_id(line)
        self.id = Log.next_id
        self.pid = None
        self.keyword = self.parse_log_keyword(log_type, line)
        self.status = status
        self.request = self.parse_log_args(log_type, line) if status == LogStatus.Start else ""
        self.response = self.parse_log_args(log_type, line) if status == LogStatus.End else ""
        self.content = parse_log_content(line)
        self.cost = self.parse_cost_time(log_type, line)
        self.start_time = parse_time(line) if status == LogStatus.Start else None
        self.end_time = parse_time(line) if status == LogStatus.End else None
        Log.next_id = Log.next_id + 1

    def parse_log_keyword(self, log_type, log):
        if log_type == LogType.Trigger:
            trigger = str.split(str.split(log, " trigger: ")[1], " ")[0].replace("`", "")
            return "[Trigger] " + trigger
        elif log_type in self.keyword_types:
            pattern = r'(\[|\]|,)'
            return '[' + log_type.desc() + '] ' + re.sub(pattern, "", str.split(log, " ")[17])
        elif log_type == LogType.Cache:
            pattern = r'(\[|\]|,)'
            return '[Cache]' + re.sub(pattern, "", str.split(str.split(log, " ")[15], ":")[2])
        elif log_type == LogType.DB:
            if "DataStoreSqlDto{sqls=[SqlParam(sql=select" in log:
                model = str.split(str.split(log, " from ")[1], " ")[0].replace("`", "")
                return "[DB] select " + model
            elif "DataStoreSqlDto{sqls=[SqlParam(sql=update" in log:
                model = str.split(str.split(log, "sql=update ")[1], " set ")[0].replace("`", "")
                return "[DB] update " + model
            elif "DataStoreSqlDto{sqls=[SqlParam(sql=insert" in log:
                model = str.split(str.split(log, "sql=insert into ")[1], " ")[0].replace("`", "")
                return "[DB] insert " + model
            return ""
        elif log_type == LogType.ES:
            model = str.split(str.split(log, ",\"index\":\"")[1], "\",")[0]
            return "[ES] index: " + model
        elif log_type in [LogType.Warn, LogType.Error, LogType.Custom]:
            keyword = str.split(log, ": ", 1)[1]
            match = re.findall(r"\{.*(?=\})\}", keyword)
            return '[' + log_type.desc() + '] ' + keyword[0:keyword.index(match[0])] if match else keyword
        elif log_type == LogType.CostTime:
            pattern = r'(\[|\]|,)'
            return re.sub(pattern, "", str.split(log, " ")[18])
        else:
            return ""

    def parse_log_args(self, log_type, log):
        if log_type in self.keyword_types:
            return str.split(log, "], args: ")[1].replace("\n", "")
        elif log_type == LogType.ES:
            return str.split(str.split(log, ", dsl=")[1], ", reqId=")[0]
        elif log_type in [LogType.Warn, LogType.Error, LogType.Custom]:
            match = re.findall(r"\{.*(?=\})\}", log)
            return match[0] if match else ""
        else:
            return ""

    def parse_cost_time(self, log_type, log):
        if log_type == LogType.CostTime and "End recording total time, function:" in log:
            return str.split(log, ", cost: ")[1].replace("\n", "").replace("[", "").replace("]", "")
        elif log_type == LogType.DB:
            return str.split(str.split(log, ", cost=")[1], ", ")[0]
        elif log_type == LogType.ES:
            return str.split(str.split(log, ", cost=")[1], ", ")[0]
        return ""

    def to_dict(self):
        return {
            "type": self.type.desc(),
            "trace_id": self.trace_id,
            "span_id": self.span_id,
            "keyword": self.keyword,
            "status": self.status.desc(),
            # "request": self.request,
            # "response": self.response,
            # "content": self.content
        }

    def to_tr(self):
        op_str = f"""
                                <button type="button" class="btn btn-primary btn-sm" data-toggle="modal" data-target="#content-modal">原日志</button>"""
        if self.request is not None and self.request != "":
            op_str = op_str + f"""
                                <button type="button" class="btn btn-info btn-sm" data-toggle="modal" data-target="#json-modal">请求</button>"""
        if self.response is not None and self.response != "" and self.type in [LogType.LogicFlow, LogType.LogicFunction, LogType.ExtensionPoint]:
            op_str = op_str + f"""
                                <button type="button" class="btn btn-info btn-sm" data-toggle="modal" data-target="#json-modal">响应</button>"""
        elif self.response is not None and self.response != "":
            op_str = op_str + f"""
                                <button type="button" class="btn btn-info btn-sm" data-toggle="modal" data-target="#json-modal">Json内容</button>"""

        color = "text-dark"
        if self.type in [LogType.Error, LogType.Unknown]:
            color = "text-danger"
        elif self.type == LogType.Warn:
            color = "text-warning"

        return f"""
                        <tr data-tt-id="{self.id}" data-tt-parent-id="{self.pid}" class="{color}">
                            <td>{self.keyword}</td>
                            <td>{self.cost}</td>
                            <td>{self.start_time}</td>
                            <td>{self.end_time}</td>
                            <td>{self.status.desc()}</td>
                            <td style="display:none">{self.request}</td>
                            <td style="display:none">{self.response}</td>
                            <td style="display:none">{self.content}</td>
                            <td style="display:none">{self.type.desc()}</td>
                            <td style="display:none">{self.trace_id}</td>
                            <td style="display:none">{self.span_id}</td>
                            <td>{op_str}</td>
                        </tr>
        """
