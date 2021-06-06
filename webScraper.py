# 웹스크래퍼

import re
import requests
import webbrowser
from bs4 import BeautifulSoup
from tkinter import *

root = Tk()
root.title("웹 스크래퍼")
root.geometry("650x650") # 가로 * 세로

def delete():
    webcontent.delete(0, END)

def create_soup(url):
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"}
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    return soup

def print_news(index, title, link):
    webcontent.insert(END, str("{}. {}".format(index+1, title)))
    webcontent.insert(END, str("  (링크) : {} ".format(link)))
    webcontent.insert(END, str())

def scrape_weather():
    webcontent.insert(END, str("[오늘의 날씨]"))
    webcontent.insert(END, str())
    url = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=%EC%84%9C%EC%9A%B8+%EB%82%A0%EC%94%A8"
    soup = create_soup(url)
    cast = soup.find("p", attrs={"class": "cast_txt"}).get_text()
    curr_temp = soup.find("p", attrs={"class":"info_temperature"}).get_text().replace("도씨", "")
    min_temp = soup.find("span", attrs={"class":"min"}).get_text() # 최저온도
    max_temp = soup.find("span", attrs={"class":"max"}).get_text() # 최고온도
    morning_rain_rate = soup.find("span", attrs={"class":"point_time morning"}).get_text().strip() # 오전 강수확률
    afternoon_rain_rate = soup.find("span", attrs={"class":"point_time afternoon"}).get_text().strip() # 오후 강수확률
    
    dust = soup.find("dl", attrs={"class":"indicator"})
    pm10 = dust.find_all("dd")[0].get_text() # 미세먼지
    pm25 = dust.find_all("dd")[1].get_text() # 초미세먼지
    

    # 출력
    webcontent.insert(END, str(cast))
    webcontent.insert(END, str("현재 {} (최저 {} / 최고 {})".format(curr_temp, min_temp, max_temp)))
    webcontent.insert(END, str("오전 {} / 오후 {}".format(morning_rain_rate, afternoon_rain_rate)))
    webcontent.insert(END, str())
    webcontent.insert(END, str("미세먼지 {}".format(pm10)))
    webcontent.insert(END, str("초미세먼지 {}".format(pm25)))
    webcontent.insert(END, str())

def scrape_headline_news():
    webcontent.insert(END, str("[헤드라인 뉴스]"))
    webcontent.insert(END, str())
    url = "https://news.naver.com"
    soup = create_soup(url)
    news_list = soup.find("ul", attrs={"class":"hdline_article_list"}).find_all("li", limit=10)
    for index, news in enumerate(news_list):
        title = news.find("a").get_text().strip()
        link = url + news.find("a")["href"]
        print_news(index, title, link)

def scrape_it_news():
    webcontent.insert(END, str("[IT 뉴스]"))
    webcontent.insert(END, str())
    url = "https://news.naver.com/main/list.nhn?mode=LS2D&mid=shm&sid1=105&sid2=230"
    soup = create_soup(url)
    news_list = soup.find("ul", attrs={"class":"type06_headline"}).find_all("li", limit=10) # 3개까지만 가져오기
    for index, news in enumerate(news_list):
        a_idx = 0
        img = news.find("img")
        if img:
            a_idx = 1 # img 태그가 있으면 1번째 a 태그의 정보를 사용
        
        a_tag = news.find_all("a")[a_idx]
        title = a_tag.get_text().strip()
        link = a_tag["href"]
        print_news(index, title, link)

def scrape_english():
    webcontent.insert(END, str("[오늘의 영어 회화]"))
    webcontent.insert(END, str())
    url = "https://www.hackers.co.kr/?c=s_eng/eng_contents/I_others_english&keywd=haceng_submain_lnb_eng_I_others_english&logger_kw=haceng_submain_lnb_eng_I_others_english#;"
    soup = create_soup(url)
    sentences = soup.find_all("div", attrs={"id":re.compile("^conv_kor_t")})
    webcontent.insert(END, str("(영어 지문)"))
    for sentence in sentences[len(sentences)//2:]:
        webcontent.insert(END, str(sentence.get_text().strip()))
    webcontent.insert(END, str())

    webcontent.insert(END, str("(한글 지문)"))
    for sentence in sentences[:len(sentences)//2]:
        webcontent.insert(END, str(sentence.get_text().strip()))
    webcontent.insert(END, str())

# 웹 선택 프레임
frame_web = LabelFrame(root, text="스크래핑을 원하는 것을 선택해주세요")
frame_web.pack(side="top", expand=True)

btn_1 = Button(frame_web, text="오늘의 날씨", width=20, height=2, command=scrape_weather)
btn_2 = Button(frame_web, text="헤드라인 뉴스", width=20, height=2, command=scrape_headline_news)
btn_3 = Button(frame_web, text="IT 뉴스", width=20, height=2, command=scrape_it_news)
btn_4 = Button(frame_web, text="오늘의 영어 회화", width=20, height=2, command=scrape_english)

btn_1.grid(row=0, column=0, sticky=N+E+W+S, padx=3, pady=3)
btn_2.grid(row=0, column=1, sticky=N+E+W+S, padx=3, pady=3)
btn_3.grid(row=0, column=2, sticky=N+E+W+S, padx=3, pady=3)
btn_4.grid(row=0, column=3, sticky=N+E+W+S, padx=3, pady=3)

# 컨텐츠 프레임
frame_content = Frame(root)
frame_content.pack(fill="both", padx=5, pady=5)

scrollbar = Scrollbar(frame_content)
scrollbar.pack(side="right", fill="y")

webcontent = Listbox(frame_content, selectmode="extended", height=38, yscrollcommand=scrollbar.set)
webcontent.pack(side="left", fill="both", expand=True)
scrollbar.config(command=webcontent.yview)

# 실행 프레임
frame_run = Frame(root)
frame_run.pack(fill="x", padx=5, pady=5)

btn_close = Button(frame_run, padx=5, pady=5, text="닫기", width=12, command=root.quit)
btn_close.pack(side="right", padx=5, pady=5)

btn_start = Button(frame_run, padx=5, pady=5, text="지우기", width=12, command=delete)
btn_start.pack(side="right", padx=5, pady=5)

root.resizable(False, False)
root.mainloop()