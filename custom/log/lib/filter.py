#!/usr/local/bin/python3.7
# -*- coding:utf-8 -*-

import re
from tree_data import write_head, write_end, add_records


def match_log_start(log):
    pattern = r'(^\d{4}[\D]\d{1,2}[\D]\d{1,2} \d{2}:\d{2}:\d{2}[\D]\d{3} (DEBUG|INFO|ERROR|WARN) )'
    return re.search(pattern, log)


def parse_trace_id(log):
    return str.split(log, ",")[1]


def parse_span_id(log):
    return str.split(str.split(log, ",")[2], "]")[0]


def parse_log_type(log):
    if "Start execute [LogicFlow] impl" in log:
        return "LogicFlow", "Start"
    if "End execute [LogicFlow] impl" in log:
        return "LogicFlow", "End"
    elif "Start execute [LogicFunction] impl" in log:
        return "LogicFunction", "Start"
    elif "End execute [LogicFunction] impl" in log:
        return "LogicFunction", "End"
    elif "Start execute [ExtensionPoint] impl" in log:
        return "ExtensionPoint", "Start"
    elif "End execute [ExtensionPoint] impl" in log:
        return "ExtensionPoint", "End"
    elif "executeByDB" in log:
        return "DS", "End"
    elif "Current cache hash key" in log:
        return "Cache", "End"
    elif "Exception" in log:
        return "Exception", "End"


def parse_log_keyword(log_type, log):
    if log_type in keyword_types:
        pattern = r'(\[|\]|,)'
        return re.sub(pattern, "", str.split(log, " ")[17])
    elif log_type == "Cache":
        # 2022-01-02 12:00:05.701 INFO  [oms-runtime,4061e1c1-5c50-483a-aa57-384391c05592,9f651f15-c168-46e6-8e48-dadcd47f8001] - [ConsumeMessageThread_20] i.t.t.c.p.invoker.TrantorCacheHandler   : Current cache hash key: functionCache:v2:io.terminus.furniture.trade.cache.QueryShopCache, field: 212022
        pattern = r'(\[|\]|,)'
        return re.sub(pattern, "", str.split(str.split(log, " ")[15], ":")[2])
    elif log_type == "executeByDB":
        return ""
    elif log_type == "Exception":
        return ""
    else:
        return ""


def parse_log_request(log_type, log):
    if log_type in keyword_types:
        return str.split(log, "], args: ")[1]
    else:
        return ""


def parse_log_response(log_type, log):
    if log_type in keyword_types:
        return str.split(log, "], args: ")[1]
    else:
        return ""


def match_log(log_type, keyword):
    for idx in range(len(trace_logs) - 1, -1, -1):
        if trace_logs[idx]["type"] == log_type and trace_logs[idx]["keyword"] == keyword:
            return idx
    return None


if __name__ == '__main__':
    keyword_types = ["LogicFlow", "LogicFunction", "ExtensionPoint"]
    trace_logs = []

    last_log = {
        "type": "Custom",
        "trace_id": "",
        "span_id": "",
        "p_span_id": "",
        "keyword": "",
        "cost": 0,
        "content": "",
        "status": "Start",
        "request": "",
        "response": ""
    }

    lines = [
        """2022-01-02 12:00:05.178 DEBUG [oms-runtime,2317235a-e695-42f5-9f75-6834300bdc75,bea98ece-20f4-45e4-8c3f-5a3738e59226] - [http-nio-8080-exec-1] i.t.t.s.i.FunctionInvokerComposite      : Start execute [LogicFlow] impl [furniture_trade_PullTaoBaoRefundFlowImpl], args: {"channelShop":{"@id":"@id:0fd64fe8-ef9e-40c8-bc00-a304233bd115","id":44002,"_version":5,"createdAt":1630466480000,"updatedAt":1638507974000,"createdBy":{"@id":"@id:9556e458-be48-479b-b40e-e3558361c4da","id":42001},"updatedBy":{"@id":"@id:4609ea2b-7f35-4612-b181-3c836649972d","id":6001},"siteCode":"SHP1630466480015","siteName":"三一测试淘宝店","siteType":"SHOP","isVirtualSite":false,"channel":{"@id":"@id:c290335e-62b6-4c00-a496-a73d74293a99","id":1,"_version":1,"createdAt":1614415445000,"updatedAt":1614415445000,"channelCode":"TAOBAO","channelName":"天猫渠道","channelType":"ONLINE","channelStatus":"ENABLED","isDeleted":false,"deletedAt":0},"siteStatus":"ENABLED","accessToken":"111","appKey":"111","appSecret":"111","gateWay":"111","salePrice":{"@id":"@id:f805e756-e787-4d32-b2f0-c733c4377dbe","id":12001},"isDeleted":false,"deletedAt":0}}""",
        """2022-01-02 12:00:05.701 INFO  [oms-runtime,2317235a-e695-42f5-9f75-6834300bdc75,9f651f15-c168-46e6-8e48-dadcd47f8001] - [http-nio-8080-exec-1] i.t.t.c.p.invoker.TrantorCacheHandler   : Current cache hash key: functionCache:v2:io.terminus.furniture.trade.cache.QueryShopCache, field: 212022""",
        """2022-01-02 12:00:05.701 DEBUG [oms-runtime,2317235a-e695-42f5-9f75-6834300bdc75,bea98ece-20f4-45e4-8c3f-5a3738e59226] - [http-nio-8080-exec-1] i.t.t.s.i.FunctionInvokerComposite      : End execute [LogicFlow] impl [furniture_trade_PullTaoBaoRefundFlowImpl], args: {"@id":"@id:dfefb14d-8a03-4ef8-b527-54d7598f73a8","id":462138,"_version":8,"createdAt":1634744200000,"updatedAt":1639484423000,"status":"FULFILLED","orderOutId":"2061264269554124501","buyerName":"花大姐2007","shippingStatus":"FINISH","tradeType":"PRE_SALE","createMode":"SYSTEM_MADE","outCreatedAt":1634743575000,"outUpdatedAt":1639484043000,"channel":{"@id":"@id:6b9d259a-f37f-412f-a333-3780fed88bf5","id":1,"_version":1,"createdAt":1614415445000,"updatedAt":1614415445000,"channelCode":"TAOBAO","channelName":"天猫渠道","channelType":"ONLINE","channelStatus":"ENABLED","deletedAt":0,"isDeleted":false},"shop":{"@id":"@id:d619ece0-d0b1-475c-9440-61b69057757c","id":212022},"paymentChannelDict":"NONE","paymentTypeDict":"ONLINE","originFee":362800,"paidAmt":362800,"itemDiscountAmt":0,"skuAmt":362800,"shippingFeeOriginal":0,"shipFee":0,"depositPayAmt":10000,"originAmountAndShip":362800,"sellerRemark":"【售中熊大/山茶】【】【】【101135】销售1中心-杨敏（繁星)","consignee":{"@id":"@id:69eb6dac-e5b7-43c8-8b88-45ee5d2efb56","name":"汪锋","mobile":"18907297800","province":"湖北省","city":"武汉市","region":"武昌区","street":"中南路街街道","detail":"中南路街街道武珞路336号佳兆业广场天御3栋1单元34楼","md5":"92f6590ac27aa5b209fb5109552607d8","md5":"92f6590ac27aa5b209fb5109552607d8"},"consigneeName":"汪锋","consigneeMobile":"18907297800","invoice":{"@id":"@id:e789becf-abb9-46ff-a0b3-f791ad14691f"},"paymentInfo":[{"@id":"@id:4ea5d7ba-3dd4-4f32-8674-0742e835a4f1","paidAmt":"3628","paySerialNo":"2021102022001209585735269472","payTime":1634743594000}],"stepStatus":"PAID","extra":{"platformDiscount":"0"},"type":"DEPOSIT_PAID","handleStatus":"CONVERT_FAIL","tmserSpuCode":"家装干支装服务","shippingType":"free","finalPaidTime":1638620411000,"failedReason":"商品活动价获取失败，请检查或补充商品价目套信息","addressHashCode":"-1204126923","addressMd5":"92f6590ac27aa5b209fb5109552607d8","fullAddress":"湖北省武汉市武昌区中南路街街道中南路街街道武珞路336号佳兆业广场天御3栋1单元34楼","asStrideStorePromotion":false,"oaid":"1lKjYE3NmGqD5aia8gXfibgk55S5myVgiczf20taKZOmpXhoAu1uibEGDhopVHzVSgDXmLC4bYO","channelOrderType":"step","verificationStatus":"NULL","isDeleted":false,"deletedAt":0}"""
    ]

    fo = write_head("test_tree_data")
    for line in lines:
        is_new_log = match_log_start(line)
        if is_new_log:
            trace_id = parse_trace_id(line)
            span_id = parse_span_id(line)
            if trace_id != last_log["trace_id"]:
                print("新请求")
                # 将上一个trace的日志记录下来
                if len(trace_logs) > 0:
                    add_records(fo, trace_logs)
                log_type, status = parse_log_type(line)
                last_log = {
                    "trace_id": trace_id,
                    "span_id": span_id,
                    "p_span_id": "",
                    "type": log_type,
                    "status": status,
                    "keyword": parse_log_keyword(log_type, line),
                    "request": parse_log_request(log_type, line)
                }

                print(last_log)
                trace_logs.append(last_log)
            else:
                log_type, status = parse_log_type(line)
                # 新span有三种可能性：1. 进入孩子节点；2. 进入兄弟节点；3. 回到父亲节点
                # 1. 进入孩子节点: 当前节点status未到End
                # 2. 进入兄弟节点：当前节点status为End，新节点和当前节点span_id相同
                # 3. 回到父亲节点：当前节点status为End，新节点和当前节点span_id不同
                if span_id != last_log["span_id"]:
                    if last_log["status"] != "End":
                        # 进入孩子节点: 当前节点status未到End
                        print("进入孩子节点")
                        p_span_id = last_log["span_id"]
                        last_log = {
                            "trace_id": trace_id,
                            "span_id": span_id,
                            "p_span_id": p_span_id,
                            "type": log_type,
                            "status": status,
                            "keyword": parse_log_keyword(log_type, line),
                            "request": parse_log_request(log_type, line)
                        }
                        trace_logs.append(last_log)
                        print(last_log)
                    else:
                        # 回到父亲节点：当前节点status为End，新节点和当前节点span_id不同
                        # 当前节点是上一个节点的父节点
                        print("回到父亲节点")
                        last_log["p_span_id"] = span_id
                        keyword = parse_log_keyword(log_type, line)
                        idx = match_log(log_type, keyword)
                        if idx is not None:
                            trace_logs[idx]["response"] = parse_log_response(log_type, line)
                            print(trace_logs[idx])
                else:
                    # 进入兄弟节点：当前节点status为End，新节点和当前节点span_id相同
                    print("进入兄弟节点")
                    p_span_id = last_log["p_span_id"]
                    last_log = {
                        "trace_id": trace_id,
                        "span_id": span_id,
                        "p_span_id": p_span_id,
                        "type": log_type,
                        "status": status,
                        "keyword": parse_log_keyword(log_type, line),
                        "request": parse_log_request(log_type, line)
                    }
                    trace_logs.append(last_log)
                    print(last_log)
                print("else")

    if len(trace_logs) > 0:
        add_records(fo, trace_logs)
    write_end(fo)
