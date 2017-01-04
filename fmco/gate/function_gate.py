# -*- coding: utf-8 -*-

import os
import re
import logging

import util
from fmco.exceptions import FuncConfNofoundError
from fmco.gate.function_gate_config import *
from util import Singleton, time_util
from util import env_util
from util import geo_util
__author__ = 'lvyi'

logger = util.logger


@Singleton
class SettingsInitService():

    def load_config_item(self, key):
        # 在settings中调用，通过http请求config服务，获得配置参数
        pass


@Singleton
class SmartConfigService():

    _cache_check_time = 2*60
    _last_load_time = 0

    _config_data = {}

    # self_ip = "0.0.0.0"

    # other_load_url = None  #"/api/smartconfig/other_load"
    #
    # def __init__(self, other_load_url):
    #     self.other_load_url = other_load_url
    #     # 获得本机的ip和端口
    #     # 提交给配置服务器
    #     # 如果配置服务器，发起刷新操作，需要根据IP list调用force_load
    #     pass
    #
    # # 提供给配置服务器调用，可以立即更新缓存
    # def force_load(self, key, ip_list):
    #     # 更新本地服务
    #     self.reload(key)
    #     # 遍历其他服务器
    #     for ip in ip_list:
    #         if ip not in ip_list:
    #             self.force_other(key, ip)
    #
    # # 请求其他的服务器，other_load
    # def force_other(self, key, ip):
    #     url = self.other_load_url
    #     req_data = {"key":key}
    #     pass
    #
    # # 提供给其他服务器调用
    # def other_load(self, key):
    #     self.reload(key)

    # 提供配置数据，定时从缓存刷新
    def get_conf(self, key):
        if self._last_load_time == 0 or \
                (time_util.get_timestamp() - self._last_load_time > self._cache_check_time
                 and self._last_load_time>0):
            self.reload(key)
            self._last_load_time = time_util.get_timestamp()

        conf = self._config_data[key]
        if not conf:
            conf = self.reload(key)
        return conf

    # 从缓存服务器加载数据
    def reload(self, key):
        data = {"a": time_util.get_timestamp()}
        self._config_data[key] = data
        return data


# def func_configs():
#     func_dict = {}
#
#     func_dict[gate_func__home_service_add_review_decay] = \
#         FuncConf(gate_func__home_service_add_review_decay,
#                  [CtrlTypeConf(ctrl_type__internal_users, {"user_ids":[123,3234,332,4442]})])
#
#     func_dict[gate_func__search_cat_radius_ctrl] = \
#         FuncConf(gate_func__search_cat_radius_ctrl,
#                  [CtrlTypeConf(ctrl_type__location_radius, {"lat":32.837308,"lon":-96.776397,"radius":80000})])
#
#     return func_dict


@Singleton
class FunctionConfigService():

    configs_data = None
    func_conf_key = "func_gate_conf"

    def get_configs(self):
        return self.configs_data        # func_configs()

    def get_employee_ids(self):
        return employee_ids

    def get_employee_ids_for_test(self):
        return employee_ids_for_test

    def load_and_parse_configs(self):

        # todo configs_json = SmartConfigService().get_conf(self.func_conf_key)
        try:
            configs_json = default_configs_json

            func_dict = {}
            for config_item in configs_json:
                ctrls_list = []
                ctrl_config = config_item.get('ctrls', None)
                ctrl_name = config_item['name']
                logger.debug("parse ctrl_name=%s", ctrl_name)

                try:
                    if isinstance(ctrl_config, list):
                        # 解析旧版模板
                        ctrl_config = config_item.get('ctrls', None)
                        for ctrl in ctrl_config:
                            ctrls_list.append(CtrlTypeConf(ctrl['name'], ctrl.get('values',None)))

                        func_dict[ctrl_name] = FuncConf(ctrl_name,
                                                        ctrls_list,
                                                        config_item.get("open_all", False),
                                                        ctrl_method=config_item.get("ctrl_method", ctrl_method__and))
                    elif isinstance(ctrl_config, dict):
                        # 解析新版模板
                        func_dict[ctrl_name] = FuncComplexConf(ctrl_name, ctrl_config)
                except Exception as e:
                    logger.error("load_and_parse_configs=%s, err=%s", ctrl_name, e, exc_info=True)

            self.configs_data = func_dict
            # logger.debug(self.configs_data)
        except Exception as e:
            logger.error("load_and_parse_configs=%s" % e, exc_info=True)


class CtrlTypeConf(object):
    # name = None
    # values = {}
    def __init__(self, name, values):
        self.name = name
        if values:
            self.values = values
        else:
            self.values = {}

    def __str__(self):
        return "CtrlTypeConf[%s,%s]" % (self.name, self.values)


class FuncConf(object):
    # name = None
    # open_all = False
    # ctrl_method = ctrl_method__and
    # ctrl_type_list = []
    def __init__(self, name, ctrl_type_list, open_all, ctrl_method=ctrl_method__and):
        self.name = name
        self.open_all = open_all
        self.ctrl_method = ctrl_method
        self.ctrl_type_list = ctrl_type_list


class FuncComplexConf(object):
    def __init__(self, name, complex_config, open_all=False):
        self.name = name
        self.open_all = open_all
        self.complex = complex_config

        logger.debug("complex_config = %s,%s", name, complex_config)
        self.values = self.parse(complex_config)
        logger.debug("values parsed= %s", self.values)

    def __str__(self):
        return "FuncComplexConf[%s,%s]" % (self.name, self.values)

    def parse(self, complex_values):

        values = {}
        # logger.debug(complex_values)

        for (it_name, it_values) in complex_values.items():
            if isinstance(it_values, list):
                new_list = []
                for it in it_values:
                    new_list.append(self.parse(it))
                values[it_name] = new_list
            else:
                values[it_name] = CtrlTypeConf(it_name, it_values)

        return values

basedata_client = None

@Singleton
class FunctionGateService:

    sys_params = {}
    ctrl_types = {}

    def __init__(self):
        self.ctrl_types[ctrl_type__location_radius] = CtrlTypeLocationRadius()
        self.ctrl_types[ctrl_type__internal_users] = CtrlTypeInternalUsers()
        self.ctrl_types[ctrl_type__test_users] = CtrlTypeTestUsers()
        self.ctrl_types[ctrl_type__user_id_mod] = CtrlTypeUserIdMod()
        self.ctrl_types[ctrl_type__user_id_parity] = CtrlTypeUserIdParity()

        self.ctrl_types[ctrl_type__env_test] = CtrlTypeEnvTest()
        self.ctrl_types[ctrl_type__env_not_prod] = CtrlTypeEnvNotProd()
        self.ctrl_types[ctrl_type__env_not_test] = CtrlTypeEnvNotTest()

        self.ctrl_types[ctrl_type__android_only] = CtrlTypeAndroidOnly()
        self.ctrl_types[ctrl_type__iphone_only] = CtrlTypeIphoneOnly()
        self.ctrl_types[ctrl_type__new_user] = CtrlTypeNewUser()
        self.ctrl_types[ctrl_type__date_between] = CtrlTypeDateTimeBetween()
        self.ctrl_types[ctrl_type__dma] = CtrlTypeDMA()
        self.ctrl_types[ctrl_type__app_version] = CtrlTypeAppVersion()
        self.ctrl_types[ctrl_type__and] = CtrlTypeAnd()
        self.ctrl_types[ctrl_type__or] = CtrlTypeOr()

        FunctionConfigService().load_and_parse_configs()

    def is_gate_open(self, func_name, req_params):
        try:

            if not req_params:
                raise RuntimeError("req_params = None")

            # logger.debug("is_open user_id=%s" % req_params.user_id)
            if not self.gate_enable():
                # logger.debug("is_open env=False")
                is_open = False
                raise RuntimeError("is_open env=False")

            func_conf = self.get_func_conf(func_name)
            # logger.debug(func_conf)
            if func_conf and func_conf.open_all is True:
                # 该控制门已经完全打开
                is_open = True
            else:
                if isinstance(func_conf, FuncConf):
                    is_open = self.gate_ctrl(func_conf, req_params)
                elif isinstance(func_conf, FuncComplexConf):
                    is_open = self.gate_ctrl_for_complex(func_conf, req_params)

            logger.debug("is_open=%s,:%s", func_conf.name, is_open)
        except FuncConfNofoundError as e:
            logger.warning("FuncConfNofoundError =%s, %s, %s" % (e, func_name, req_params), exc_info=True)
            is_open = False
        except Exception as e:
            logger.warning("is_open error=%s, %s, %s" % (e, func_name, req_params), exc_info=True)
            is_open = False
        finally:
            return 1 if is_open else 0

    def get_func_conf(self, func_name):
        conf = FunctionConfigService().get_configs().get(func_name, None)
        if not conf:
            raise FuncConfNofoundError(func_name)
        return conf

    def get_ctrl_by_name(self, ctrl_name):
        return self.ctrl_types.get(ctrl_name, None)

    def gate_ctrl_for_complex(self, func_conf, req_params):
        logger.debug(func_conf.values)
        k, v = func_conf.values.items()[0]
        ctrl = self.get_ctrl_by_name(k)
        if ctrl is None:
            return False
        is_open = ctrl.cal(func_conf.values, req_params=req_params)

        logger.debug("gate_ctrl_for_complex:k=%s,result=%s", k, is_open)
        return is_open

    def gate_ctrl(self, func_conf, req_params):
        ctrl_types = func_conf.ctrl_type_list
        ctrl_method = func_conf.ctrl_method

        is_open = False

        if len(ctrl_types) == 0:
            return is_open

        if ctrl_method == ctrl_method__and:
            for ctrl_type in ctrl_types:
                inst = self.ctrl_types[ctrl_type.name]
                is_open = inst.cal(ctrl_type, req_params)
                if not is_open:
                    break
        elif ctrl_method == ctrl_method__or:
            for ctrl_type in ctrl_types:
                inst = self.ctrl_types[ctrl_type.name]
                is_open = inst.cal(ctrl_type, req_params)
                if is_open:
                    break
        logger.debug("gate_ctrl:len=%s,result=%s", len(ctrl_types), is_open)
        return is_open

    # test,     忽略gate
    # stage,    启用gate
    # product,  启用gate
    def gate_enable(self):
        # env_tag = self.get_env_tag()
        # if "dev"==env_tag:
        #     return False
        # elif "test"==env_tag:
        #     return False
        # elif "stage"==env_tag:
        #     return True
        # elif "product"==env_tag:
        #     return True
        # else:
        #     logger.debug("gate_enable: ENV_TAG no config.")
        #     return False
        return True

    def get_env_tag(self):
        env_tag = os.getenv('ENV_TAG')
        logger.debug("env_tag=%s", env_tag)
        return env_tag


class CtrlTypeBase:
    def __init__(self):
        pass

    def cal(self, func_conf, req_params, sys_params=None):
        return False


class CtrlTypeInternalUsers(CtrlTypeBase):
    def cal(self, func_conf, req_params, sys_params=None):
        user_id = req_params.user_id
        # print "CtrlType_InternalUsers",func_conf.values
        user_ids = func_conf.values.get('user_ids', [])
        is_open = False
        if user_ids:
            if user_id and int(user_id) in user_ids:
                is_open = True
        # print "CtrlType_InternalUsers", user_ids, is_open
        if not is_open:
            is_open = is_employee(user_id)

        # logger.debug("ct result=%s,%s,%s" % (func_conf.name, user_id, is_open))
        return is_open

class CtrlTypeTestUsers(CtrlTypeBase):
    def cal(self, func_conf, req_params, sys_params=None):

        if env_util.is_not_test():
            return False

        user_id = req_params.user_id
        user_ids = func_conf.values.get('user_ids', [])

        is_open = False
        if user_ids:
            if user_id and int(user_id) in user_ids:
                is_open = True

        if not is_open:
            is_open = is_employee_for_test(user_id)

        # logger.debug("ct result=%s,%s,%s" % (func_conf.name, user_id, is_open))
        return is_open

def is_employee_for_test(user_id):
    user_ids = FunctionConfigService().get_employee_ids_for_test()
    if user_id in user_ids:
        return True
    return False


def is_employee(user_id):
    user_ids = FunctionConfigService().get_employee_ids()
    if user_id in user_ids:
        return True
    return False


class CtrlTypeUserIdParity(CtrlTypeBase):
    def cal(self, func_conf, req_params, sys_params=None):
        user_id = req_params.user_id
        is_open = False
        if user_id and int(user_id) % 2 == 0:
            is_open = True

        # logger.debug("ct result=%s,%s,%s" % (func_conf.name, user_id, is_open))
        return is_open


class CtrlTypeUserIdMod(CtrlTypeBase):
    def cal(self, func_conf, req_params, sys_params=None):

        if type(req_params) == dict:
            user_id = req_params['user_id']
        else:
            user_id = req_params.user_id

        mod_val = int(func_conf.values['mod'])           # 10
        check_list = func_conf.values['check_list']         # [2,3,4]

        is_open = False
        if user_id:
            mod = int(user_id) % mod_val
            if mod in check_list:
                is_open = True
        # logger.debug("ct result=%s,%s,%s" % (func_conf.name, user_id, is_open))
        return is_open


class CtrlTypeNewUser(CtrlTypeBase):
    def cal(self, func_conf, req_params, sys_params=None):
        user_id = req_params.user_id
        max_id = int(func_conf.values['max_id'])           # 10
        is_open = False
        if user_id:
            if int(max_id) < user_id:
                is_open = True
        # logger.debug("ct result=%s,%s,%s" % (func_conf.name, user_id, is_open))
        return is_open


class CtrlTypeDateTimeBetween(CtrlTypeBase):
    def cal(self, func_conf, req_params, sys_params=None):
        start = int(func_conf.values['start'])
        end = int(func_conf.values['end'])
        now = time_util.get_timestamp()

        is_open = False
        if start <= now <= end:
            is_open = True
        # logger.debug("ct result=%s,%s,%s" % (func_conf.name, user_id, is_open))
        return is_open


class CtrlTypeEnvTest(CtrlTypeBase):
    def cal(self, func_conf, req_params, sys_params=None):
        return env_util.is_test()


class CtrlTypeEnvNotProd(CtrlTypeBase):
    def cal(self, func_conf, req_params, sys_params=None):
        return env_util.is_not_production()


class CtrlTypeEnvNotTest(CtrlTypeBase):
    def cal(self, func_conf, req_params, sys_params=None):
        return env_util.is_not_test()


class CtrlTypeAndroidOnly(CtrlTypeBase):
    def cal(self, func_conf, req_params, sys_params=None):
        return 'android' == req_params.os


class CtrlTypeIphoneOnly(CtrlTypeBase):
    def cal(self, func_conf, req_params, sys_params=None):
        return 'ios' == req_params.os


class CtrlTypeLocationRadius(CtrlTypeBase):

    def cal(self, func_conf, req_params, sys_params=None):

        value = func_conf.values
        # logger.debug("%s,%s", func_conf, value)
        func_lat = value['lat']
        func_lon = value['lon']
        func_radius = value['radius']

        user_lat = req_params.lat
        user_lon = req_params.lon
        user_id = req_params.user_id

        # logger.debug("CtrlType_LocationRadius geo=%s,%s,%s,%s",  user_lat, user_lon, func_lat, func_lon)
        dis = geo_util.cal_distance(user_lat, user_lon, func_lat, func_lon)
        is_open = False
        if dis == -1:
            is_open = False
        elif dis <= func_radius:
            is_open = True
        logger.debug("CtrlType_LocationRadius result=%s,%s,%s,%s", func_conf.name, user_id, dis, is_open)
        return is_open


class CtrlTypeDMA(CtrlTypeBase):

    cities_map = {}

    def cal(self, func_conf, req_params, sys_params=None):
        values = func_conf.values
        dma_code_list = values['dma_codes']
        req_city = CtrlTypeDMA.build_req_city(req_params)
        logger.debug("CtrlType_DMA:%s,%s", req_city, dma_code_list)
        if req_city in self.dma_cities(dma_code_list):
            return True
        else:
            return False

    @staticmethod
    def build_req_city(req_params):
        # 获得用户的 region_city
        user_id = req_params.user_id
        region = req_params.user_region
        city = req_params.user_city
        # base_info = UserDao().get_base_info(user_id)
        if region and city:
            return CtrlTypeDMA.build_city(region, city)
        return None

    def dma_cities(self, dma_code_list):
        cities = []
        for dma_code in dma_code_list:
            if dma_code not in self.cities_map:
                self.load_dma_cities(dma_code, dma_code_list)
            # 合并 citys ，可以优化
            cities.extend(self.cities_map[dma_code])
        return cities

    @staticmethod
    def build_city(region, city):
        return "%s_%s" % (region, city)

    @staticmethod
    def load_dma_cities(dma_code, dma_code_list):
        resp_content = basedata_client.dma_citys(dma_code)
        cities = [CtrlTypeDMA.build_city(tmp_city['region'], tmp_city['city']) for tmp_city in resp_content]
        logger.info('%s load_dma_cities %s', dma_code_list, cities)
        CtrlTypeDMA.cities_map[dma_code] = cities


class CtrlTypeAnd(CtrlTypeBase):
    def cal(self, func_conf, req_params, sys_params=None):
        if isinstance(func_conf, dict):
            ctrl_conf_array = func_conf[ctrl_type__and]
        else:
            ctrl_conf_array = func_conf
        logger.debug("CtrlType_And =%s", ctrl_conf_array)
        if ctrl_conf_array is None:
            return True

        result = False
        for ctrl_conf in ctrl_conf_array:
            item = ctrl_conf.items()[0]
            ctrl = FunctionGateService().get_ctrl_by_name(item[0])
            if ctrl is None:
                continue

            result = ctrl.cal(item[1], req_params=req_params)
            logger.debug("CtrlTypeAnd:name=%s,result=%s", item[0], result)
            if not result:
                break
        return result


class CtrlTypeOr(CtrlTypeBase):

    def cal(self, func_conf, req_params, sys_params=None):
        if isinstance(func_conf, dict):
            ctrl_conf_array = func_conf[ctrl_type__or]
        else:
            ctrl_conf_array = func_conf
        logger.debug("CtrlType_Or =%s", ctrl_conf_array)
        if ctrl_conf_array is None:
            return True

        result = False
        for ctrl_conf in ctrl_conf_array:
            item = ctrl_conf.items()[0]
            ctrl = FunctionGateService().get_ctrl_by_name(item[0])
            if ctrl is None:
                continue

            result = ctrl.cal(item[1], req_params=req_params)
            logger.debug("CtrlTypeOr:name=%s,result=%s", item[0], result)
            if result:
                break
        return result


class CtrlTypeAppVersion2(CtrlTypeBase):
    def cal(self, func_conf, req_params, sys_params=None):
        pass


class CtrlTypeAppVersion(CtrlTypeBase):
    reg = re.compile('([0-9\.]+)')

    def cal(self, func_conf, req_params, sys_params=None):
        if type(req_params) == dict:
            app_version = req_params.get('app_version', '')
        elif hasattr(req_params, 'app_version'):
            app_version = req_params.app_version
        else:
            app_version = req_params.app_ver

        result = self.reg.findall(app_version)
        if len(result) == 0:
            return False

        nums = result[0].split('.')
        if len(nums) < 3:
            nums.append('0')

        app_ver_num = 0
        for num in nums[:3]:
            app_ver_num = app_ver_num * 100 + int(num)
        
        min_app_num = func_conf.values.get('from', -1)
        max_app_num = func_conf.values.get('to', -1)
        logger.debug("app_version_check:%d|%d|%d|%s", app_ver_num, min_app_num, max_app_num, nums)
        if min_app_num != -1 and app_ver_num < min_app_num:
            return False
        if max_app_num != -1 and app_ver_num >= max_app_num:
            return False
        return True
