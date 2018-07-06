# -*- coding: utf-8 -*-

def filter_key(key):
    '''
    将下划线字段转换为驼峰型字段
    :param key:
    :return:
    '''
    tmp = key.split('_')
    for i in range(1, len(tmp)):
        tmp[i] = tmp[i][0].upper() + tmp[i][1:]
    return ''.join(tmp)