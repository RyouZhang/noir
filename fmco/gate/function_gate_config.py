# -*- coding: utf-8 -*-

from fmco.gate.function_gate_const import *

__author__ = 'lvyi'


gate_func__search_cat_radius_ctrl = "search_cat_radius_ctrl"
gate_func__home_service_add_review_decay = "home_service_add_review_decay"
gate_func__pay_demo_users = "pay_demo_users"
gate_func__channel_by_dallas = "channel_by_dallas"
gate_func__top_seller_by_dallas = "top_seller_by_dallas"
gate_func__appointment_by_dallas = "appointment_by_dallas"
gate_func__dealer_by_dallas = "dealer_by_dallas"

gate_func__home_cache = "home_cache"
gate_func__new_chat = "new_chat"

gate_func__sign_verify = "sign_verify"

gate_func__home_ad = "home_ad"
gate_func__dealer_application = "dealer_application"
gate_func__show_user_preference = "show_user_preference"
gate_func__detail_rc = "detail_rc"

gate_func__home_ads_item_test = "gate_func__home_ads_item_test"

gate_func__ad_test_mode = "gate_func__ad_test_mode"

gate_func__shipping_tab = 'gate_func__shipping_tab'
gate_func__shipping_h5 = 'gate_func__shipping_h5'

gate_func__installment = 'gate_func__installment'
gate_func__credit_activity = 'gate_func__credit_activity'

# gate_func__produce_offset_40 = "produce_offset_40"
# gate_func__produce_offset_60 = "produce_offset_60"
# gate_func__produce_offset_80 = "produce_offset_80"
# gate_func__produce_offset_100 = "produce_offset_100"

# gate_func_cat_box_state_test = "cat_box_state_test"

# gate_func_cat_keyword_create_update_test = "cat_keyword_create_update_test"

# gate_func_suggest_items_client_limit = "suggest_items_client_limit"

# gate_func__home_rec_cats = "home_rec_cats"

# gate_func__key_cat = "key_cat"

# gate_func__keyword_suggest = "keyword_suggest"
# gate_func__keyword_popular = "keyword_popular"

gate_func__featured_item = "featured_item"

gate_func__keyword_ad = "gate_func__keyword_ad"

gate_func__command = "gate_func__command"

gate_func__dwa_dallas = "gate_func__dwa_dallas"

gate_func__dwa_houston = "gate_func__dwa_houston"


gate_func__boost_mode = "gate_func__boost_mode"

# 担保交易控制门
gate_func__diamond = "gate_func__diamond"

gate_func__print_prod_log = "gate_func__print_prod_log"

gate_func__all_test = "all_test"


gate_func__new_home = "gate_func__new_home"
gate_func__new_home_test = "gate_func__new_home_test"

gate_func__suggest_1728000 = "gate_func__suggest_1728000"

gate_func__test_env = "gate_func__test_env"


default_configs_json = [
                            {"name": gate_func__search_cat_radius_ctrl,
                             "open_all": True,       # 2015-12-09 全面开放
                             "ctrls": [{"name": ctrl_type__internal_users, "values": {"user_ids": [1080573]}},
                                       # {"name":ctrl_type__location_radius,
                                       # "values":{"lat":32.837308,"lon":-96.776397,"radius":80000}},
                                       ]},

                            {"name": gate_func__pay_demo_users,
                             "ctrl_method": ctrl_method__or,
                             "ctrls": [{"name": ctrl_type__env_test}]},

                            {"name": gate_func__home_service_add_review_decay,
                             "ctrls": [{"name": ctrl_type__internal_users,
                                       "values": {"user_ids": [1080573]}}]},    # 1080573 why,63101 lvyi

                            {"name": gate_func__channel_by_dallas,
                             "ctrls": [{"name": ctrl_type__location_radius,
                                       "values": {"lat": 32.773023, "lon": -97.060980, "radius": 80000}}]},

                            {"name": gate_func__top_seller_by_dallas,
                             "ctrls": [{"name": ctrl_type__location_radius,
                                       "values": {"lat": 32.773023, "lon": -97.060980, "radius": 80000}}]},

                            {"name": gate_func__appointment_by_dallas,
                             "ctrls": [{"name": ctrl_type__location_radius,
                                       "values": {"lat": 32.773023, "lon": -97.060980, "radius": 80000}}]},

                            {"name": gate_func__dealer_by_dallas,
                             "ctrls": [{"name": ctrl_type__location_radius,
                                       "values": {"lat": 32.773023, "lon": -97.060980, "radius": 80000}}]},

                             {
                                 "name": gate_func__ad_test_mode,
                                 "ctrls": {
                                     "or": [
                                         {ctrl_type__env_not_prod:{}},
                                         {ctrl_type__internal_users:{}}
                                     ]
                                 }
                             },
                             {
                                 "name": gate_func__shipping_tab,
                                 "ctrls": {
                                     "and": [
                                         {ctrl_type__app_version: {"from": 40200}},
                                     ]
                                 }
                             },
                             {
                                 "name": gate_func__shipping_h5,
                                 "ctrls": {
                                     "and": [
                                         {ctrl_type__android_only: {}},
                                     ]
                                 }
                             },
                            {"name": gate_func__new_chat,
                             "ctrl_method": ctrl_method__or,
                             "ctrls": [{"name": ctrl_type__internal_users},
                                       {"name": ctrl_type__env_test},
                                       {"name": ctrl_type__user_id_mod,
                                        "values": {"mod": 10, "check_list": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]}}]},

                            {"name": gate_func__home_ad,
                             "ctrl_method": ctrl_method__or,
                             "ctrls": [{"name": ctrl_type__internal_users}, {"name": ctrl_type__env_test},
                                       {"name": ctrl_type__location_radius,
                                       "values": {"lat": 32.837308, "lon": -96.776397, "radius": 80000}}]},

                            {"name": gate_func__dealer_application,
                             # "open_all":True,
                             # "ctrl_method": ctrl_method__or,
                             "ctrls": [
                                      {"name": ctrl_type__location_radius,
                                       "values": {"lat": 32.773023, "lon": -97.060980, "radius": 80000}}]},

                            {"name": gate_func__detail_rc,
                             "ctrls": [{"name": ctrl_type__location_radius,  # 休斯顿 houston
                                       "values": {"lat": 29.8174782, "lon": -95.6814953, "radius": 80000}},
                                       {"name": ctrl_type__user_id_mod,
                                        "values": {"mod": 10, "check_list": [1, 5, 3, 7, 9]}}]},

                            # {"name": gate_func__produce_offset_40,
                            #  "ctrls": [{"name":ctrl_type__user_id_mod,"values":{"mod":10,"check_list":[2,3]}},
                            #            {"name": ctrl_type__location_radius,
                            #            "values": {"lat": 32.773023, "lon": -97.060980, "radius": 160000}}]},
                            # {"name": gate_func__produce_offset_60,
                            #  "ctrls": [{"name":ctrl_type__user_id_mod,"values":{"mod":10,"check_list":[4,5]}},
                            #            {"name": ctrl_type__location_radius,
                            #            "values": {"lat": 32.773023, "lon": -97.060980, "radius": 160000}}]},
                            # {"name": gate_func__produce_offset_80,
                            #  "ctrls": [{"name":ctrl_type__user_id_mod,"values":{"mod":10,"check_list":[6,7]}},
                            #            {"name": ctrl_type__location_radius,
                            #            "values": {"lat": 32.773023, "lon": -97.060980, "radius": 160000}}]},
                            # {"name": gate_func__produce_offset_100,
                            #  "ctrls": [{"name":ctrl_type__user_id_mod,"values":{"mod":10,"check_list":[8,9]}},
                            #            {"name": ctrl_type__location_radius,
                            #            "values": {"lat": 32.773023, "lon": -97.060980, "radius": 160000}}]},

                            # {"name": gate_func_cat_box_state_test,
                            #  "ctrls": [{"name": ctrl_type__internal_users}]},

                            # {"name": gate_func_cat_keyword_create_update_test,
                            #  "ctrls": [{"name":ctrl_type__user_id_mod,"values":{"mod":10,"check_list":[1,5,3,7,9]}}]},

                            # {"name": gate_func_suggest_items_client_limit,
                            #  "ctrls": [{"name":ctrl_type__user_id_mod,"values":{"mod":10,"check_list":[1,5,3,7,9]}}]},

                            # {"name": gate_func__key_cat,
                            #  "ctrls": [{"name":ctrl_type__user_id_mod,"values":{"mod":10,"check_list":[0,2,4,6,8]}}]},

                            # {"name":gate_func__home_rec_cats,
                            # "ctrl_method":ctrl_method__or,
                            # "ctrls":[{"name":ctrl_type__internal_users,"values":{"user_ids":self.get_employee_ids()}},
                            #           {"name":ctrl_type__user_id_mod,"values":{"mod":10,"check_list":[1,2]}}
                            #           ]},

                            # {"name": gate_func__keyword_suggest,
                            #  "ctrl_method":ctrl_method__or,
                            #  "ctrls": [{"name":ctrl_type__user_id_mod,"values":{"mod":10,"check_list":[3,4]}},
                            #            {"name": ctrl_type__internal_users,
                            # "values":{"user_ids":self.get_employee_ids()}}
                            #            ]},

                            {"name": gate_func__featured_item,
                             "ctrls": [{"name": ctrl_type__user_id_mod, "values": {"mod": 10, "check_list": [3, 4]}}]},

                            # {"name": gate_func__keyword_popular,
                            #  "ctrl_method":ctrl_method__or,
                            #  "ctrls": [{"name":ctrl_type__user_id_mod,"values":{"mod":10,"check_list":[5,6]}},
                            #            {"name": ctrl_type__internal_users}
                            #            ]},

                            {"name": gate_func__show_user_preference,
                             "ctrls": [{"name": ctrl_type__user_id_mod, "values": {"mod": 10, "check_list": [1, 2]}}]},

                            {"name": gate_func__home_ads_item_test,
                             "ctrls": [
                                 {"name": ctrl_type__date_between, "values": {"start": 1479254400+3600*8,
                                                                              "end": 1479254400+86400*7}}
                                 ]},
                            {"name": gate_func__credit_activity,
                             "ctrls": {
                                 "and": [
                                     {ctrl_type__date_between: {"start": 1479686400, "end": 1481846400+3600*8}},
                                     {ctrl_type__app_version: {"from": 40300}},
                                     # {"or": [
                                     #     {ctrl_type__internal_users: {}},
                                     #     {ctrl_type__env_test: {}},
                                     #     # {ctrl_type__user_id_mod: {"mod": 10, "check_list": [0, 2, 4, 6, 8]}},
                                     #     {ctrl_type__dma: {"dma_codes": [803, 999]}}
                                     #   ]}
                                  ]}
                             },

                            {"name": gate_func__keyword_ad,
                             "ctrl_method": ctrl_method__or,
                             "ctrls": [
                                    {"name": ctrl_type__env_test},
                                    {"name": ctrl_type__internal_users}
                                ]
                             },

                            {"name": gate_func__command,
                             "ctrl_method": ctrl_method__or,
                             "ctrls": [
                                    {"name": ctrl_type__internal_users}
                                ]
                             },

                            {"name": gate_func__print_prod_log,
                             "ctrls": [{"name": ctrl_type__env_not_prod}]
                             },

                            {"name": gate_func__dwa_dallas,
                             "ctrls": [
                                 {"name": ctrl_type__dma, "values": {"dma_codes": [623]}}
                             ]
                             },

                            {"name": gate_func__dwa_houston,
                             "ctrl_method": ctrl_method__or,
                             "ctrls": [
                                    {"name": ctrl_type__dma, "values": {"dma_codes": [618]}}
                                ]
                             },

                            {"name": gate_func__boost_mode,
                             "ctrl_method": ctrl_method__or,
                             "ctrls": [
                                    {"name": ctrl_type__internal_users},
                                    {"name": ctrl_type__user_id_mod, "values": {"mod": 10, "check_list": [1, 6]}}
                                ]
                             },

                            {"name": gate_func__suggest_1728000,
                             "ctrl_method": ctrl_method__or,
                             "ctrls": [
                                    {"name": ctrl_type__internal_users},
                                    {"name": ctrl_type__user_id_mod, "values": {"mod": 10, "check_list": [0, 1, 2, 3, 4]}}
                                ]
                             },

                            {"name": gate_func__diamond,
                             "ctrls": [
                                 {"name": ctrl_type__dma, "values": {"dma_codes": [819, 505]}}
                             ]
                             },
                            {"name": gate_func__installment,
                             "ctrls": {
                                 "or":
                                     [
                                         {ctrl_type__env_test: {}},
                                         {"and": [
                                             {ctrl_type__android_only: {}},
                                             {ctrl_type__user_id_mod: {"mod": 10, "check_list": [1, 3]}}
                                         ]}
                                     ]
                             }},
                            {"name": gate_func__all_test,
                             "ctrls": {
                                 "and":
                                     [
                                         {ctrl_type__android_only: {}},
                                         {ctrl_type__new_user: {"max_id": 1000}},
                                         {ctrl_type__date_between: {"start": 1475654400 + 8 * 3600,
                                                                    "end": 1475654400 + 8 * 3600 + 86400 * 7}},
                                         {ctrl_type__user_id_parity: {}},
                                         {ctrl_type__app_version: {"to": 50000}},
                                         {"or": [
                                             {ctrl_type__location_radius: {"lat": 29.75, "lon": -95.366667,
                                                                           "radius": 80000}},
                                             {ctrl_type__user_id_mod: {"mod": 10, "check_list": [2, 7]}},
                                             {ctrl_type__internal_users: {}}
                                         ]}
                                     ]
                             }},
                             {"name": gate_func__new_home,
                              "ctrls": {
                                  "or": [
                                        {ctrl_type__internal_users: {}},
                                        {ctrl_type__env_test: {}},                                      
                                        {"and": [
                                            {ctrl_type__android_only: {}},
                                            {ctrl_type__app_version: {"from": 40300}},
                                        ]},
                                        {"and": [
                                            {ctrl_type__iphone_only: {}},
                                            {ctrl_type__app_version: {"from": 40400}},                                       
                                        ]},
                                  ]}
                              },
                             {"name": gate_func__new_home_test,
                              "ctrls": {
                                  "or": [
                                      {ctrl_type__env_test: {}},
                                      ]}
                              },
                              {"name": gate_func__test_env,
                              "ctrls": {
                                  "and": [
                                      {ctrl_type__env_test: {}}
                                  ]
                              }
                              },


                        ]
