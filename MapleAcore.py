# # 메이플 A 코어 기간별 가격변화 
# 
# ## 데이터 수집 과정
# * 데이터를 수집하기 위해서 프로젝트를 시작한 날 부터 특정 시간대(11시, 23시)에 경매장의 판매내역을 저장하였다. 판매내역을 볼 수 있는 것이 최대 100개이기 때문에 하루에 200개의 데이터를 수집하였다.
# 
# ## 데이터 가공

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime 
from matplotlib.dates import MonthLocator, DateFormatter

mp_a = pd.read_excel("C:/Users/Kimkangmin/Desktop/메이플/A코어.xlsx") 
# 데이터를 변수에 저장

mp_a.info() 
# 데이터 정보 확인

mp_a[mp_a['개수'] > 300] 
# 최대 300개가 팔릴 수 있으므로 초과되는 값들을 확인

mp_a.dropna(axis = 'rows') 
#결측치 제거

mp_a_m = np.mean(mp_a['가격'])
mp_a_m
# A코어 가격의 평균

over_a_pr_U = mp_a[mp_a['가격'] > mp_a_m*3] 
# 데이터 입력 과정에서 숫자 입력누락으로 인한 데이터 수정을 위해 경매장에서 비정상적으로 높은 가격으로 팔린 데이터를 찾음
over_a_pr_U

over_a_pr_l = mp_a[mp_a['가격'] < mp_a_m/3] 
# 데이터 입력 과정에서 숫자 입력누락으로 인한 데이터 수정을 위해 경매장에서 비정상적으로 낮은 가격으로 팔린 데이터를 찾음
over_a_pr_l


# ## 데이터 분석

# ### 날짜별 가격 변화

plt.rc('font', family='Malgun Gothic')

plt.figure(figsize = (10, 3))
sns.lineplot(data = mp_a, x = '날짜', y = '가격', ci = None)


# * 가격이 비이상적으로 높고 낮은 행이 추가 될 경우 그래프가 비이상적으로 되고 값에 큰 영향을 주기 때문에 
# 데이터를 제거한다.

mp_a = mp_a[(mp_a['가격'] < mp_a_m*3) & (mp_a['가격'] > mp_a_m/3) & (mp_a['개수'] < 301)].copy()
plt.figure(figsize = (10, 3))
f_a = sns.lineplot(data = mp_a, x = '날짜', y = '가격',ci = None)
f_a.xaxis.set_major_locator(MonthLocator(interval = 1))

c_d = mp_a[(mp_a['날짜'] >= '2021-12-01') & (mp_a['날짜'] <= '2021-12-26')]
c_d.groupby('날짜')['가격'].mean().round()
#특정 날짜의 일별 평균 가격

# * 21.01.31 스타포스 강화 비용 30% 할인 이벤트가 시작 될 때에는 약 4% 정도 증가했지만, 이벤트가 끝나고, 가격이 약 11% 정도 감소했다.
# 
# 
# * 21.02.18 환생의 불꽃, 어빌리티 확률 조작 사건이 발발하고 4일만에 약 20% 정도 감소했다.
# 
# 
# * 21.02.24 환생의 불꽃, 어빌리티 확률 조작 사건 관련 보상안을 공지하고 보상안을 수령하는 그 다음날인 21.02.25에 약 19% 정도 증가했다. 그리고 꾸준히 증가해서 약 30% 정도까지 증가했다.

# ### 요일별 가격 변화
plt.figure(figsize = (20, 10))
box_plot = sns.boxplot(data = mp_a, x = '요일', y = '가격')
ax = box_plot.axes
lines = ax.get_lines()
categories = ax.get_xticks()

for cat in categories:
    # every 4th line at the interval of 6 is median line
    # 0 -> p25 1 -> p75 2 -> lower whisker 3 -> upper whisker 4 -> p50 5 -> upper extreme value
    y = round(lines[4+cat*6].get_ydata()[0],1) 

    ax.text(
        cat, 
        y, 
        f'{y}', 
        ha='center', 
        va='center', 
        fontweight='bold', 
        size=20,
        color='white',
        bbox=dict(facecolor='#445A64'))

box_plot.figure.tight_layout()

plt.figure(figsize = (18, 5))
sns.lineplot(data = mp_a, x = '요일', y = '가격') #평균값으로 그래프(파란색)
sns.lineplot(data = mp_a, x = '요일', y = '가격',estimator = np.median) #중앙값으로 그래프(주황색)


# * 그래프를 보게 되면 평균적으로 월요일이 가격이 가장 낮고, 토요일에 가장 높은 것으로 나타난다.
# 
# 
# * 평균적으로 목요일에 가격이 급등하게 된다.

# ### 개수별 가격 변화

plt.figure(figsize = (18, 5))
sns.lineplot(data = mp_a, x = '개수', y = '가격', ci = None)


# * 그래프를 그리게 되면 개수와 가격 간의 상관관계가 없어 보인다.

mp_a1 = mp_a.copy()

for i in mp_a1.index[:]:
    mp_a1.loc[i, '개수'] = mp_a1.loc[i, '개수']//10 *10
# A코의 개수를 10개 단위로 0부터 300까지 나눔

sns.lineplot(data = mp_a1, x = '개수', y = '가격', ci = None)


# * 10개 단위로 나누어 봐도 개수에 따른 가격이 상관관계가 없는 것으로 나타난다.(21.03.03)

def chd():
    global sd
    global ed
    sd = datetime.strptime(input('시작 날짜를 형식에 알맞게 넣어주세요 : 년/월/일 '), '%Y/%m/%d')
    ed = datetime.strptime(input('끝 날짜를 형식에 알맞게 넣어주세요 : 년/월/일 '), '%Y/%m/%d')

def check():
    while sd >= ed :
        print('시작 날짜는 끝 날짜보다 작아야하고 하루 이상 차이나야 합니다.')
        chd()

    while sd > max(mp_a['날짜']) :
        print('시작 날짜 이후의 데이터가 존재하지 않습니다.')
        chd()
    while ed < min(mp_a['날짜']) :
        print('끝 날짜 이전의 데이터가 존재하지 않습니다.')    
        chd()

chd()

check()

mp_a_chd = mp_a[(mp_a['날짜'] >= sd) & (mp_a['날짜'] <= ed)]
plt.figure(figsize = (10, 3))
sns.lineplot(data = mp_a_chd, x = '날짜', y = '가격',ci = None)

day_o = ["월", "화", "수", "목", "금", "토", "일"]
sns.boxplot(data = mp_a_chd, x = '요일', y = '가격', order = day_o)
