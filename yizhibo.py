# This Python file uses the following encoding: utf-8
import sys
import lxml.html as myhtml

from downloader import Downloader
import json
from selenium import webdriver

import time
from datetime import datetime
#from selenium import selenium
#from FlashSelenium import FlashSelenium
from pyvirtualdisplay import Display

reload(sys)
sys.setdefaultencoding('utf8')
TABS_NUM_CONSTANT = 6
display = Display(visible=0, size=(1280, 1024))
display.start()
option = webdriver.ChromeOptions()
option.add_argument("--disable-component-update")
option.add_argument("--allow-running-insecure-content")
option.add_argument("--disable-web-security")
option.add_argument("--ppapi-flash-path=/home/kxdadmin/.config/google-chrome/PepperFlash/26.0.0.131/libpepflashplayer.so")
option.add_argument("--allow-outdated-plugins")
#driver = webdriver.Chrome(executable_path="/home/krude/Downloads/chromedriver", chrome_options=option)
driver = webdriver.Chrome(executable_path="/home/wanting/Sophia_yizhibo/chromedriver")
finished = [1]
interest_anchor = [0]
interest_anchid = [1]
currentUrl = ["a"]
file_time = ["a"]
anchor_title = ""
previous = [0]
pregiftentry = [0]
#try to open tabs
for j in range(TABS_NUM_CONSTANT-1):
    time.sleep(1)
    driver.execute_script("window.open('');")
    finished.append(1)
    interest_anchor.append(0)
    interest_anchid.append(1)
    currentUrl.append("a")
    file_time.append("a")
    previous.append(0)
    pregiftentry.append(0)
first_time = 1
D = Downloader()
html_list = D("https://www.yizhibo.com/www/web/get_pc_power_list")
timeout = 0
anchor_id_list = [110938741, 14208778, 4141175, 186526607, 2640762, 33403585, 55604544, 418769, 213198916, 66654597, 145761090, 305579853, 341092662, 268836621, 260911901, 236201509, 69848573, 34406507, 56648154, 90732155]
interest_url=[]
for anchor_id in anchor_id_list:
    try:
        url_str = "https://www.yizhibo.com/member/personel/user_works?memberid=" + str(anchor_id)
        anchor_page = D(url_str)
        source_tree = myhtml.fromstring(anchor_page)
        begin_time_info = \
            source_tree.xpath('//ul[starts-with(@class, "index_all")]')[0].findall("li")[0].findall("div")[0]
        begin_time = begin_time_info.text_content()
        if begin_time.find("直播中") != -1:
            live_url = \
                begin_time_info.xpath('div[starts-with(@class, "index_img")]')[0].findall("a")[0].xpath(
                    "@href")[0]
            interest_url.append(live_url)
            # print(live_url)
    except:
        continue
prev_time = datetime.now()
while 1:
    #check state of anchors of interest at time interval
    #if memberid not in list, then detect whether the anchor launcher new live stream
    curr_time = datetime.now()
    secDiff = (curr_time - prev_time).seconds
    #if time interval longer than 10 minutes, check the interest anchors
    if secDiff > 600:
        prev_time = curr_time
        for anchor_id in anchor_id_list:
            if anchor_id in interest_anchid:
                continue
            try:
                url_str = "https://www.yizhibo.com/member/personel/user_works?memberid=" + str(anchor_id)
                anchor_page = D(url_str)
                source_tree = myhtml.fromstring(anchor_page)
                begin_time_info = \
                    source_tree.xpath('//ul[starts-with(@class, "index_all")]')[0].findall("li")[0].findall("div")[0]
                begin_time = begin_time_info.text_content()
                if begin_time.find("直播中") != -1:
                    live_url = \
                        begin_time_info.xpath('div[starts-with(@class, "index_img")]')[0].findall("a")[0].xpath(
                            "@href")[0]
                    if live_url not in interest_url:
                        interest_url.append(live_url)
                    #print(live_url)
            except:
                continue
    for i in range(TABS_NUM_CONSTANT):
        driver.switch_to.window(driver.window_handles[i])
        #if not of interest anchor, and there is online interest anchor
        if interest_anchor[i]==0:
            if len(interest_url)!=0:
                # pop up the url, navigate to that url, get info
                # set the value of interest_anchor[i], interest_anchid[i], finished[i]
                try:
                    driver.get("http://www.yizhibo.com" + interest_url[0])
                    currentUrl[i] = interest_url[0]
                    interest_url.pop(0)
                except:
                    timeout = 1
                    pass
                if timeout:
                    timeout = 0
                    continue
                interest_anchor[i]=1
                previous[i] = 0
                pregiftentry[i] = 0
                time.sleep(3)
                # get the information of the anchor
                tree = myhtml.fromstring(driver.page_source)
                try:
                    anchor_info = tree.xpath('//div[@id="J_anchorinfo" and @class="anchorinfo clearfix pr"]')[0]
                    anchorinfo = anchor_info.xpath('div[@class="info"]')[0]
                    anchorinforlist = anchorinfo.findall("div")
                    anchorname_level = anchorinforlist[0]
                    anchormoney = anchorinfo.xpath('div[@class="id"]')[0]
                    anchorname = anchorname_level.findall("a")[0].text_content()
                    anchorlevel = anchorname_level.findall("div")[0].xpath('@class')[0]
                    anchormoneylevel = anchormoney.text_content()
                    anchor_title = anchorname + "," + anchorlevel + "," + anchormoneylevel + ","
                    anchor_cover = tree.xpath('//div[@class="cover" and @id="J_cover"]')[0]
                    anchor_id_hot = anchor_cover.xpath('div[starts-with(@class, "topicon")]')
                    anchor_id = anchor_id_hot[0].findall("span")[0].text_content()
                    anchor_hot = anchor_id_hot[1].findall("span")[0].text_content()
                    anchor_title = anchor_title + anchor_id + "," + anchor_hot
                    # love_group of the anchor
                    love_group_msg_clearfix = tree.xpath('//div[starts-with(@class, "love_group_msg")]')[0]
                    love_group_name = love_group_msg_clearfix.xpath('span[starts-with(@class, "fl")]')[0].text_content()
                    love_group_num = love_group_msg_clearfix.xpath('i[@class="fl"]')[1].text_content()
                    anchor_title = anchor_title + "," + love_group_name + love_group_num
                    love_level_clearfix = tree.xpath('//div[starts-with(@class, "love_level")]')[0]
                    love_level = love_level_clearfix.findall("span")[0].xpath('@class')[0]
                    love_value = love_level_clearfix.findall("div")[0].findall("i")[0].text_content()
                except:
                    continue
                    pass
                anchor_title = anchor_title + "," + love_level + "," + love_value
                print(anchor_title)
                file_time[i] = anchor_id[7:]
                interest_anchid[i] = int(anchor_id[7:])
                extracted = open('/home/wanting/Sophia_yizhibo/' + file_time[i] + '.csv', 'a')
                extracted.write("#enter_to_scrape#," + str(datetime.now()) + "," + anchor_title + ",live stream begin\n")
                extracted.close()
                finished[i] = 0
        if finished[i]:
            interest_bool = 0
            if len(interest_url)==0:
                #if no interest url, then extract from the powerlist
                if first_time:
                    pass
                else:
                    html_list = D("https://www.yizhibo.com/www/web/get_pc_power_list")
                parsed_json = json.loads(html_list)
                data = parsed_json['data']
                for power_entry in data:
                    if power_entry['liveurl'] in currentUrl:
                        continue
                    else:
                        try:
                            driver.get("http://www.yizhibo.com" + power_entry['liveurl'])
                            currentUrl[i] = power_entry['liveurl']
                            break
                        except:
                            timeout = 1
                            pass
            else:
                #extract url from the interest url
                try:
                    driver.get("http://www.yizhibo.com" + interest_url[0])
                    currentUrl[i] = interest_url[0]
                    interest_url.pop(0)
                    interest_bool = 1
                except:
                    timeout = 1
                    pass

            if timeout:
                timeout = 0
                continue
            interest_anchor[i] = interest_bool
            previous[i] = 0
            pregiftentry[i] = 0
            time.sleep(3)
            # get the information of the anchor
            try:
                tree = myhtml.fromstring(driver.page_source)
            except:
                continue
            try:
                anchor_info = tree.xpath('//div[@id="J_anchorinfo" and @class="anchorinfo clearfix pr"]')[0]
                anchorinfo = anchor_info.xpath('div[@class="info"]')[0]
                anchorinforlist = anchorinfo.findall("div")
                anchorname_level = anchorinforlist[0]
                anchormoney = anchorinfo.xpath('div[@class="id"]')[0]
                anchorname = anchorname_level.findall("a")[0].text_content()
                anchorlevel = anchorname_level.findall("div")[0].xpath('@class')[0]
                anchormoneylevel = anchormoney.text_content()
                anchor_title = anchorname + "," + anchorlevel + "," + anchormoneylevel + ","
                anchor_cover = tree.xpath('//div[@class="cover" and @id="J_cover"]')[0]
                anchor_id_hot = anchor_cover.xpath('div[starts-with(@class, "topicon")]')
                anchor_id = anchor_id_hot[0].findall("span")[0].text_content()
                anchor_hot = anchor_id_hot[1].findall("span")[0].text_content()
                anchor_title = anchor_title+anchor_id + "," + anchor_hot
                # love_group of the anchor
                love_group_msg_clearfix = tree.xpath('//div[starts-with(@class, "love_group_msg")]')[0]
                love_group_name = love_group_msg_clearfix.xpath('span[starts-with(@class, "fl")]')[0].text_content()
                love_group_num = love_group_msg_clearfix.xpath('i[@class="fl"]')[1].text_content()
                anchor_title = anchor_title + ","+love_group_name + love_group_num
                love_level_clearfix = tree.xpath('//div[starts-with(@class, "love_level")]')[0]
                love_level = love_level_clearfix.findall("span")[0].xpath('@class')[0]
                love_value = love_level_clearfix.findall("div")[0].findall("i")[0].text_content()
            except:
                continue
                pass
            anchor_title = anchor_title +","+love_level + "," + love_value
            print(anchor_title)
            file_time[i] = anchor_id[7:]
            interest_anchid[i] = int(anchor_id[7:])
            extracted = open('/home/wanting/Sophia_yizhibo/' + file_time[i] + '.csv', 'a')
            extracted.write("#enter_to_scrape#," + str(datetime.now()) + "," + anchor_title + ",live stream begin\n")
            extracted.close()
            finished[i] = 0

        time.sleep(10/TABS_NUM_CONSTANT)
        extracted = open('/home/wanting/Sophia_yizhibo/' + file_time[i] + '.csv', 'a')

        # driver.refresh()
        # get the gifting info
        htmlStr = driver.page_source
        if htmlStr.find("直播已经结束") != -1:
            fileHtml = open('/home/wanting/Sophia_yizhibo/html_'+str(i)+'.txt', 'w')
            fileHtml.write(driver.page_source)
            fileHtml.close()
            finished[i] = 1
        tree = myhtml.fromstring(htmlStr)
        # tree.make_links_absolute('https://www.yizhibo.com')
        gifts = tree.xpath('//ul[@id="J_gift_his"]')
        giftlist = gifts[0].findall("li")
        if len(giftlist) < pregiftentry[i]:
            pregiftentry[i] = 0
        newgiftlist = giftlist[pregiftentry[i]:]
        gift_time = str(datetime.now())
        for giftentry in newgiftlist:
            try:
                gift_group = " "
                gifts = giftentry.findall("div")
                nickname = gifts[0].text_content()
                level_group_name = gifts[0].findall("div")
                level = level_group_name[0].xpath('@class')[0]
                if len(level_group_name) > 1:
                    gift_group = level_group_name[1].text_content()
                    nickname = nickname.replace(gift_group, "")
                action = gifts[1].text_content()
                gift_icon = gifts[2].findall("img")[0].xpath('@src')[0]
                print(gift_time + "|" + level + "|" + nickname + "|" + action + "|" + gift_icon)
                print(giftentry.text_content())
                extracted.write(
                    "#gift_entry#," + gift_time + "," + level + "," + gift_group + "," + nickname + "," + action + "," + gift_icon + "\n")
            except:
                extracted.write("#gift_entry#," + gift_time + "," + giftentry.text_content() + ", gift_exception\n")
                pass
        pregiftentry[i] = len(giftlist)

        message = tree.xpath('//div[@id="J_msglist" and @class="msglist J_scroll"]')
        msglist = message[0].xpath('div[starts-with(@class, "msg")]')
        msglist = msglist[1:]
        if len(msglist) < previous[i]:
            previous[i] = 0
        newmsglist = msglist[previous[i]:]
        msg_time = str(datetime.now())
        for msgentry in newmsglist:
            try:
                class_name = msgentry.xpath('@class')[0]
                if class_name.startswith('msg_1'):
                    # print(html.tostring(msgentry))
                    clearfix = msgentry.find_class("clearfix")[0]
                    level = clearfix.findall("span")[0].xpath('@class')[0]
                    level = level.replace(" fl", "")
                    group = ""
                    if len(clearfix.findall("div")) != 0:
                        group = clearfix.findall("div")[0].text_content()
                    nickname = clearfix.findall("span")[1].text_content()
                    if level.startswith("gui"):
                        nickname = clearfix.findall("span")[2].text_content()
                    content = msgentry.find_class("content")[0].text_content()
                    print(msg_time + "|" + level + "|" + group + "|" + nickname + "|" + content)
                    extracted.write(
                        "#chat_of_fans#," + msg_time + "," + level + "," + group + "," + nickname + "," + content + "\n")
                if class_name.startswith('msg_3'):
                    print("#time_script#|" + msg_time + "|" + msgentry.text_content())
                    extracted.write(
                        "#time_script#," + msg_time + "," + msgentry.text_content() + ", time_synchronize\n")
                if class_name.endswith('msg_2_1'):
                    try:
                        span = msgentry.findall("span")[0]
                        nickname = span.text_content()
                        span = span.findall("span")[0]
                        level = span.xpath('@class')[0]
                        print(msg_time + "|" + level + "|" + nickname + "|" + "进入直播间")
                        extracted.write("#fan_enter#," + msg_time + "," + level + ",normal," + nickname + "," + "进入直播间\n")
                    except:
                        span = msgentry.findall("span")[0]
                        level = span.xpath('@class')[0]
                        abbr = msgentry.findall("abbr")[0]
                        em = msgentry.findall("em")[0]
                        nickname = abbr.text_content()
                        noble = em.xpath('@class')[0]
                        noble = noble + span.text_content()
                        print(msg_time + "|" + level + "|" + noble + "|" + nickname + "|" + "来捧场了，欢迎！")
                        extracted.write("#fan_enter#," + msg_time + "," + level + "," + noble + ", "+ nickname + "," + "来捧场了，欢迎！\n")
                if class_name.endswith('msg_2_2'):
                    span = msgentry.findall("span")[0]
                    text = span.text_content()
                    span = span.findall("span")[0]
                    pos = text.find("关注了主播")
                    nickname = text[:pos]
                    level = span.xpath('@class')[0]
                    print(msg_time + "|" + level + "|" + nickname + "|" + "关注了主播")
                    extracted.write("#fan_hashtag#," + msg_time + "," + level + "," + nickname + "," + "关注了主播\n")
                print(msgentry.text_content())
            except:
                extracted.write("#fan_enter#," + msg_time + "," + msgentry.text_content() + ", msg_exception\n")
                pass
        previous[i] = len(msglist)

        # get the ranking, 贵宾,场榜 ,总榜,观众席
        if finished[i]:
            all_gift_ranking = tree.xpath('//div[@class="togp" and @id="J_tog_1"]')[0]
            four_ranking_list = all_gift_ranking.xpath('ul[starts-with(@class,"rank_1 J_scroll")]')
            vip_audience_list = four_ranking_list[0].findall("li")
            venue_ranking_list = four_ranking_list[1].findall("li")
            allhistory_ranking = four_ranking_list[2].findall("li")
            audience_list = four_ranking_list[3].findall("li")
            # true love box
            true_love_box = tree.xpath('//div[@class="true_love_box"]')[0]
            true_love_ranking = true_love_box.xpath('//ul[@class="hover_con1"]')[0]
            true_love_list = true_love_ranking.findall("li")
            if len(true_love_list):
                extracted.write("true_love:\n")
                for true_love_entry in true_love_list:
                    try:
                        true_love_level = true_love_entry.findall("span")[0].xpath("@class")[0]
                        true_love_name = true_love_entry.findall("em")[0].text_content()
                    except:
                        continue
                        pass
                    extracted.write("true_love_ranking," + true_love_level + "," + true_love_name + "\n")
            # other ranking info
            if (len(vip_audience_list)):
                extracted.write("贵宾:\n")
                vip_level = ""
                vip_name = ""
                vip_value = ""
                for vip_entry in vip_audience_list:
                    try:
                        vip_level = vip_entry.findall("span")[0].xpath("@class")[0]
                        vip_name = vip_entry.findall("i")[0].text_content()
                        vip_value = vip_entry.findall("div")[0].text_content()
                    except:
                        continue
                        pass
                    extracted.write("vip_entry," + vip_level + "," + vip_name + "," + vip_value + "\n")
            if (len(venue_ranking_list)):
                extracted.write("场榜:\n")
                venue_level = ""
                venue_name = ""
                venue_value = ""
                for venue_entry in venue_ranking_list:
                    try:
                        venue_name_level = venue_entry.xpath('div[@class="nickname"]')[0].findall("span")[0]
                        venue_name = venue_name_level.text_content()
                        venue_level = venue_name_level.findall("span")[0].xpath('@class')[0]
                        venue_value = venue_entry.xpath('div[@class="sort"]')[0].text_content()
                    except:
                        continue
                        pass
                    extracted.write("venue_entry," + venue_level + "," + venue_name + "," + venue_value + "\n")
            if (len(allhistory_ranking)):
                extracted.write("总榜:\n")
                history_level = ""
                history_name = ""
                history_value = ""
                for history_entry in allhistory_ranking:
                    try:
                        history_name_level = history_entry.xpath('div[@class="nickname"]')[0].findall("span")[0]
                        history_name = history_name_level.text_content()
                        history_level = history_name_level.findall("span")[0].xpath('@class')[0]
                        history_value = history_entry.xpath('div[@class="sort"]')[0].text_content()
                    except:
                        continue
                        pass
                    extracted.write(
                        "all_history_entry," + history_level + "," + history_name + "," + history_value + "\n")
            if (len(audience_list)):
                extracted.write("观众席:\n")
                audience_level = ""
                audience_name = ""
                for audience_entry in audience_list:
                    try:
                        audience_name_level = audience_entry.findall("span")[0]
                        audience_name = audience_name_level.text_content()
                        audience_level = audience_name_level.findall("span")[0].xpath('@class')[0]
                    except:
                        continue
                        pass
                    extracted.write("audience_entry," + audience_level + "," + audience_name + "\n")

        extracted.close()
    first_time = 0

