from selenium import webdriver

p1 = re.compile('[가-힣]{4}[시] [가-힣]+[구] [0-9가-힣]+[길|로] [0-9\-0-9]+|[가-힣]+[도] [가-힣]+[시] [0-9가-힣]+[길|로] [0-9\-0-9]+|[가-힣]+[도] [가-힣]+[시] [0-9가-힣]+[구] [0-9가-힣]+[길|로] [0-9\-0-9]+|[가-힣]+[도] [가-힣]+[시] [가-힣]+[읍] [0-9가-힣]+[길|로] [0-9\-0-9]+')
p2 = re.compile('서울특별시 [가-힣]+구 [가-힣0-9]+[동|가]')
dong=[]
driver = webdriver.Chrome('C:/Users/KimDH/Downloads/chromedriver_win32/chromedriver')
driver.get('http://www.juso.go.kr/support/AddressMainSearch.do?searchType=TOTAL')
for i,j in df.items():
    for k in range(1, len(j)+1):
        print(k)
        if p1.match(j[k]) != None:#도로명 주소이면
            try:#지번주소 긁어옴
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID,'searchButton')))
                driver.find_element_by_id('keyword').click()
                driver.find_element_by_id('keyword').send_keys(j[k])
                driver.find_element_by_id('searchButton').click()
                body=driver.find_element_by_css_selector('div.num.landLot')
            except:#지번주소가 없으면 그냥 넣는다# 얘는 else로 안감
                dong.append(j[k])
                driver.find_element_by_id('keyword').clear()
            else:#try문 마지막처리
                dong.append(p2.match(body.text).group())
                driver.find_element_by_id('keyword').clear()
        else:#도로명 주소가 아니면(지번주소면) 그냥 넣음
            dong.append(j[k])
            
            
s=pd.DataFrame(dong, columns=['주소'], index=range(1,628))#변환한거 저장
s.to_csv("리스트2.csv", mode='w', encoding='cp949')


df=pd.read_csv("리스트2.csv", engine='python', encoding='cp949', index_col=0)#불러와서 동별로 그룹화
s=df.groupby('주소').size().reset_index(name='횟수')
s.to_csv("성범죄 동별 통계.csv", mode='w', encoding='cp949')
