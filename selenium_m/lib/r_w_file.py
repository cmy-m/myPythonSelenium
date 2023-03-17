#! /usr/bin/env python3
# _*_ coding: utf-8 _*_
# Copyright (C) mileschen


import configparser
import os, json
import pandas as pd


class IniFile:
    @staticmethod
    def read_ini(file_path, sec):
        """
        读取配置文件（ini/cof）中制定的section配置,以字典的形式返回
        :param file_path:配置文件
        :param sec: 配置项
        :return:以字典形式返回,如果sec不在配置中返回{}
        """
        config = configparser.ConfigParser()
        config.read(filenames=file_path, encoding='utf8')
        sec_list = config.sections()
        if sec not in sec_list:
            return {}
        data = {}
        for item in config.items(section=sec):
            data.update({item[0]: item[1]})
        return data

    @staticmethod
    def write_ini(file_path: str, data):
        """
        写配置文件，支持修改，写入的数据类型必须为字典嵌套类型
        :return: 返回写入成功或失败
        :param file_path: 配置文件
        :param data: {sec:{opt:value}}
        """
        config = configparser.ConfigParser()
        config.read(filenames=file_path, encoding='utf8')
        # 判断写入的数据是否为字典嵌套类型
        if isinstance(data, dict):
            for x in data.values():
                if not isinstance(x, dict):
                    return '不是字典嵌套类型，写入失败'
        else:
            return '不是字典嵌套类型，写入失败'
        # 字典嵌套方式整体写入，支持多个
        config.read_dict(data)
        with open(file_path, 'w+', encoding='utf8') as f:
            config.write(f)
        return '配置更新成功'

    @staticmethod
    def delete_ini(file_path, sec_list):
        """
        删除配置中指定section的配置信息，支持批量删除
        :param file_path:
        :param sec_list:需要删除的section列表
        """
        config = configparser.ConfigParser()
        config.read(filenames=file_path, encoding='utf8')
        for sec in sec_list:
            config.remove_section(section=sec)
        with open(file=file_path, mode='w', encoding='utf8') as f:
            config.write(f)


class JsonFile:
    @staticmethod
    def write_json(json_file, dict_data):
        """
        将字典追加写入json文件中
        :param json_file:json文件路径
        :param dict_data:写入的字典数据
        """
        if os.path.exists(path=json_file) and len(dict_data) > 0:
            with open(file=json_file, mode='r', encoding='utf8') as f:
                data = json.load(fp=f)
                if len(data) == 0:
                    data = dict_data
                else:
                    for k, v in dict_data.items():
                        data.update({k: v})
            with open(file=json_file, mode='w', encoding='utf8') as f:
                json.dump(data, f, indent=4)
        else:
            with open(file=json_file, mode='w', encoding='utf8') as f:
                json.dump(dict_data, f, indent=4)

    @staticmethod
    def read_json(json_file):
        """
        读取json文件，返回字典类型
        :param json_file: json文件路径
        :return:字典形式返回
        """
        with open(file=json_file, mode='r', encoding='utf8') as f:
            return json.load(fp=f)

    @staticmethod
    def del_json(json_file, k_list):
        with open(file=json_file, mode='w', encoding='utf8') as f:
            dict_data = json.load(fp=f)
            for k in k_list:
                dict_data.pop(k)
            json.dump(dict_data, f)


class ExcelFile:
    @staticmethod
    def read_excel(file_path, sheet_name=0, header=0, nrows=None, is_clean=True):
        """
        读取Excel文件内容，返回字典，并将非整行整列为空的空值替换成字符串'Null'
        :param file_path: Excel文件路径
        :param sheet_name: 需要读取的sheet，默认第一个表
        :param header: 把第几行当作头部，默认第一行， 从0开始
        :param nrows: 读取前几行 从0开始
        :param is_clean: 是否对整行或者整列均为空/na值数据进行清洗，默认清洗，False表示不清洗
        :return:
        """
        pf = pd.read_excel(io=file_path, sheet_name=sheet_name, header=header, nrows=nrows)
        if is_clean:
            # 清洗整行为空/na的数据，修改原数据
            pf.dropna(how='all', inplace=True)
            # 清洗整列为空/na的数据，修改原数据
            pf.dropna(how='all', axis=1, inplace=True)
            # 清洗为空/na的值为指定内容，修改原数据
            pf.fillna('Null', inplace=True)
        return pf.to_dict(orient='record')

    @staticmethod
    def read_xls(file_path):
        pf = pd.read_csv(file_path)
        return pf.to_dict(orient='record')


class SeleniumCaseFile:
    @staticmethod
    def read_selenium_case_excel(file_path, is_allure=False):
        """
        读取selenium的Excel格式用例，分基础信息（前两行数据）和用例信息（第三行以后的数据）
        :param file_path: 文件路径
        :param is_allure: 是否使用allure生成测试报告，用于allure测试报告获取用例名称
        :return: 返回两个数据基础信息和用例信息 base_datas:list[dict], case_datas:list[(dict,str)]
        """
        # 获取基础信息，默认为表的前两行
        base_data = ExcelFile.read_excel(file_path=file_path, nrows=1)
        # 获取用例信息，默认从表的第三行开始
        case_datas = ExcelFile.read_excel(file_path=file_path, header=2)

        base_datas = []

        for x in base_data:
            for y in x.items():
                if y[1] == 'nan':
                    x.pop(y[0])
            base_datas.append(x)
        if is_allure:
            case_datas_allure = []
            for x in case_datas:
                for y in x.items():
                    if y[0] == 'case_name':
                        case_datas_allure.append((x, y[1]))
            return base_datas, case_datas_allure
        return base_datas, case_datas


if __name__ == '__main__':
    # print(IniFile.read_ini(file_path='/Users/cw/Desktop/miles/demo/common/config/db_config.ini', sec='db_1'))
    # d = ['miles234',{'host': '443434552', 'port': '11'}, 'cc', {'a': 'a'}]
    # print(write_ini(file_path='/Users/cw/Desktop/miles/demo/common/config/db_config.ini', data=d))
    # IniFile.delete_ini(file_path='/Users/cw/Desktop/miles/demo/common/config/db_config.ini', sec_list=['miles', 'cc'])
    # dict_da = {'miles': 'gdh', 'age': {'1': 2324, '2': '2'}, 'ccc': 22, 'bbbb': 'uyyy'}
    # JsonFile.write_json(json_file='/Users/cw/Desktop/miles/demo/common/config/json_config.json', dict_data=dict_da)
    # r = JsonFile.read_json(json_file='/Users/cw/Desktop/miles/demo/common/config/json_config.json')
    # print(r, type(r))
    e = ExcelFile.read_excel(file_path='/Users/cw/Desktop/miles/demo/testdata/case_data.xlsx')
    print(e)
