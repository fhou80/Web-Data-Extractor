# This Python file uses the following encoding: utf-8

import sys
import lxml.html as myhtml
from downloader import Downloader
from pandaranks import PandaRanks
import json
from selenium import webdriver
import time
from datetime import datetime
from pyvirtualdisplay import Display

reload(sys)
sys.setdefaultencoding('utf8')
TABS_NUM_CONSTANT = 5
display = Display(visible=0, size=(1280, 1024))
display.start()
option = webdriver.ChromeOptions()
option.add_argument("--disable-component-update")
option.add_argument("--allow-running-insecure-content")
option.add_argument("--disable-web-security")
option.add_argument("--ppapi-flash-path=/home/ming/.config/google-chrome/PepperFlash/31.0.0.108/libpepflashplayer.so")
option.add_argument("--allow-outdated-plugins")
driver = webdriver.Chrome(executable_path="/home/ming/Sophia_yizhibo/chromedriver", chrome_options=option)
#driver = webdriver.Chrome(executable_path="/home/krude/Downloads/chromedriver")
#driver.get("https://www.panda.tv/1226973")
#driver.get("https://www.douyu.com/5076442")

#tested urls during the last 10 minutes
interest_url = []
#interested room ids
room_id = [88888, 20641, 575757, 10027, 80000, 520520, 236658, 102689, 596605, 20520, 337852, 504097, 1109535, 1627281, 365382, 1272245, 6666666, 1509115, 45115, 20487]
#whether the room finished live streamming
finished=[1]
#whether the page is of interest
interest_anchor = [0]
#the room id of the page, same as current_url, but is of int
current_id=[1]
#the url that was opened in each tab until now, the roomd id
current_url=[""]
#the num of previous messge list
previous = [0]

#try to open tabs
for j in range(TABS_NUM_CONSTANT):
    time.sleep(1)
    driver.execute_script("window.open('');")
    finished.append(1)
    interest_anchor.append(0)
    current_url.append("")
    current_id.append(1)
    previous.append(0)

#whether or not timeout when loading the page
timeout = 0

#a PandaRank object to download the panda.tv ranks
pandaranklist = PandaRanks()
#pandaranklist.down_save("/home/ming/Sophia_yizhibo/panda/")

#at the last tab, navigate and check the status
driver.switch_to.window(driver.window_handles[TABS_NUM_CONSTANT])
for room_entry in room_id:
    try:
        room_url = "https://www.panda.tv/"+str(room_entry)
        driver.get(room_url)
        time.sleep(5)
        page_tree = myhtml.fromstring(driver.page_source)
        anchor_status = ""
        anchor_info_detail = page_tree.xpath('//div[@class="room-head-info-title-wrapper"]')
        if len(anchor_info_detail) == 0:
            anchor_info_detail = page_tree.xpath('//div[starts-with(@class,"room-head-info-detail")]')
        if len(anchor_info_detail)>0:
            anchor_label_info = anchor_info_detail[0].findall("a")
            if len(anchor_label_info) > 0:
                anchor_label = anchor_label_info[0].text_content()
                anchor_status_info = anchor_label_info[0].xpath('@data-tips')
                if len(anchor_status_info) > 0:
                    anchor_status = anchor_status_info[0]
        #print(anchor_status)
        if anchor_status.startswith("直播中"):
            interest_url.append(str(room_entry))
    #ignore the timeout
    except:
        continue
print(interest_url)
#the previous time string
rank_prev_time = datetime.now()
rank_curr_time = datetime.now()
urls_prev_time = datetime.now()
urls_curr_time = datetime.now()

#open page and get info in a never ending while loop
while 1:
    #get the ranking lists after a time interval
    rank_curr_time = datetime.now()
    secDiff = (rank_curr_time - rank_prev_time).days
    if secDiff > 1:
        rank_curr_time = datetime.now()
        #get the ranking
        pandaranklist.down_save("/home/ming/Sophia_yizhibo/panda/")

    # clear the tested urls after a time interval
    urls_curr_time = datetime.now()
    secDiff = (urls_curr_time - urls_prev_time).seconds
    if secDiff > 600:
        urls_prev_time = datetime.now()
        #if all the tabs are of interest anchors, don't update
        all_tabs_interest = 1
        for j in range(TABS_NUM_CONSTANT):
            if not interest_anchor[j]:
                all_tabs_interest = 0
        if not all_tabs_interest:
            # clear the interest urls
            while len(interest_url) > 0:
                interest_url.pop()
            # # at the last tab, navigate and check the status
            driver.switch_to.window(driver.window_handles[TABS_NUM_CONSTANT])
            for room_entry in room_id:
                if room_entry in current_id:
                    continue
                try:
                    room_url = "https://www.panda.tv/" + str(room_entry)
                    driver.get(room_url)
                    time.sleep(5)
                    page_tree = myhtml.fromstring(driver.page_source)
                    anchor_status = ""
                    anchor_info_detail = page_tree.xpath('//div[@class="room-head-info-title-wrapper"]')
                    if len(anchor_info_detail) == 0:
                        anchor_info_detail = page_tree.xpath('//div[starts-with(@class,"room-head-info-detail")]')
                    if len(anchor_info_detail) > 0:
                        anchor_label_info = anchor_info_detail.findall("a")
                        if len(anchor_label_info) > 0:
                            anchor_label = anchor_label_info[0].text_content()
                            anchor_status_info = anchor_label_info[0].xpath('@data-tips')
                            if len(anchor_status_info) > 0:
                                anchor_status = anchor_status_info[0]
                    # print(anchor_status)
                    if anchor_status.startswith("直播中"):
                        live_url = str(room_entry)
                        interest_url.append(live_url)
                except:
                    continue
    #finished updating status

    for i in range(TABS_NUM_CONSTANT):
        driver.switch_to.window(driver.window_handles[i])
        # if not of interest anchor, and there is online interest anchor
        if interest_anchor[i] == 0:
            if len(interest_url) > 0:
                # pop up the url, navigate to that url, get info
                # set the value of interest_anchor[i], interest_anchid[i], finished[i]
                try:
                    driver.get("https://www.panda.tv/" + interest_url[0])
                    current_url[i] = interest_url[0]
                    interest_url.pop(0)
                except:
                    timeout = 1
                    pass
                if timeout:
                    timeout = 0
                    continue
                interest_anchor[i] = 1
                previous[i] = 0
                current_id[i] = int(current_url[i])
                finished[i] = 0
                time.sleep(5)
                #get the room info
                tree = myhtml.fromstring(driver.page_source)
                room_title_info = tree.xpath('//h1[@class="room-head-info-title"]')
                if len(room_title_info)==0:
                    room_title_info = tree.xpath('//span[starts-with(@class,"room-head-info__title")]')
                room_title = ""
                if len(room_title_info)>0:
                    room_title = room_title_info[0].text_content()
                room_title = room_title.replace("\n", "")
                anchor_info_detail = tree.xpath('//div[starts-with(@class,"room-head-info-detail")]')[0]
                anchor_levl = anchor_info_detail.findall("i")[0].xpath('@data-level')[0]
                anchor_ranking = ""
                anchor_ranking_info = anchor_info_detail.xpath('span[@class="room-head-info-rank"]')
                if len(anchor_ranking_info) > 0:
                    anchor_ranking = anchor_ranking_info[0].text_content()
                    anchor_ranking = anchor_ranking.replace("\n", "")
                anchor_name = anchor_info_detail.xpath('span[starts-with(@class,"room-head-info-hostname")]')[0].text_content()
                room_subscriber = tree.xpath('//div[starts-with(@class,"room-head-tool-follow-count")]')[0].text_content()
                room_subscriber = room_subscriber.replace(",", "")

                #anchor lable and status info
                anchor_label = ""
                anchor_status = ""
                anchor_label_status_info = tree.xpath('//div[@class="room-head-info-title-wrapper"]')
                if len(anchor_label_status_info)==0:
                    anchor_label_status_info = tree.xpath('//div[starts-with(@class,"room-head-info-detail")]')
                anchor_label_info = anchor_label_status_info[0].findall("a")
                if len(anchor_label_info) > 0:
                    anchor_label = anchor_label_info[0].text_content()
                    anchor_status_info = anchor_label_info[0].xpath('@data-tips')
                    if len(anchor_status_info) > 0:
                        anchor_status = anchor_label_info[0].xpath('@data-tips')[0]

                #room view info
                room_viewer_info = tree.xpath('//div[@class="room-viewer-detail"]')
                if len(room_viewer_info)==0:
                    room_viewer_info = tree.xpath('//div[@class="room-head-person-num-detail"]')
                room_viewer_cur = room_viewer_info[0].findall("p")[1].findall("em")[0].text_content()
                room_viewer_acc = room_viewer_info[0].findall("p")[2].findall("em")[0].text_content()

                #room bamboo info
                room_bamboo_info = tree.xpath('//div[@class="room-bamboo-num"]')
                room_bamboo_num = ""
                if len(room_bamboo_info)>0:
                    room_bamboo_num = room_bamboo_info[0].text_content()
                else:
                    room_bamboo_info = tree.xpath('//span[starts-with(@class,"room-head-info__text room-bamboo-num")]')
                    room_bamboo_num = room_bamboo_info[0].text_content()[3:]
                room_viewer_acc = room_viewer_acc.replace(",", "")
                room_viewer_cur = room_viewer_cur.replace(",", "")
                room_bamboo_num = room_bamboo_num.replace(",", "")
                extracted = open('/home/ming/Sophia_yizhibo/panda/' + current_url[i] + '.csv', 'a')
                anchor_title = room_title+","+anchor_levl+","+anchor_ranking+","+anchor_name+","+room_subscriber+","+ anchor_label+","+room_viewer_cur+","+room_viewer_acc+","+room_bamboo_num
                print(anchor_title)
                extracted.write("#enter_to_scrape#," + str(datetime.now()) + "," + anchor_title + ",live stream begin\n")
                extracted.close()

        #if the current page finished
        if finished[i]:
            interest_bool = 0
            # if no interest url, then extract from the powerlist
            if len(interest_url) == 0:
                online_list = pandaranklist.get_oline_list()
                if len(online_list) == 0:
                    continue
                for online_entry in online_list:
                    if online_entry in current_url:
                        continue
                    else:
                        try:
                            driver.get("https://www.panda.tv/" + online_entry)
                            current_url[i] = online_entry
                            break
                        except:
                            timeout = 1
                            pass
            else:
                # extract url from the interest url
                try:
                    driver.get("https://www.panda.tv/" + interest_url[0])
                    current_url[i] = interest_url[0]
                    interest_url.pop(0)
                    interest_bool = 1
                except:
                    timeout = 1
                    pass
            # ignore if time out
            if timeout:
                timeout = 0
                continue
            time.sleep(5)
            interest_anchor[i] = interest_bool
            current_id[i] = int(current_url[i])
            previous[i] = 0
            finished[i] = 0
            # get the information of the anchor
            tree = myhtml.fromstring(driver.page_source)
            room_title_info = tree.xpath('//h1[@class="room-head-info-title"]')
            if len(room_title_info) == 0:
                room_title_info = tree.xpath('//span[starts-with(@class,"room-head-info__title")]')
            room_title = ""
            if len(room_title_info) > 0:
                room_title = room_title_info[0].text_content()
            room_title = room_title.replace("\n", "")
            anchor_info_detail = tree.xpath('//div[starts-with(@class,"room-head-info-detail")]')[0]
            anchor_levl = anchor_info_detail.findall("i")[0].xpath('@data-level')[0]
            anchor_ranking = ""
            anchor_ranking_info = anchor_info_detail.xpath('span[@class="room-head-info-rank"]')
            if len(anchor_ranking_info) > 0:
                anchor_ranking = anchor_ranking_info[0].text_content()
                anchor_ranking = anchor_ranking.replace("\n", "")
            anchor_name = anchor_info_detail.xpath('span[starts-with(@class,"room-head-info-hostname")]')[
                0].text_content()
            room_subscriber = tree.xpath('//div[starts-with(@class,"room-head-tool-follow-count")]')[0].text_content()
            room_subscriber = room_subscriber.replace(",", "")

            # anchor lable and status info
            anchor_label = ""
            anchor_status = ""
            anchor_label_status_info = tree.xpath('//div[@class="room-head-info-title-wrapper"]')
            if len(anchor_label_status_info) == 0:
                anchor_label_status_info = tree.xpath('//div[starts-with(@class,"room-head-info-detail")]')
            anchor_label_info = anchor_label_status_info[0].findall("a")
            if len(anchor_label_info) > 0:
                anchor_label = anchor_label_info[0].text_content()
                anchor_status_info = anchor_label_info[0].xpath('@data-tips')
                if len(anchor_status_info) > 0:
                    anchor_status = anchor_label_info[0].xpath('@data-tips')[0]

            # room view info
            room_viewer_info = tree.xpath('//div[@class="room-viewer-detail"]')
            if len(room_viewer_info) == 0:
                room_viewer_info = tree.xpath('//div[@class="room-head-person-num-detail"]')
            room_viewer_cur = room_viewer_info[0].findall("p")[1].findall("em")[0].text_content()
            room_viewer_acc = room_viewer_info[0].findall("p")[2].findall("em")[0].text_content()

            # room bamboo info
            room_bamboo_info = tree.xpath('//div[@class="room-bamboo-num"]')
            room_bamboo_num = ""
            if len(room_bamboo_info) > 0:
                room_bamboo_num = room_bamboo_info[0].text_content()
            else:
                room_bamboo_info = tree.xpath('//span[starts-with(@class,"room-head-info__text room-bamboo-num")]')
                room_bamboo_num = room_bamboo_info[0].text_content()[3:]
            room_viewer_acc = room_viewer_acc.replace(",", "")
            room_viewer_cur = room_viewer_cur.replace(",", "")
            room_bamboo_num = room_bamboo_num.replace(",", "")
            extracted = open('/home/ming/Sophia_yizhibo/panda/' + current_url[i] + '.csv', 'a')
            anchor_title = room_title + "," + anchor_levl + "," + anchor_ranking + "," + anchor_name + "," + room_subscriber + "," + anchor_label + "," + room_viewer_cur + "," + room_viewer_acc + "," + room_bamboo_num
            print(anchor_title)
            extracted.write("#enter_to_scrape#," + str(datetime.now()) + "," + anchor_title + ",live stream begin\n")
            extracted.close()
            #end of the loading phase

        #in normal state this should be the start of main code
        time.sleep(10 / TABS_NUM_CONSTANT)
        extracted = open('/home/ming/Sophia_yizhibo/panda/' + current_url[i] + '.csv', 'a')

        # driver.refresh()
        # get info of the anchor status, online or not
        tree = myhtml.fromstring(driver.page_source)
        anchor_info_detail = tree.xpath('//div[@class="room-head-info-title-wrapper"]')
        if len(anchor_info_detail) == 0:
            anchor_info_detail = tree.xpath('//div[starts-with(@class,"room-head-info-detail")]')
        anchor_status = ""
        anchor_label_info = anchor_info_detail[0].findall("a")
        if len(anchor_label_info) > 0:
            anchor_label = anchor_label_info[0].text_content()
            anchor_status_info = anchor_label_info[0].xpath('@data-tips')
            if len(anchor_status_info) > 0:
                anchor_status = anchor_label_info[0].xpath('@data-tips')[0]
        if anchor_status.find("休息")!=-1:
            finished[i] = 1
            fileHtml = open('/home/ming/Sophia_yizhibo/panda/html_' + current_url[i]+"_"+str(time.time()) + '.txt', 'w')
            fileHtml.write(driver.page_source)
            fileHtml.close()

        # get the messages on the right pane
        chat_message_info = tree.xpath('//ul[@class="room-chat-messages"]')[0]
        chat_message_list = chat_message_info.findall("li")
        if len(chat_message_list) < previous[i]:
            previous[i] = 0
        new_msg_list = chat_message_list[previous[i]:]
        msg_time = str(datetime.now())
        for chat_message_entry in new_msg_list:
            tag_class_name = chat_message_entry.xpath('@class')[0]
            if tag_class_name.startswith("room-chat-item room-chat-message"):
                fan_level = ""
                fan_group = ""
                icon_badge = ""
                fan_level_info = chat_message_entry.xpath('div[@class="room-chat-tags"]')
                if len(fan_level_info) > 0:
                    fan_level_span = fan_level_info[0].findall("span")
                    if len(fan_level_span) > 0:
                        for fan_level_entry in fan_level_span:
                            fan_level += "|" + fan_level_entry.xpath('@class')[0]
                    fan_group_span = fan_level_info[0].xpath('//span[@class="room-chat-tag-school-group-name"]')
                    if len(fan_group_span) > 0:
                        fan_group = fan_group_span[0].text_content()
                    icon_badge_a = fan_level_info[0].findall("a")
                    if len(icon_badge_a) > 0:
                        if len(icon_badge_a[0].findall("em")) > 0:
                            icon_badge += icon_badge_a[0].findall("em")[0].text_content()
                        if len(icon_badge_a[0].findall("div")) > 0:
                            icon_level = icon_badge_a[0].findall("div")[0].findall("span")
                            if len(icon_level) > 0:
                                icon_badge += icon_level[0].text_content()
                fan_name = chat_message_entry.xpath('span[@class="room-chat-user-name"]')[0].xpath("@data-name")[0]
                fan_text = chat_message_entry.xpath('span[@class="room-chat-content"]')[0].text_content()
                #print("#fan_chat,#"+msg_time+","+fan_group + "," + fan_level + ","+ icon_badge + "," + fan_name+","+fan_text+"\n")
                extracted.write("#fan_chat#,"+msg_time+","+fan_group + "," + fan_level + ","+ icon_badge + "," + fan_name+","+fan_text+"\n")
            if tag_class_name.endswith("room-chat-send-gift "):
                sender_name = chat_message_entry.xpath('span[@class="room-chat-user-name"]')[0].xpath("@data-name")[0]
                send_gift = chat_message_entry.xpath('span[@class="room-chat-send-gift-name"]')[0].text_content()
                send_num = str(1)
                send_num_info = chat_message_entry.xpath('span[@class="room-chat-send-gift-combo"]')
                if len(send_num_info) != 0:
                    send_num = send_num_info[0].text_content()
                #print("#fan_send_gift#,"+msg_time+","+sender_name + "," + send_num + "," + send_gift+"\n")
                extracted.write("#fan_send_gift#,"+msg_time+","+sender_name + "," + send_num + "," + send_gift+"\n")
            if tag_class_name.endswith("room-chat-send-bamboo "):
                sender_name = chat_message_entry.xpath('span[@class="room-chat-user-name"]')[0].xpath("@data-name")[0]
                send_gift = chat_message_entry.xpath('span[@class="room-chat-send-bamboo-gift"]')[0].text_content()
                send_num = str(1)
                send_num_info = chat_message_entry.xpath('span[@class="room-chat-send-bamboo-num"]')
                if len(send_num_info) != 0:
                    send_num = send_num_info[0].text_content()
                to_whom = chat_message_entry.xpath('span[@class="room-chat-send-bamboo-to"]')[0].text_content()
                #print("#fan_send_gift_to#,"+msg_time+","+sender_name + "," + send_num + "," + send_gift + "," + to_whom+"\n")
                extracted.write("#fan_send_gift_to#,"+msg_time+","+sender_name + "," + send_num + "," + send_gift + "," + to_whom+"\n")
            if tag_class_name.endswith("room-chat-hero-vip"):
                fan_name = chat_message_entry.xpath('@data-name')[0]
                fan_level = ""
                info_span = chat_message_entry.findall("span")[0].xpath('@class')[0]
                if not info_span.endswith("hero-vip-info"):
                    fan_level = info_span
                fan_action = "进入直播间"
                #print("#fan_enters#,"+msg_time+","+fan_level + "," + fan_name + "," + fan_action+"\n")
                extracted.write("#fan_enters#,"+msg_time+","+fan_level + "," + fan_name + "," + fan_action+"\n")
            if tag_class_name.endswith("room-chat-open-hero"):
                open_info = chat_message_entry.xpath('//span[@class="color-text"]')
                fan_name = ""
                open_level = ""
                action = ""
                if len(open_info) > 0:
                    fan_name = open_info[0].text_content()
                if len(open_info) > 1:
                    open_level = open_info[1].text_content()
                action_info = chat_message_entry.findall("span")[1].text_content()
                if action_info.find("开通了") != -1:
                    action = "在直播间内开通了"
                if action_info.find("") != -1:
                    action = "在直播间内续费了"
                #print("#fan_buy_level#,"+msg_time+","+fan_name + ","+action +","+ open_level+"\n")
                extracted.write("#fan_buy_level#,"+msg_time+","+fan_name + ","+action +","+ open_level+"\n")
        previous[i] = len(chat_message_list)

        if finished[i]:
            # 车站
            station_ticket_info = tree.xpath('//div[@class="rank-station-state-info"]')
            if len(station_ticket_info) > 0:
                station_ticket_list = station_ticket_info[0].xpath('span[@class="rank-station-state-info-desc"]')
                ticket_num = station_ticket_list[0].findall("a")[0].text_content()
                ticket_rank = station_ticket_list[1].findall("a")[0].findall("i")[1].text_content()
                #print("#anchor_station#"+ticket_num + "," + ticket_rank+"\n")
                extracted.write("#anchor_station#,"+ticket_num + "," + ticket_rank+"\n")
            # 周榜
            fangift_week_rank_top3_info = tree.xpath('//div[@class="rank-top-row-wrap clearfix"]')
            fangift_week_rank_long_list = tree.xpath('//div[@class="rank-row "]')
            if len(fangift_week_rank_top3_info) > 0:
                fangift_week_top3 = fangift_week_rank_top3_info[0].xpath('div[starts-with(@class, "rank-top-row")]')
                if len(fangift_week_top3) > 0:
                    rank_seq = 0
                    for fangift_week_top3_entry in fangift_week_top3:
                        rank_seq += 1
                        fan_info = fangift_week_top3_entry.xpath('div[@class="rank-user-name"]')[0]
                        fan_name = fan_info.findall("div")[0].xpath('@data-name')[0]
                        fan_level = fangift_week_top3_entry.findall("span")[0].xpath('@data-level')[0]
                        #print("#fan_gift_ranking#,"+str(rank_seq) + "," + fan_level + "," + fan_name+"\n")
                        extracted.write("#fan_gift_ranking#,"+str(rank_seq) + "," + fan_level + "," + fan_name+"\n")
            if len(fangift_week_rank_long_list) > 0:
                for fangift_week_long_entry in fangift_week_rank_long_list:
                    rank_seq += 1
                    fan_level = ""
                    fan_name = ""
                    fan_gift = ""
                    fan_info = fangift_week_long_entry.findall("span")
                    if len(fan_info)>0:
                        rank_seq = fan_info[0].text_content()
                    if len(fan_info)>1:
                        fan_level = fan_info[1].xpath('@data-level')[0]
                    if len(fan_info) > 2:
                        fan_name = fan_info[2].xpath('@data-name')[0]
                    if len(fan_info) > 3:
                        fan_gift = fan_info[3].text_content()
                    #print("#fan_gift_ranking#,"+str(rank_seq) + "," + fan_level + "," + fan_name+","+fan_gift+"\n")
                    extracted.write("#fan_gift_ranking#,"+str(rank_seq) + "," + fan_level + "," + fan_name+","+fan_gift+"\n")
            # 英雄
            hero_top3_info = tree.xpath('//div[starts-with(@class, "hero-rank-top-row-wrap clearfix")]')
            if len(hero_top3_info) > 0:
                hero_top3_list = hero_top3_info[0].xpath('div[starts-with(@class, "hero-rank-top-row")]')
                if len(hero_top3_list) > 0:
                    for hero_top3_entry in hero_top3_list:
                        hero_level = hero_top3_entry.findall("span")[0].xpath('@class')[0]
                        hero_nickname = hero_top3_entry.findall("span")[1].xpath('@data-name')[0]
                        #print("#hero_fans#,"+hero_level + ","+hero_nickname + "\n")
                        extracted.write("#hero_fans#," + hero_level + ","+hero_nickname + "\n")
            hero_long_info = tree.xpath('//div[starts-with(@class, "hero-rank-row-scroll")]')
            if len(hero_long_info) > 0:
                hero_long_list = hero_long_info[0].xpath('div[@class="hero-rank-row"]')
                for hero_long_entry in hero_long_list:
                    hero_level = hero_long_entry.findall("span")[0].xpath('@class')[0]
                    hero_nickname = hero_long_entry.findall("span")[1].xpath('@data-name')[0]
                    #print("#hero_fans#," + hero_level + "," + hero_nickname + "\n")
                    extracted.write("#hero_fans#," + hero_level + "," + hero_nickname + "\n")
        extracted.close()
