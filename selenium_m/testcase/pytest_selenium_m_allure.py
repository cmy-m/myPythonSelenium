#! /usr/bin/env python3
# _*_ coding: utf-8 _*_
# Copyright (C) mileschen

# from base_browser import BaseBrowser
# from selenium_m.base_browser import BaseBrowser
import pytest
import allure
from selenium_m.common import constant
from selenium_m.common import element_operation


@allure.epic('selenium自动化')
@allure.feature('seventeen主页')
class TestSeleniumCase:

    @allure.description("这是用例描述：{case_name}")
    @allure.title("这是用例名：{case_name}")
    @pytest.mark.parametrize('case_data, case_name', constant.case_body)
    def test_case(self, get_browser, case_data, case_name):
        browser = get_browser

        TestSeleniumCase.test_case.__doc__ = "{}".format(case_data['case_name'])
        # 处理用例跳过判断
        if int(case_data['skip']) == 1:
            pytest.skip()
        # 查询元素的方法
        _element_type: str = case_data['element_type']
        # 查询单个元素的属性值
        _element_value: str = case_data['element_value']
        # 对元素的动作
        _element_action: str = case_data['element_action']
        # 查询批量元素的属性值
        # _elements_value = json.loads(case_data['element_value'])
        # 操作动作需要的值
        _action_data: str = str(case_data['data'])
        # 预期结果校验
        _assert_value: str = case_data['assert']
        with allure.step("开始执行用例"):
            # 处理页面元素查找
            _element = element_operation.processing_element(_element_type, _element_value, browser)
            # 处理页面操作动作
            element_operation.processing_action(_element_action, _element, browser, _action_data)
        with allure.step('断言'):
            # 处理断言
            element_operation.processing_assert(_assert_value)


if __name__ == '__main__':
    pytest.main()
