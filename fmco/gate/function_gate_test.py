# -*- coding: utf-8 -*-

from fmco.gate.function_gate import *
import logging

__author__ = 'lvyi'

logger = logging.getLogger("pinnacle")

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M', )

if __name__ == '__main__':

    # req_params = ReqParamsObject()
    # req_params.user_id=1080573
    #
    # gate_res = FunctionGateService().is_gate_open(gate_func__home_service_add_review_decay, req_params=req_params)
    # print "--->test1", gate_res
    # if gate_res:
    #     print True

    # req_params = ReqParamsObject()
    # req_params.lat = 32
    # req_params.lon = -96
    # req_params.user_id = 1080573
    # print req_params
    #
    # gate_res = FunctionGateService().is_gate_open(gate_func__search_cat_radius_ctrl, req_params=req_params)
    # print "--->test2", gate_res
    # if gate_res:
    #     print True

    logger.debug("----------------")

    conf = SmartConfigService().get_conf("haha")
    logger.debug("conf=%s" % conf)

    # print SmartConfigService().get_conf("haha")

    req_pms = ReqParamsObject()
    req_pms.user_id = 63101
    req_pms.region = 'TX'
    req_pms.city = 'Allen'

    # req_pms.region = 'Beijing'
    # req_pms.city = 'Beijing'

    # req_pms.os = 'ios'
    req_pms.os = 'android'
    req_pms.lat = 32
    req_pms.lon = -96
    req_pms.app_version = "4.1(4100)"
    #
    # logger.debug("----------------")
    # gate_res = FunctionGateService().is_gate_open(gate_func__pay_demo_users, req_params=req_pms)
    # logger.debug("gate_res=%s" % gate_res)
    #
    # # gate_res = FunctionGateService().is_gate_open(gate_func__dwa_dallas, req_params=req_params)
    # # FunctionGateService().is_gate_open(gate_func__dwa_houston, req_params)
    #
    # logger.debug("----------------")
    # gate_res = FunctionGateService().is_gate_open(gate_func__dwa_dallas, req_params=req_pms)
    # logger.debug("gate_res=%s" % gate_res)

    # gate_res = FunctionGateService().is_gate_open(gate_func__news_preview_test, req_params=req_pms)
    # logger.debug("gate_res=%s" % gate_res)

    logger.debug("----------------")
    gate_res = FunctionGateService().is_gate_open(gate_func__new_home, req_params=req_pms)
    logger.debug("gate_res=%s" % gate_res)
    #
    # # logger.debug("----------------")
    # gate_res = FunctionGateService().is_gate_open(gate_func__all_test, req_params=req_pms)
    # logger.debug("gate_res=%s" % gate_res)
