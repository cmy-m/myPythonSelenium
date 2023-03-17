#! /usr/bin/env python3
# _*_ coding: utf-8 _*_
# Copyright (C) mileschen
# 该文件用于selenium框架中常量的定义

from selenium_m.lib import r_w_file
import get_path


# case_head存储用例的基础信息，默认Excel前两行
# case_body存储用例信息，默认Excel第三行开始
# 当前是allure方式，取消allure方式可以is_allure=False
case_head, case_body = r_w_file.SeleniumCaseFile.read_selenium_case_excel(
    file_path=get_path.add_path('selenium_m/case_data/selenium_case.xlsx'), is_allure=True)

# webdriver配置文件地址
driver_ini_path = get_path.add_path('selenium_m/config/selenium_webdriver_config.ini')
