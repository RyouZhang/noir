# -*- coding: utf-8 -*-
import os
import util

__author__ = 'lvyi'

ENV_PRODUCTION = 'prod'
ENV_DEV = 'dev'
ENV_STAGE = 'stage'
ENV_TEST = 'test'
ENV_NO = 'no'


def get_env_tag():
    _env = os.getenv('ENV_TAG')
    util.logger.info("get_env_tag=%s" % _env)
    return _env


env_tag = ENV_NO


def is_test():
    global env_tag
    if env_tag == ENV_NO:
        env_tag = get_env_tag()
    if env_tag in [ENV_DEV, ENV_TEST]:
        # logger.debug("is_test=True")
        return True
    else:
        return False


def is_stage():
    global env_tag
    if env_tag == ENV_NO:
        env_tag = get_env_tag()
    if ENV_STAGE == env_tag:
        return True
    else:
        return False


def is_not_production():
    global env_tag
    if env_tag == ENV_NO:
        env_tag = get_env_tag()
    # 默认情况prod环境  没有配置ENV_TAG标记
    if env_tag in [ENV_PRODUCTION, None, ENV_NO]:
        return False
    else:
        return True


def is_not_test():
    global env_tag
    if env_tag == ENV_NO:
        env_tag = get_env_tag()
    # 默认情况prod环境  没有配置ENV_TAG标记
    if env_tag in [ENV_TEST, ENV_DEV]:
        return False
    else:
        return True
