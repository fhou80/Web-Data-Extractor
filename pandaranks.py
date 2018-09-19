# This Python file uses the following encoding: utf-8

import time
from datetime import datetime
import sys
from downloader import Downloader
import json


class PandaRanks():
    """download the panda.tv ranks"""
    def __init__(self):
        self.downer = Downloader()
        reload(sys)
        sys.setdefaultencoding('utf8')

    def get_oline_list(self):
        time_str = str(time.time())
        dt = datetime.now()
        dt.strftime("%s")
        dot_pos = time_str.find(".")
        str_stamp = time_str[:dot_pos]
        time_str = str(dt)
        dot_pos = time_str.find(".") + 1
        str_stamp += time_str[dot_pos:dot_pos + 3]

        rank_anchor_online_json = json.loads(
            self.downer("https://www.panda.tv/cmstatic/weekly_rank_anchor_gift.json?token=&_="+str_stamp))
        # # 魅力主播榜
        rank_anchor_online_list = rank_anchor_online_json['cur_rank_list']
        online_list = []
        for rank_anchor_online_entry in rank_anchor_online_list:
            room_status = rank_anchor_online_entry['roominfo']['status']
            if room_status:
                online_list.append(rank_anchor_online_entry['roominfo']['id'])
        return online_list


    def down_save(self, file_path):
        time_str = str(time.time())
        dt = datetime.now()
        dt.strftime("%s")
        dot_pos = time_str.find(".")
        str_stamp = time_str[:dot_pos]
        time_str = str(dt)
        dot_pos = time_str.find(".") + 1
        str_stamp += time_str[dot_pos:dot_pos + 3]
        token_int = int(str_stamp)

        rank_anchor_gift_json = json.loads(
            self.downer("https://www.panda.tv/cmstatic/weekly_rank_anchor_gift.json?token=&_="+str(token_int)))
        # 魅力主播榜
        rank_anchor_gift_list = rank_anchor_gift_json['cur_rank_list']
        rank_i = 0
        rank_file = open(file_path + '魅力主播榜.csv', 'a')
        rank_file.write("new entry\n")
        for rank_anchor_gift_entry in rank_anchor_gift_list:
            rank_i += 1
            anchor_id4_rank = rank_anchor_gift_entry['userinfo']['rid']
            room_id4_rank = rank_anchor_gift_entry['roominfo']['id']
            anchor_nickname4_rank = rank_anchor_gift_entry['userinfo']['nickName']
            #print(str(rank_i) + ", " + str(anchor_id4_rank) + "," + room_id4_rank + "," + anchor_nickname4_rank+"\n")
            rank_file.write(str(rank_i) + ", " + str(anchor_id4_rank) + "," + room_id4_rank + "," + anchor_nickname4_rank+"\n")
        rank_file.close()

        rank_file = open(file_path + '受欢迎主播.csv', 'a')
        rank_file.write("new entry\n")
        token_int += 1
        rank_anchor_gift_user_json = json.loads(
            self.downer("https://www.panda.tv/cmstatic/weekly_rank_anchor_gift_user.json?token=&_="+str(token_int)))
        # 受欢迎主播
        rank_anchor_gift_user_list = rank_anchor_gift_user_json['cur_rank_list']
        rank_i = 0
        for rank_anchor_gift_user_entry in rank_anchor_gift_user_list:
            rank_i += 1
            anchor_id4_rank = rank_anchor_gift_user_entry['userinfo']['rid']
            room_id4_rank = rank_anchor_gift_user_entry['roominfo']['id']
            anchor_nickname4_rank = rank_anchor_gift_user_entry['userinfo']['nickName']
            user_count = rank_anchor_gift_user_entry['user_count']
            #print(str(rank_i) + "," + str(anchor_id4_rank) + "," + str(room_id4_rank) + "," + anchor_nickname4_rank + "," + str(user_count)+"\n")
            rank_file.write(str(rank_i) + "," + str(anchor_id4_rank) + "," + str(room_id4_rank) + "," + anchor_nickname4_rank + "," + str(user_count)+"\n")
        rank_file.close()

        rank_file = open(file_path + '弹幕条数榜.csv', 'a')
        rank_file.write("new entry\n")
        token_int += 1
        rank_anchor_barrage_json = json.loads(
            self.downer("https://www.panda.tv/cmstatic/weekly_rank_anchor_barrage.json?token=&_="+str(token_int)))
        # 弹幕条数榜
        rank_anchor_barrage_list = rank_anchor_barrage_json['cur_rank_list']
        rank_i = 0
        for rank_anchor_barrage_entry in rank_anchor_barrage_list:
            rank_i += 1
            anchor_barrage_count = rank_anchor_barrage_entry['barrage_count']
            anchor_id4_rank = rank_anchor_barrage_entry['userinfo']['rid']
            room_id4_rank = rank_anchor_barrage_entry['roominfo']['id']
            anchor_nickname4_rank = rank_anchor_barrage_entry['userinfo']['nickName']
            #print(str(rank_i) + "," + str(anchor_id4_rank) + "," + room_id4_rank + "," + anchor_nickname4_rank + "," + anchor_barrage_count + "\n")
            rank_file.write(str(rank_i) + "," + str(anchor_id4_rank) + "," + room_id4_rank + "," + anchor_nickname4_rank + "," + anchor_barrage_count + "\n")
        rank_file.close()

        rank_file = open(file_path + '土豪实力榜.csv', 'a')
        rank_file.write("new entry\n")
        token_int += 1
        rank_user_gift_json = json.loads(
            self.downer("https://www.panda.tv/cmstatic/weekly_rank_user_gift.json?token=&_="+str(token_int)))
        # 土豪实力榜
        rank_user_gift_list = rank_user_gift_json['cur_rank_list']
        rank_i = 0
        for rank_user_gift_entry in rank_user_gift_list:
            rank_i += 1
            user_id4_rank = rank_user_gift_entry['userinfo']['rid']
            user_nickname4_rank = rank_user_gift_entry['userinfo']['nickName']
            user_gift_sum = rank_user_gift_entry['gift_sum']
            #print(str(rank_i) + "," + str(user_id4_rank) + "," + user_nickname4_rank + "," + user_gift_sum + "\n")
            rank_file.write(str(rank_i) + "," + str(user_id4_rank) + "," + user_nickname4_rank + "," + user_gift_sum + "\n")
        rank_file.close()

        rank_file = open(file_path + '任性新壕友.csv', 'a')
        rank_file.write("new entry\n")
        token_int += 1
        rank_new_user_gift_json = json.loads(
            self.downer("https://www.panda.tv/cmstatic/weekly_rank_new_user_gift.json?token=&_="+str(token_int)))
        # 任性新壕友
        rank_new_user_gift_list = rank_new_user_gift_json['cur_rank_list']
        rank_i = 0
        for rank_new_user_gift_entry in rank_new_user_gift_list:
            rank_i += 1
            user_id4_rank = rank_new_user_gift_entry['userinfo']['rid']
            user_nickname4_rank = rank_new_user_gift_entry['userinfo']['nickName']
            user_gift_sum = rank_new_user_gift_entry['gift_sum']
            #print(str(rank_i) + "," + str(user_id4_rank) + "," + user_nickname4_rank + "," + user_gift_sum+"\n")
            rank_file.write(str(rank_i) + "," + str(user_id4_rank) + "," + user_nickname4_rank + "," + user_gift_sum+"\n")
        rank_file.close()

        rank_file = open(file_path + '主播身高榜.csv', 'a')
        rank_file.write("new entry\n")
        token_int += 1
        rank_anchor_bamboo_json = json.loads(
            self.downer("https://www.panda.tv/cmstatic/weekly_rank_anchor_bamboo.json?token=&_="+str(token_int)))
        # 主播身高榜
        rank_anchor_bamboo_list = rank_anchor_bamboo_json['cur_rank_list']
        rank_i = 0
        for rank_anchor_bamboo_entry in rank_anchor_bamboo_list:
            rank_i += 1
            anchor_id4_rank = rank_anchor_bamboo_entry['userinfo']['rid']
            anchor_nickname4_rank = rank_anchor_bamboo_entry['userinfo']['nickName']
            anchor_bamboo_sum = rank_anchor_bamboo_entry['bamboo_sum']
            #print(str(rank_i) + "," + str(anchor_id4_rank) + "," + anchor_nickname4_rank + "," + anchor_bamboo_sum+"\n")
            rank_file.write(str(rank_i) + "," + str(anchor_id4_rank) + "," + anchor_nickname4_rank + "," + anchor_bamboo_sum+"\n")
        rank_file.close()

        rank_file = open(file_path + '主播敬业榜.csv', 'a')
        rank_file.write("new entry\n")
        token_int += 1
        rank_anchor_online_json = json.loads(
            self.downer("https://www.panda.tv/cmstatic/weekly_rank_anchor_play.json?token=&_="+str(token_int)))
        # 主播敬业榜
        rank_anchor_online_list = rank_anchor_online_json['cur_rank_list']
        rank_i = 0
        for rank_anchor_online_entry in rank_anchor_online_list:
            rank_i += 1
            anchor_id4_rank = rank_anchor_online_entry['userinfo']['rid']
            anchor_nickname4_rank = rank_anchor_online_entry['userinfo']['nickName']
            anchor_online_sum = rank_anchor_online_entry['play_sum']
            #print(str(rank_i) + "," + str(anchor_id4_rank) + "," + anchor_nickname4_rank + "," + anchor_online_sum+"\n")
            rank_file.write(str(rank_i) + "," + str(anchor_id4_rank) + "," + anchor_nickname4_rank + "," + anchor_online_sum+"\n")
        rank_file.close()

        rank_file = open(file_path + '主播收视榜.csv', 'a')
        rank_file.write("new entry\n")
        token_int += 1
        rank_anchor_view_json = json.loads(
            self.downer("https://www.panda.tv/cmstatic/weekly_rank_anchor_viewtime.json?token=&_="+str(token_int)))
        # 主播收视榜
        rank_anchor_view_list = rank_anchor_view_json['cur_rank_list']
        rank_i = 0
        for rank_anchor_view_entry in rank_anchor_view_list:
            rank_i += 1
            anchor_id4_rank = rank_anchor_view_entry['userinfo']['rid']
            anchor_nickname4_rank = rank_anchor_view_entry['userinfo']['nickName']
            anchor_viewtime_sum = rank_anchor_view_entry['viewtime_sum']
            #print(str(rank_i) + "," + str(anchor_id4_rank) + "," + anchor_nickname4_rank + "," + anchor_viewtime_sum+"\n")
            rank_file.write(str(rank_i) + "," + str(anchor_id4_rank) + "," + anchor_nickname4_rank + "," + anchor_viewtime_sum+"\n")
        rank_file.close()

        rank_file = open(file_path + '新人人气王.csv', 'a')
        rank_file.write("new entry\n")
        token_int += 1
        rank_newanchor_pop_json = json.loads(
            self.downer("https://www.panda.tv/cmstatic/weekly_rank_new_anchor_popular.json?token=&_="+str(token_int)))
        # 新人人气王
        rank_newanchor_pop_list = rank_newanchor_pop_json['cur_rank_list']
        rank_i = 0
        for rank_newanchor_pop_entry in rank_newanchor_pop_list:
            rank_i += 1
            anchor_id4_rank = rank_newanchor_pop_entry['userinfo']['rid']
            anchor_nickname4_rank = rank_newanchor_pop_entry['userinfo']['nickName']
            anchor_popular_max = rank_newanchor_pop_entry['popular_max']
            #print(str(rank_i) + "," + str(anchor_id4_rank) + "," + anchor_nickname4_rank + "," + anchor_popular_max+"\n")
            rank_file.write(str(rank_i) + "," + str(anchor_id4_rank) + "," + anchor_nickname4_rank + "," + anchor_popular_max+"\n")
        rank_file.close()

        rank_file = open(file_path + '车站日榜.csv', 'a')
        rank_file.write("new entry\n")
        token_int += 1
        anchor_station_day_json = json.loads(
            self.downer("https://www.panda.tv/cmstatic/weekly_rank_anchor_station_day.json?token=&_="+str(token_int)))
        # 车站日榜
        anchor_station_day_list = anchor_station_day_json['cur_rank_list']
        rank_i = 0
        for anchor_station_day_entry in anchor_station_day_list:
            rank_i += 1
            anchor_id4_rank = anchor_station_day_entry['userinfo']['rid']
            anchor_nickname4_rank = anchor_station_day_entry['userinfo']['nickName']
            anchor_ticket_num = anchor_station_day_entry['gift_sum']
            #print(str(rank_i) + "," + str(anchor_id4_rank) + "," + anchor_nickname4_rank + "," + str(anchor_ticket_num)+"\n")
            rank_file.write(str(rank_i) + "," + str(anchor_id4_rank) + "," + anchor_nickname4_rank + "," + str(
                anchor_ticket_num)+"\n")
        rank_file.close()

        rank_file = open(file_path + '车站周榜.csv', 'a')
        rank_file.write("new entry\n")
        token_int += 1
        anchor_station_week_json = json.loads(
            self.downer("https://www.panda.tv/cmstatic/weekly_rank_anchor_station_week.json?token=&_="+str(token_int)))
        # 车站周榜
        anchor_station_week_list = anchor_station_week_json['cur_rank_list']
        rank_i = 0
        for anchor_station_week_entry in anchor_station_week_list:
            rank_i += 1
            anchor_id4_rank = anchor_station_week_entry['userinfo']['rid']
            anchor_nickname4_rank = anchor_station_week_entry['userinfo']['nickName']
            anchor_ticket_num = anchor_station_week_entry['gift_sum']
            #print(str(rank_i) + "," + str(anchor_id4_rank) + "," + anchor_nickname4_rank + "," + str(anchor_ticket_num)+"\n")
            rank_file.write(str(rank_i) + "," + str(anchor_id4_rank) + "," + anchor_nickname4_rank + "," + str(anchor_ticket_num)+"\n")
        rank_file.close()

        rank_file = open(file_path + '车站月榜.csv', 'a')
        rank_file.write("new entry\n")
        token_int += 1
        anchor_station_month_json = json.loads(
            self.downer("https://www.panda.tv/cmstatic/weekly_rank_anchor_station_month.json?token=&_="+str(token_int)))
        # 车站月榜
        anchor_station_month_list = anchor_station_month_json['cur_rank_list']
        rank_i = 0
        for anchor_station_month_entry in anchor_station_month_list:
            rank_i += 1
            anchor_id4_rank = anchor_station_month_entry['userinfo']['rid']
            anchor_nickname4_rank = anchor_station_month_entry['userinfo']['nickName']
            anchor_ticket_num = anchor_station_month_entry['gift_sum']
            #print(str(rank_i) + "," + str(anchor_id4_rank) + "," + anchor_nickname4_rank + "," + str(anchor_ticket_num)+"\n")
            rank_file.write(str(rank_i) + "," + str(anchor_id4_rank) + "," + anchor_nickname4_rank + "," + str(anchor_ticket_num)+"\n")
        rank_file.close()

        rank_file = open(file_path + 'PK胜利榜.csv', 'a')
        rank_file.write("new entry\n")
        token_int += 1
        rank_anchor_pkwin_json = json.loads(
            self.downer("https://www.panda.tv/cmstatic/weekly_rank_anchor_pkwin.json?token=&_="+str(token_int)))
        # PK胜利榜
        rank_anchor_pkwin_list = rank_anchor_pkwin_json['cur_rank_list']
        rank_i = 0
        for rank_anchor_pkwin_entry in rank_anchor_pkwin_list:
            rank_i += 1
            anchor_id4_rank = rank_anchor_pkwin_entry['userinfo']['rid']
            anchor_nickname4_rank = rank_anchor_pkwin_entry['userinfo']['nickName']
            anchor_win_num = rank_anchor_pkwin_entry['win']
            #print(str(rank_i) + "," + str(anchor_id4_rank) + "," + anchor_nickname4_rank + "," + str(anchor_win_num)+"\n")
            rank_file.write(str(rank_i) + "," + str(anchor_id4_rank) + "," + anchor_nickname4_rank + "," + str(anchor_win_num)+"\n")
        rank_file.close()

        rank_file = open(file_path + 'PK连胜榜.csv', 'a')
        rank_file.write("new entry\n")
        token_int += 1
        rank_anchor_pkcwin_json = json.loads(
            self.downer("https://www.panda.tv/cmstatic/weekly_rank_anchor_pkcwin.json?token=&_="+str(token_int)))
        # PK连胜榜
        rank_anchor_pkcwin_list = rank_anchor_pkcwin_json['cur_rank_list']
        rank_i = 0
        for rank_anchor_pkcwin_entry in rank_anchor_pkcwin_list:
            rank_i += 1
            anchor_id4_rank = rank_anchor_pkcwin_entry['userinfo']['rid']
            anchor_nickname4_rank = rank_anchor_pkcwin_entry['userinfo']['nickName']
            anchor_cwin_num = rank_anchor_pkcwin_entry['win']
            #print(str(rank_i) + "," + str(anchor_id4_rank) + "," + anchor_nickname4_rank + "," + str(anchor_cwin_num)+"\n")
            rank_file.write(str(rank_i) + "," + str(anchor_id4_rank) + "," + anchor_nickname4_rank + "," + str(anchor_cwin_num)+"\n")
        rank_file.close()



