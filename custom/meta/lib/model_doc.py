#!/usr/bin/python3
# -*- coding: UTF-8 -*-


def query_model_meta(cursor, model):
    sql = f"""
        select `id`
        from meta_store__model_meta
        where `key`= '{model}' ;
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


def query_model_fields_i18n(cursor, model):
    sql = f"""
        SELECT `translation`, `originalKey` 
        FROM meta_store__i18n_model_field_meta 
        WHERE locale = 'zh-CN' and  originalKey like '%\_{model}\_%';
        """
    cursor.execute(sql)
    return cursor.fetchall()


def persist_model_meta(cursor, model_key, model_desc, model_field_desc, fo):
    print("persist model name:", model_key, ",desc:", model_desc)
    mode_meta = query_model_meta(cursor, model_key)
    if mode_meta is None:
        print("model:", model_key, "not found")
        return []
    # 国际化
    model_fields_i18n = query_model_fields_i18n(cursor, model_key)

    lines = []
    # 模型信息
    if model_desc is None:
        lines += ["### " + model_key]
    else:
        lines += ["### " + model_desc + "--" + model_key]

    # 列名
    cols = ["字段名称", "描述", "类型", "关联模型", "必填", "生效状态"]
    lines += ["| {} |".format(' | '.join(cols))]

    # 分割线
    lines += ["|" + " :- |" * len(cols)]

    # 关联模型
    relate_meta = []
    # 数据部分
    for row in mode_meta:
        label = row[1]
        # 国际化
        key = model_key + "_" + row[0]
        for field_i18n in model_fields_i18n:
            if key in field_i18n[1]:
                label = field_i18n[0]
        # 配置文件中字段文案
        if model_field_desc is not None and row[0] in model_field_desc:
            label = model_field_desc[row[0]]

        lines += ["| {} | {} | {} | {} | {} | {} |".format(row[0], label, row[2], row[3], row[4], row[5])]

        # 收集关联模型
        if row[3] is not None and row[3] != "":
            relate_meta.append(row[3])

    for line in lines:
        fo.write(line + "\n")
    fo.write("\n")

    return relate_meta
