# encoding:utf-8
from common.douyu_request import dyreq
from common.logger import logger
from common.config import conf
from common.get_secrets import get_secrets
from lxml import etree
import re
import math
import requests



def get_badge():
    """
    :return: 获取具有粉丝牌的房间号、当前经验、升级所需经验、升级还需要的经验
    """
    badges_url = "/member/cp/getFansBadgeList"
    badges = dyreq.request("get", badges_url)
    html = etree.HTML(badges.text, etree.HTMLParser())
    num = len(html.xpath('//*[@id="wrap"]/div/div[2]/div[2]/div[3]/table/tbody/tr'))
    re_now = r'(?<= )\d.*\d(?=\/\d)'
    re_up = r'(?<=\/)\d.*\d'
    badge_dict = {}
    exp_list = []
    for path in range(num):
        path += 1
        room_id = html.xpath('//*[@id="wrap"]/div/div[2]/div[2]/div[3]/table/tbody/tr[%s]/@data-fans-room' % path)[
            0]
        anchor = html.xpath('//*[@id="wrap"]/div/div[2]/div[2]/div[3]/table/tbody/tr[%s]/td[2]/a/text()' % path)[0]
        exp = html.xpath('//*[@id="wrap"]/div/div[2]/div[2]/div[3]/table/tbody/tr[%s]/td[3]/text()' % path)[0]
        exp_now = float(re.findall(re_now, exp)[0])
        up_grade = float(re.findall(re_up, exp)[0])
        exp_need = round((up_grade - exp_now), 1)
        exp_list.append(exp_need)
        badge_dict[room_id] = anchor
    return badge_dict, exp_list


def get_room_list():
    """
    :return:通过数组方式返回房间号
    """
    room_list = []
    for room in get_badge()[0]:
        room_list.append(room)
    return room_list


def get_need_exp():
    """
    :return:通过数组方式返回升级所需经验
    """
    nums = conf.get_conf_list('selfMode', 'giftCount')
    for i in range(len(get_badge()[1])):
        logger.info("房间号%s升级还需%s点经验" % (get_room_list()[i], get_badge()[1][i]))
        logger.info(nums[i])
        logger.info(get_badge()[1][i])
        days = int(get_badge()[1][i]) / int(nums[i])
        days_require = int(math.ceil(int(math.ceil(get_badge()[1][i])) / int(nums[i])))
        logger.info(days_require)

'''
def get_need_exp():
    """
    :return:通过数组方式返回升级所需经验
    """
    nums = conf.get_conf_list('selfMode', 'giftCount')
    for i in range(len(get_badge()[1])):
        days_require = int(math.ceil(get_badge()[1][i] / nums[i]))
        logger.info("当前nums长度为%s"%(len(nums)))
        logger.info("房间号%s升级还需%s点经验" % (get_room_list()[i], get_badge()[1][i]))
        logger.info("房间号%s升级还需%s点经验,还需%s天" % (get_room_list()[i], get_badge()[1][i], days_require))
        notify_url = get_secrets('BARKURL') + "/房间号%s/升级还需%s点经验" % (get_room_list()[i], get_badge()[1][i])
        requests.get(notify_url)
'''


if __name__ == '__main__':
    a = get_room_list()
    get_need_exp()