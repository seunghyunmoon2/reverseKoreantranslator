# -*- coding: utf-8 -*-
"""HeadsupNConverter.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1QmE2t3rxllDk4aVJpOUX5-QJ38OjQ9db

# Could be useful links

[webdriver-close](https://stackoverflow.com/questions/15067107/difference-between-webdriver-dispose-close-and-quit)

[seleniumDOCUMENT](https://selenium-python.readthedocs.io/)

https://stackoverflow.com/questions/36840886/how-to-copy-and-paste-a-value-using-selenium

https://sqa.stackexchange.com/questions/30596/how-to-store-copied-text-to-a-string-in-selenium-webdriver/40426

# 웹드라이버 실험 <- 복사해가면 좋겠다. 임포트도 위로 당겨오고
"""

# set options to be headless, ..
from selenium import webdriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# open it, go to a website, and get results
driver = webdriver.Chrome('chromedriver',options=options)
#wd.get("https://www.website.com")
#print(wd.page_source)  # results

driver.get('https://thtl1999.github.io/God-sejong/')

driver.find_element_by_xpath('//*[@id="input-area"]')

"""# 문장나누기"""

!pip install kss
!apt install chromium-chromedriver
!pip install selenium

import kss
t = ''
# 원본. 처리 전
s = """요번에 오랜만에 외국여행을 친구들이랑 왔는데 여기 집주인이 아주 아니에요. 가격도 그렇게 싼 편이 아닌데 서비스가 엉망이고요, 화장실도 더럽고 우리가 뭐라 하니 화만 내네요 ㅠ.ㅠ 여기 주변 음식점도 다 맛 없고 분위기도 별로에요.


여기 리뷰 잘 써주면 할인해준다고는 해서 쓰고있는데 이 리뷰 보시고 다들 잘 거르시길 바랍니다..."""
for sent in kss.split_sentences(s):
    print(sent, type(sent))
    t += sent

print(type(t))

print(t) # 문장 구분 완료

"""# 중간완성본

'''요번에 오랜만에 외국여행을 친구들이랑 왔는데 여기 집주인이 아주 아니에요. 가격도 그렇게 싼 편이 아닌데 서비스가 엉망이고요, 화장실도 더럽고 우리가 뭐라 하니 화만 내네요 ㅠ.ㅠ 여기 주변 음식점도 다 맛 없고 분위기도 별로에요.

여기 리뷰 잘 써주면 할인해준다고는 해서 쓰고있는데 이 리뷰 보시고 다들 잘 거르시길 바랍니다...'''
"""

!pip install kss
!apt install chromium-chromedriver
!pip install selenium

import kss
from selenium import webdriver
import pyperclip
import time
import csv

"""* colab에서 실행시 해줘야함."""

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome('chromedriver',options=options)

"""* 코랩 실행 시 csv 파일로 저장하는걸 아직 안해서 두 단계로 해야함.
    
    1. preprocess_comment는 코랩에서 실행(패키지가 c++ 기반인데 PC 안깔아놔서 안돌아감.
    2. processed 가지고 그 이후는 PC 에서 돌리면 됨
    
    * (웹드라이버도 colab에서 실행하려면 윗 셀.)
"""

class Converter:
    
    def preprocess_comment(cmt):
        processed = ''
        for sent in kss.split_sentences(cmt):
            processed = processed + ' ' +  sent
            
        return processed
    
    def fetch_from_Godsejong(processed): # processed cmt from PREPORCESS_COMMENT
        driver = webdriver.Chrome('C:\chromedriver.exe') # PC 디렉토리
        driver.get('https://thtl1999.github.io/God-sejong/')
        
        driver.find_element_by_xpath('//*[@id="addPraise"]').click() # 앞뒤칭찬빼기
        driver.find_element_by_xpath('//*[@id="cambridge"]').click() # 캠브릿지연결구과
        original = driver.find_element_by_xpath('//*[@id="input-area"]') # input box
        convert_btn = driver.find_element_by_xpath('//*[@id="convert_button"]') #convert btn
        to_clip_board = driver.find_element_by_xpath('//*[@id="copy_button"]') # copy to clipboard btn
        
        original.clear() # clear input box
        original.send_keys(processed) # send keys
        
        converted = []
        
        for i in range(1000): # 8072/10000 였음. 문장이 짧으면 500개정도도 가능.
            convert_btn.click()       # 바꾸고
            driver.implicitly_wait(3)
            to_clip_board.click()     # 복사하고
            driver.implicitly_wait(3)
            converted.append(pyperclip.paste()) # 리스트에 넣는다
            driver.implicitly_wait(3)

        driver.quit()
        converted = list(set(converted))
        
        return converted
    
    def split_converted_list(converted): # 각 코멘트를 단어별로(빈칸으로 split) 묶어준다. 안그러면 한글자씩 들어감.
        splited = []
        for line in converted:
            splited.append(line.split(' '))
        
        return splited
        
    def export_to_csv(splited):
        with open('full_test.csv','w+',newline='') as f:
            write = csv.writer(f)
            write.writerows(splited)

import kss
cmt = """
요번에 오랜만에 외국여행을 친구들이랑 왔는데 여기 집주인이 아주 아니에요. 가격도 그렇게 싼 편이 아닌데 서비스가 엉망이고요, 화장실도 더럽고 우리가 뭐라 하니 화만 내네요 ㅠ.ㅠ 여기 주변 음식점도 다 맛 없고 분위기도 별로에요.

여기 리뷰 잘 써주면 할인해준다고는 해서 쓰고있는데 이 리뷰 보시고 다들 잘 거르시길 바랍니다...
"""

print(Converter.preprocess_comment(cmt))

processed = ' 요번에 오랜만에 외국여행을 친구들이랑 왔는데 여기 집주인이 아주 아니에요. 가격도 그렇게 싼 편이 아닌데 서비스가 엉망이고요, 화장실도 더럽고 우리가 뭐라 하니 화만 내네요 ㅠ.ㅠ 여기 주변 음식점도 다 맛 없고 분위기도 별로에요. 여기 리뷰 잘 써주면 할인해준다고는 해서 쓰고있는데 이 리뷰 보시고 다들 잘 거르시길 바랍니다...'
converted = Converter.fetch_from_Godsejong(processed)
splited = Converter.split_converted_list(converted)
Converter.export_to_csv(splited)

"""# 문장 인코딩해주기

[여기가 유력함](https://github.com/warnikchow/paraKQC/blob/master/han2one.py)  
[뭐하는인간들이냐.유력22](https://github.com/kaniblu/hangul-utils)   
[뭐하는2](http://aidev.co.kr/nlp/8948)   

[한글문자 초중종성 변환.1](https://github.com/neotune/python-korean-handler/blob/master/korean_handler.py)   
[변환.2](https://frhyme.github.io/python/python_korean_englished/)
[변환.3](https://m.blog.naver.com/raf629/221894210886)


[한글 문자열 자르기](https://blog.naver.com/PostView.nhn?blogId=wideeyed&logNo=221681943732&parentCategoryNo=&categoryNo=&viewDate=&isShowPopularPosts=false&from=postView)   
[한글,영어 구분](https://alreadyusedadress.tistory.com/68)

[그럴듯한거찾았는데별건없는듯하다](https://ifyourfriendishacker.tistory.com/5)   



나머지도 혹시 모르니...  
https://github.com/gusdnd852/kocrawl  
https://github.com/Huffon/nlp-various-tutorials  
https://github.com/YBIGTA/DeepNLP-Study  
https://github.com/kakaobrain/KorNLUDatasets  
https://github.com/shbictai/narrativeKoGPT2  
https://github.com/likejazz/korean-sentence-splitter   
https://github.com/IBM/tensorflow-hangul-recognition#4-convert-images-to-tfrecords

## 한글 스페이싱 - 긁어온 코멘트를 스페이스 없이 가져와서 학습시키고 다시 스페이싱시키기? 이게 필요한가? - 일단은 뭔가 대박이다

[스페이싱1-1](http://freesearch.pe.kr/archives/4647)   
[스페이싱1-github](https://github.com/youngwoos/kospacing)   
[스페이싱2](https://mrchypark.github.io/post/kospacing-%ED%95%9C%EA%B8%80-%EB%9D%84%EC%96%B4%EC%93%B0%EA%B8%B0-%ED%8C%A8%ED%82%A4%EC%A7%80%EB%A5%BC-%EC%82%AC%EC%9A%A9%ED%95%B4%EB%B3%B4%EC%9E%90/)

# 정규식으로 한글만 가져오기 - 코멘트 긁어올 때?

[정규식한글가져오기블로그](https://jokergt.tistory.com/52)
"""
