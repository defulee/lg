#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import re
from enum import Enum


class LogType(Enum):
    """日志类型"""
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
        if self == LogType.LogicFlow:
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
    # 2022-01-20 14:47:39.623 INFO  [oms-runtime,6a008032fd10c17586795e2e18f4cfb8,c01c1c0c-acab-4f9e-9bcd-c4749c7a1066] - [http-nio-8080-exec-5] i.t.furniture.trade.utils.TimeWatch     : [TimeWatch '客审保存]' running time = 1141 ms
    # 2022-01-20 14:47:48.961 INFO  [oms-runtime,b3097e90c4878ff10b4741ff22c88acb,5afa9c5a-efdf-4608-88a9-613910f1c45a] - [http-nio-8080-exec-9] i.t.furniture.trade.utils.TimeWatch     : [TimeWatch-Step]: 查询组合订单; 合并订单:HB2022012000002200
    # 2022-01-20 14:47:48.988 INFO  [oms-runtime,b3097e90c4878ff10b4741ff22c88acb,469901db-bece-4d14-a07f-d1fad66ec47a] - [http-nio-8080-exec-9] .f.o.a.BuildChangeTradeOrderLineFuncImpl: [客审保存]- 更新商品行，toOccupyLineList:null | toCancelLineList:[566112]
    content = str.split(log, ": ")[1]
    return re.search(r'^\[.*\]', content, re.I | re.M) or content.startswith("TimeWatch-Step")


def parse_log_content(log):
    return log


def parse_log_type(log):
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
        if log_type in self.keyword_types:
            pattern = r'(\[|\]|,)'
            return '[' + log_type.desc() + '] ' + re.sub(pattern, "", str.split(log, " ")[17])
        elif log_type == LogType.Cache:
            # 2022-01-02 12:00:05.701 INFO  [oms-runtime,4061e1c1-5c50-483a-aa57-384391c05592,9f651f15-c168-46e6-8e48-dadcd47f8001] - [ConsumeMessageThread_20] i.t.t.c.p.invoker.TrantorCacheHandler   : Current cache hash key: functionCache:v2:io.terminus.furniture.trade.cache.QueryShopCache, field: 212022
            pattern = r'(\[|\]|,)'
            return '[Cache]' + re.sub(pattern, "", str.split(str.split(log, " ")[15], ":")[2])
        elif log_type == LogType.DB:
            # 2022-01-20 14:47:02.342 INFO  [oms-runtime,6d0a8c3c-304d-4378-a0a5-d445ec811f79,b1adfcbe-7846-4066-b80f-64c3f46c0623,requestId=lkrm1z9u33] - [ConsumeMessageThread_13] API_DS                                  : executeByDB, cost=3ms, gqlOrSql=DataStoreSqlDto{sqls=[SqlParam(sql=select `id`, `tradeOrderCode`, `_version` from furniture_trade_TradeOrderLineSO where id IN (?), params=[[566184, 566185, 566187]], isSearchSQL=false, language=null)]}, reqId=fa087bfc-4b70-406f-85e5-76bcf99d18c6
            # 2022-01-20 14:47:02.354 INFO  [oms-runtime,6d0a8c3c-304d-4378-a0a5-d445ec811f79,b1adfcbe-7846-4066-b80f-64c3f46c0623,requestId=lkrm1z9u33] - [ConsumeMessageThread_13] API_DS                                  : executeByDB, cost=12ms, gqlOrSql=DataStoreSqlDto{sqls=[SqlParam(sql=update furniture_trade_TradeOrderLineSO set orderStatus = 'TO_AUDIT' where `id` = 566184, params=null, isSearchSQL=false, language=null)]}, reqId=fa087bfc-4b70-406f-85e5-76bcf99d18c6
            # 2022-01-20 14:47:04.097 INFO  [oms-runtime,38e4f14e-7eb3-457f-9ed9-95470d135453,ba5d08dd-aee5-4858-b0e3-2acfa318c0cb] - [ConsumeMessageThread_2] API_DS                                  : executeByDB, cost=13ms, gqlOrSql=DataStoreSqlDto{sqls=[SqlParam(sql=insert into `furniture_trade_OpenClientFullOrderBO` (`originFee`, `paymentChannelDict`, `consignee`, `createMode`, `asStrideStorePromotion`, `postFee`, `channelOrderType`, `paidAmt`, `shippingStatus`, `buyerName`, `orderOutId`, `itemDiscountAmt`, `fullAddress`, `paymentInfo`, `invoice`, `outCreatedAt`, `status`, `skuAmt`, `shippingFeeOriginal`, `addressHashCode`, `shop`, `channelCode`, `payTime`, `shippingType`, `extra`, `outUpdatedAt`, `channel`, `shipFee`, `type`, `isO2OPayOrder`, `consigneeName`, `originAmountAndShip`, `handleStatus`, `errorStatus`, `consigneeMobile`, `_version`, `tradeType`, `paymentTypeDict`, `oaid`) values (10, 'ALIPAY', '{"@id":"@id:a4a2f3cb-b098-4e09-83e2-3412c0939f14","name":"彭**","mobile":"*******4877","province":"辽宁省","city":"葫芦岛市","region":"龙港区","street":"","detail":"龙*街道新区龙**街**号生态**局","md5":"b6f934256c4318a970d77f446f695517"}', 'SYSTEM_MADE', false, 0, 'fixed', 10, 'WAIT_DELIVERY', 'yljylj44877_2007', '2426912280197112551', 0, '辽宁省葫芦岛市龙港区龙*街道新区龙**街**号生态**局', '[{"@id":"@id:55c05fcc-3068-4c63-a8b5-801bfefe34c2","paySerialNo":"2022012022001162761413307490","payTime":1642661223000}]', '{"@id":"@id:99718612-dbe2-461e-aa02-5f4a25a7d053"}', 1642661214000, 'PAID', 10, 0, '948213186', 2785, 'TAOBAO', 1642661223000, 'express', '{"platformDiscount":"0"}', 1642661223000, '{"@id":"@id:7d76125c-cf21-4d22-8418-8d31f21064df","id":1,"channelCode":"TAOBAO","channelName":"天猫渠道"}', 0, 'NORMAL', false, '彭**', 10, 'NEED_DECRYPT', 'NO_ERROR', '*******4877', 1, 'NORMAL_SALE', 'ONLINE', '1k5EXIJJw5SqhNfNSI71uDrskHSrZBuQeBTccfzbWrwYmpARmV1mgEGDfic5J5L3gI6f1zmT'), params=null, isSearchSQL=false, language=null)]}, reqId=
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
            # 2022-01-20 14:48:20.820 INFO  [oms-runtime,898a94ba56dcd378dc4e28b79dbf1696,51d72b30-f330-4e28-928b-bc28621d3bde] - [http-nio-8080-exec-9] API_DS                                  : executeDSLByES, cost=41ms, dsl={"boolQueryBuilderSearch":{"boolQuery":{"must":[{"termQuery":{"field":"status","value":"TO_AUDIT"}},{"termQuery":{"field":"channelOrderCode","value":"SO22012000000003"}}]}},"index":"furniture_trade_TradeOrderLineSO","isCount":true,"searchSortOrderByList":[{"field":"groupOrderId","order":"DESC"},{"field":"tradeOrderCode","order":"DESC"}]}, reqId=
            model = str.split(str.split(log, ",\"index\":\"")[1], "\",")[0]
            return "[ES] index: " + model
        elif log_type in [LogType.Warn, LogType.Error, LogType.Custom]:
            # 2022-01-20 14:47:48.961 INFO  [oms-runtime,b3097e90c4878ff10b4741ff22c88acb,5afa9c5a-efdf-4608-88a9-613910f1c45a] - [http-nio-8080-exec-9] i.t.furniture.trade.utils.TimeWatch     : [TimeWatch-Step]: 查询组合订单; 合并订单:HB2022012000002200
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
        elif log_type == LogType.Custom:
            match = re.findall(r"\{.*(?=\})\}", log)
            return match[0] if match else log
        elif log_type == LogType.Error or log_type == LogType.Warn:
            match = re.findall(r"\{.*(?=\})\}", log)
            return match[0] if match else None
        else:
            return ""

    def parse_cost_time(self, log_type, log):
        if log_type == LogType.CostTime and "End recording total time, function:" in log:
            # End recording total time, function: [furniture_trade_LockConflictFunc], requestId: [02c0f6b0-d778-4560-ae6a-07facd1d5d97], cost: [5 ms]
            return str.split(log, ", cost: ")[1].replace("\n", "").replace("[", "").replace("]", "")
        elif log_type == LogType.DB:
            # 2022-01-20 14:47:02.342 INFO  [oms-runtime,6d0a8c3c-304d-4378-a0a5-d445ec811f79,b1adfcbe-7846-4066-b80f-64c3f46c0623,requestId=lkrm1z9u33] - [ConsumeMessageThread_13] API_DS                                  : executeByDB, cost=3ms, gqlOrSql=DataStoreSqlDto{sqls=[SqlParam(sql=select `id`, `tradeOrderCode`, `_version` from furniture_trade_TradeOrderLineSO where id IN (?), params=[[566184, 566185, 566187]], isSearchSQL=false, language=null)]}, reqId=fa087bfc-4b70-406f-85e5-76bcf99d18c6
            return str.split(str.split(log, ", cost=")[1], ", ")[0]
        elif log_type == LogType.ES:
            # 2022-01-20 14:48:20.820 INFO  [oms-runtime,898a94ba56dcd378dc4e28b79dbf1696,51d72b30-f330-4e28-928b-bc28621d3bde] - [http-nio-8080-exec-9] API_DS                                  : executeDSLByES, cost=41ms, dsl={"boolQueryBuilderSearch":{"boolQuery":{"must":[{"termQuery":{"field":"status","value":"TO_AUDIT"}},{"termQuery":{"field":"channelOrderCode","value":"SO22012000000003"}}]}},"index":"furniture_trade_TradeOrderLineSO","isCount":true,"searchSortOrderByList":[{"field":"groupOrderId","order":"DESC"},{"field":"tradeOrderCode","order":"DESC"}]}, reqId=
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
        return f"""
                        <tr data-tt-id="{self.id}" data-tt-parent-id="{self.pid}">
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
                        </tr>
        """
