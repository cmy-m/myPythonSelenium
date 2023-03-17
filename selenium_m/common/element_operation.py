#! /usr/bin/env python3
# _*_ coding: utf-8 _*_
# Copyright (C) mileschen

# 该文件封装用例的解析，可扩展
import json


def processing_element(_element_type, _element_value, browser):
    """
    处理页面元素查找操作
    :param _element_type: 查找元素的类型，id/name/classname/xpath/css
    :param _element_value: 查找元素的标签值
    :param browser: 浏览器对象，通过BaseBrowser类获取
    """
    _element = None
    # 处理元素查找
    if _element_type != 'Null' and not _element_type.endswith('_s'):
        # 处理单个元素
        if _element_type == 'css':
            _element = browser.by_css(css_selector=_element_value)
        elif _element_type == 'xpath':
            _element = browser.by_xpath(xpath=_element_value)
        elif _element_type == 'id':
            _element = browser.by_id(id=_element_value)
        elif _element_type == 'name':
            _element = browser.by_name(name=_element_value)
        elif _element_type == 'classname':
            _element = browser.by_classname(classname=_element_value)
    elif _element_type != 'Null' and _element_type.endswith('_s'):
        # 查询批量元素的属性值
        _elements_value = json.loads(_element_value)
        # 处理批量元素
        if _element_type == 'css_s':
            _element = browser.by_css(css_selector=_elements_value[0], is_list=True)[
                _elements_value[1]]
        elif _element_type == 'xpath_s':
            _element = browser.by_xpath(xpath=_elements_value[0], is_list=True)[_elements_value[1]]
        elif _element_type == 'id_s':
            _element = browser.by_id(id=_elements_value[0], is_list=True)[_elements_value[1]]
        elif _element_type == 'name_s':
            _element = browser.by_name(name=_elements_value[0], is_list=True)[_elements_value[1]]
        elif _element_type == 'classname_s':
            _element = browser.by_classname(classname=_elements_value[0], is_list=True)[
                _elements_value[1]]

        else:
            raise ValueError('{}不在元素定位方法定义的范围内'.format(_element_type))
    else:
        pass
    return _element


def processing_action(_element_action, _element=None, browser=None, _action_data=None):
    """
    处理页面元素动作操作
    :param _element_action: 动作类型
    :param _element: 查询到的元素对象，非必要参数，默认为None
    :param browser: 浏览器对象，通过BaseBrowser类获取， 非必要参数，默认为None
    :param _action_data: 操作动作需要的数据,非必要参数，默认为None
    """
    # 处理操作动作
    if _element_action != 'Null':
        if _element_action == 'send_keys':
            _element.send_keys(_action_data)
        elif _element_action == 'click':
            _element.click()
        elif _element_action == 'to_window':
            browser.switch_new_window()
        elif _element_action == 'to_alter':
            if _action_data == 'accept':
                browser.switch_to_alter()
            elif _action_data not in ['Null', 'dismiss']:
                browser.switch_to_alter(input_str=_action_data)
            else:
                browser.switch_to_alter(option='dismiss')
        elif _element_action == 'alter_txt':
            alter_txt = browser.get_alter_txt()
        elif _element_action == 'to_bottom':
            browser.scroll_to_bottom()
        elif _element_action == 'to_top':
            browser.scroll_to_top()
        else:
            pass


def processing_assert(_assert_value):
    """
    处理断言信息
    :param _assert_value: 预期的结果
    """
    assert _assert_value
