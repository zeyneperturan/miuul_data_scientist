###################################################
# Rating Products
###################################################
# olası faktörleri göz önünde bulundurarark ağırlıklı puan hesaplama


# - Average
# - Time-Based Weighted Average
# - User-Based Weighted Average
# - Weighted Rating


############################################
# Uygulama: Kullanıcı ve Zaman Ağırlıklı Kurs Puanı Hesaplama
############################################

import pandas as pd
import math
import scipy.stats as st
from sklearn.preprocessing import MinMaxScaler

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 500)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

# (50+ Saat) Python A-Z™: Veri Bilimi ve Machine Learning
# Puan: 4.8 (4.764925)
# Toplam Puan: 4611
# Puan Yüzdeleri: 75, 20, 4, 1, <1
# Yaklaşık Sayısal Karşılıkları: 3458, 922, 184, 46, 6

df = pd.read_csv("datasets/course_reviews.csv")
df.head()
df.shape # (4323, 6)

# rating dagılımı
df["Rating"].value_counts() # puanların dağılımı

df["Questions Asked"].value_counts() # sorulan soruların dağılımı

df.groupby("Questions Asked").agg({"Questions Asked": "count",
                                   "Rating": "mean"}) # sorulan soru kırılımında verilen puanlar

df.head()

# kursa verilen puanı hesaplama amacındaydık

####################
# Average
####################

# Ortalama Puan
df["Rating"].mean() # bu hesapla, memnuniyeti kaçırıyor olabiliriz, son 3 ay ilk 3 ay puan farkları olabilir bu yüzden zamansal bakalım - güncel trendi ortalmaya yansıtmak lazım yani

####################
# Time-Based Weighted Average - Puan Zamanlarına Göre Ağırlıklı Ortalama
####################
# Puan Zamanlarına Göre Ağırlıklı Ortalama

df.head()
df.info()

df["Timestamp"] = pd.to_datetime(df["Timestamp"]) # fonk. ile tipini zamana çevirelim

# yapılan yorumları gün cinsinden ifade etmeliyiz, bugünü bi tarih olarak verdik
current_date = pd.to_datetime('2021-02-10 0:0:0')

# bugünün tarihi - yorum tarihi ( 4 ise 4 gün önce yorum yapıldı gibi)
df["days"] = (current_date - df["Timestamp"]).dt.days # gün cinsinden

# son 30 günde ki yorumlara erişelim
df.loc[df["days"] <= 30, "Rating"].mean()  # 4.775773195876289

# en az 31 ve 90dan küçük
df.loc[(df["days"] > 30) & (df["days"] <= 90), "Rating"].mean() #  4.763833992094861

# en az 91 ve en fazla 180
df.loc[(df["days"] > 90) & (df["days"] <= 180), "Rating"].mean() # 4.752503576537912

# 180'den büyük olan
df.loc[(df["days"] > 180), "Rating"].mean() # 4.76641586867305

# ağırlıklarına göre hesaplama yapalım. (ağırlık toplamları 100), ağırlık sayısı arrtıkça hareket edebileceğimiz range azalır
df.loc[df["days"] <= 30, "Rating"].mean() * 28/100 + \
    df.loc[(df["days"] > 30) & (df["days"] <= 90), "Rating"].mean() * 26/100 + \
    df.loc[(df["days"] > 90) & (df["days"] <= 180), "Rating"].mean() * 24/100 + \
    df.loc[(df["days"] > 180), "Rating"].mean() * 22/100 # 4.765025682267194

# güncel olan yorumlara daha fazla ağırlık verdik, 28 - 26 - 24 - 22

# biz bu işi fonksiyonlaştıralım w1 + w2 + w3 + w4 = 100
def time_based_weighted_average(dataframe, w1=28, w2=26, w3=24, w4=22):
    return dataframe.loc[df["days"] <= 30, "Rating"].mean() * w1 / 100 + \
           dataframe.loc[(dataframe["days"] > 30) & (dataframe["days"] <= 90), "Rating"].mean() * w2 / 100 + \
           dataframe.loc[(dataframe["days"] > 90) & (dataframe["days"] <= 180), "Rating"].mean() * w3 / 100 + \
           dataframe.loc[(dataframe["days"] > 180), "Rating"].mean() * w4 / 100

time_based_weighted_average(df)

time_based_weighted_average(df, 30, 26, 22, 22)


####################
# User-Based Weighted Average - Kullanıcı Temellli Ağırlıklı Ortalama
####################

# herkesin verdiği puanın ağırlığı aynı mı olmalı? kursun tamamını izleyen ile %60'ını izleyenin puanı aynı değerde midir?

df.head()

df.groupby("Progress").agg({"Rating": "mean"}) # kursu izleme programlarına göre puanların ortalamasına bi bakalım

# kursu tamamlama 10'dan küçükse ağırlığı 22, 10dan büyük 45ten küçükse ağırlık 24...
df.loc[df["Progress"] <= 10, "Rating"].mean() * 22 / 100 + \
    df.loc[(df["Progress"] > 10) & (df["Progress"] <= 45), "Rating"].mean() * 24 / 100 + \
    df.loc[(df["Progress"] > 45) & (df["Progress"] <= 75), "Rating"].mean() * 26 / 100 + \
    df.loc[(df["Progress"] > 75), "Rating"].mean() * 28 / 100 # 4.800257704672543

# yani aslında kursu en fazla tamamlayanların ağırlıkları daha yüksektir.

def user_based_weighted_average(dataframe, w1=22, w2=24, w3=26, w4=28):
    return dataframe.loc[dataframe["Progress"] <= 10, "Rating"].mean() * w1 / 100 + \
           dataframe.loc[(dataframe["Progress"] > 10) & (dataframe["Progress"] <= 45), "Rating"].mean() * w2 / 100 + \
           dataframe.loc[(dataframe["Progress"] > 45) & (dataframe["Progress"] <= 75), "Rating"].mean() * w3 / 100 + \
           dataframe.loc[(dataframe["Progress"] > 75), "Rating"].mean() * w4 / 100


user_based_weighted_average(df, 20, 24, 26, 30) # 4.803286469062915

# amaç başarı değil, ortalama almayı hassaslaştırdığımızda sonuçların değişkenlik göstermiş olmasını inceliyoruz

####################
# Weighted Rating - Ağırlıklı Değerlendirme
####################

# zaman ve kişi ağırlıklı odaklı bi ortalama alıp daha verimli bi ortalama

# time_w = timedan gelecek ağırlık - time_based_weighted_average fonk
# user_w = kullanıcı ağırlığı - user_based_weighted_average fonk

def course_weighted_rating(dataframe, time_w = 50, user_w = 50): # ön tanım verdik
    return time_based_weighted_average(dataframe) * time_w / 100 + user_based_weighted_average(dataframe) * user_w / 100

course_weighted_rating(df) # 4.782641693469868 time ve user toplamları


# ağırlıkları değiştirelim, time ve user önemine göre
course_weighted_rating(df, time_w=40, user_w=60) # 4.786164895710403












