#!/usr/bin/python3
# -*- coding: UTF-8 -*-


def query_model_meta(cursor, model):
    sql = f"""
        select id
        from meta_store__model_meta
        where originalKey= '{model}' ;
    """

    cursor.execute(sql)
    ret = cursor.fetchall()
    if ret is None or len(ret) == 0:
        return None

    model_id = ret[0][0]

    sql = f"""
        select `originalKey` as 字段名称,
               `name` as 描述,
               `type` as 类型,
               ifnull(REPLACE(case
                                  JSON_EXTRACT(typeMeta, '$.type')
                                  when '"Dictionary"'
                                      then JSON_EXTRACT(typeMeta, '$.dictionaryKey')
                                  when '"Link"'
                                      then JSON_EXTRACT(typeMeta, '$.linkModel')
                                  when '"Json"'
                                      then JSON_EXTRACT(typeMeta, '$.model')
                                  when '"Lookup"'
                                      then JSON_EXTRACT(typeMeta, '$.lookupModel')
                                  end, '"', ''), '') as 关联模型,
               if(nullable= 0, '是', '否') as 必填,
               if(active= 0, '未生效', '生效') as 生效状态
        from meta_store__model_field_meta
        where FromModel= '{model_id}' and persistent=1
        order by `order`;
    """
    cursor.execute(sql)
    return cursor.fetchall()


def persist_model_meta(cursor, model, model_field_desc, fo):
    print("persist model name:", model["name"], ",desc:", model["desc"])
    mode_meta = query_model_meta(cursor, model["name"])
    if mode_meta is None:
        print("model:", model["name"], "not found")
        return

    lines = []
    # 模型信息
    lines += ["### " + model["desc"] + "--" + model["name"]]

    # 列名
    cols = ["字段名称", "描述", "类型", "关联模型", "必填", "生效状态"]
    lines += ["| {} |".format(' | '.join(cols))]

    # 分割线
    lines += ["|" + " :- |" * len(cols)]

    # 关联模型
    relate_meta = []
    # 数据部分
    for row in mode_meta:
        # 处理字段描述
        if model_field_desc is not None and row[0] in model_field_desc:
            lines += ["| {} | {} | {} | {} | {} | {} |".format(row[0], model_field_desc[row[0]], row[2], row[3], row[4],
                                                               row[5])]
        else:
            lines += ["| {} |".format(' | '.join(row))]

        # 收集关联模型
        if row[3] is not None and row[3] != "":
            relate_meta.append(row[3])

    for line in lines:
        fo.write(line + "\n")
    fo.write("\n")

    return relate_meta