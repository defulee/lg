#!/usr/bin/env python3
# -*- coding: UTF-8 -*-


def query_dict_meta(cursor, dict_key):
    sql = f"""
        select `id`
        from meta_store__dictionary_meta
        where `key`='{dict_key}';
    """

    cursor.execute(sql)
    ret = cursor.fetchall()
    if ret is None or len(ret) == 0:
        return None
    dict_id = ret[0][0]

    sql = f"""
        select `originalKey` as 字典值,
               `label` as 文案,
               if(`active`= 0, '未生效', '生效') as 生效状态
        from meta_store__dictionary_item_meta
        where `FromDictionary`= '{dict_id}'
        order by `displayOrder`;
    """
    cursor.execute(sql)
    return cursor.fetchall()


def query_dict_item_i18n(cursor, dict_key):
    sql = f"""
        SELECT `translation`, `originalKey` 
        FROM meta_store__i18n_dictionary_item_meta 
        WHERE locale = 'zh-CN' and  originalKey like '%\_{dict_key}\_%';
        """
    cursor.execute(sql)
    return cursor.fetchall()


def persist_dict_meta(cursor, dict_key, fo):
    print("persist dict:", dict_key)
    dict_meta = query_dict_meta(cursor, dict_key)
    if dict_meta is None or len(dict_meta) == 0:
        return
    # 国际化
    dict_item_i18n = query_dict_item_i18n(cursor, dict_key)

    lines = []
    # 字典信息
    lines += ["### " + dict_key]

    # 列名
    cols = ["字典值", "文案", "生效状态"]
    lines += ["| {} |".format(' | '.join(cols))]

    # 分割线
    lines += ["|" + " :- |" * len(cols)]

    # 数据部分
    for row in dict_meta:
        label = row[1]
        # 国际化
        key = dict_key + "_" + row[0]
        for item_i18n in dict_item_i18n:
            if key in item_i18n[1]:
                label = item_i18n[0]
        lines += ["| {} | {} | {} |".format(row[0], label, row[2])]

    for line in lines:
        fo.write(line + "\n")
    fo.write("\n")
