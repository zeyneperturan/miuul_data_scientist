###################################################
# Sorting Products
###################################################

###################################################
# Uygulama: Kurs Sıralama
###################################################
import pandas as pd
import math
import scipy.stats as st
from sklearn.preprocessing import MinMaxScaler # standartlaştırma

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

df = pd.read_csv("datasets/product_sorting.csv")
print(df.shape)
df.head(10)

####################
# Sorting by Rating
####################

# kursları puana göre azalan sıralayalım
df.sort_values("rating", ascending=False).head(20)
# puana göre sıralama yapınca satın ve alma yorum etkileri ezilmiş gibi duruyor, ratinge göre sıralama yemedi

####################
# Sorting by Comment Count or Purchase Count
####################
# sıralamayı satın alma ve yoruma göre de bi sıralayım

df.sort_values("purchase_count", ascending=False).head(20)
# satın almaya göre sıraladık ama kullanıcının memnunn olduğu kursları tepede görmek isteyebiliriz, bi tek bu da etkili olmadı sonuçta ücretsiz olan kurslarda satın alınmış olabilir, sadece satın alma yemedi

df.sort_values("commment_count", ascending=False).head(20)
# yorum sayısına göre sıralama tamam sosyal ikna oldu ama yine yoruma göre sıraladığımızda yine sıralama doğru olmadı


####################
# Sorting by Rating, Comment and Purchase
####################
# puan, yorum ve satın almayı bi arada sıralayım

# satın alma
df["purchase_count_scaled"] = MinMaxScaler(feature_range=(1, 5)). \
    fit(df[["purchase_count"]]). \
    transform(df[["purchase_count"]])
# yeni oluşturduğumuz değişken = değişken 1-5 arasında fit edelim (dönüştür) eski satın almayı yeni satın almaya dönüştür transform
# transform: araya girmek istersek dönüp, dönüştürme için kullanma, varolanın yerine yazdı ama geriye dönülebilir

df.describe().T # dağılımlarını bi görelim

# yorum için de aynı işi yapalım
df["comment_count_scaled"] = MinMaxScaler(feature_range=(1, 5)). \
    fit(df[["commment_count"]]). \
    transform(df[["commment_count"]])

df.head()

# satın alma, yorumun ve puanın önem ağırlığının farklılığına bi bakalım
(df["comment_count_scaled"] * 32 / 100 +
 df["purchase_count_scaled"] * 26 / 100 +
 df["rating"] * 42 / 100) # sonuç skordur (puan değil) bir çok faktörlü skor

# rating önemli olduğundan 42, satın alma önemli ama yorum daha önemlidir diye düünüp ters bi ağırlık verdik

# bu işi fonksiyonlaştıralım
def weighted_sorting_score(dataframe, w1=32, w2=26, w3=42):
    return (dataframe["comment_count_scaled"] * w1 / 100 +
            dataframe["purchase_count_scaled"] * w2 / 100 +
            dataframe["rating"] * w3 / 100)


df["weighted_sorting_score"] = weighted_sorting_score(df)

df.sort_values("weighted_sorting_score", ascending=False).head(20)

# ilgisizleri çıkaralım, kurs adı veri bilimi olanları
df[df["course_name"].str.contains("Veri Bilimi")].sort_values("weighted_sorting_score", ascending=False).head(20)

# soyuutları somutlaştırdık ölçeklendirdik skorlaştırdık ve daha hassas bi sıralama işlemi gerçekleştirmiş olduk.
# birdan fazla faktör olduğunda önce hepsini aynı standarta getirip gerekirse ağırlaştırıp sıralıyoruz.

####################
# Bayesian Average Rating Score - puan dağımları üzerinden ağırlıklı şekilde olasılıksal bi ortalam
####################
# sıralama işiyle ilgilenmeye devam (puanı skorlaştırıp skor olarak değerlendirmeye devam)

# Sorting Products with 5 Star Rated
# Sorting Products According to Distribution of 5 Star Rating


# ortalama hesabı yapıyoruz evet, puan dağılımları elimizde zaten var bu önsel hesaplama işine odaklanarak tekrar rating hesabı

# n: girilecek olan yıldızların gözlemleme frekansı (1. elamda kaç yıldız var?)
def bayesian_average_rating(n, confidence=0.95):
    if sum(n) == 0:
        return 0
    K = len(n)
    z = st.norm.ppf(1 - (1 - confidence) / 2)
    N = sum(n)
    first_part = 0.0
    second_part = 0.0
    for k, n_k in enumerate(n):
        first_part += (k + 1) * (n[k] + 1) / (N + K)
        second_part += (k + 1) * (k + 1) * (n[k] + 1) / (N + K)
    score = first_part - z * math.sqrt((second_part - first_part * first_part) / (N + K + 1))
    return score


df.head()

df["bar_score"] = df.apply(lambda x: bayesian_average_rating(x[["1_point",
                                                                "2_point",
                                                                "3_point",
                                                                "4_point",
                                                                "5_point"]]), axis=1)

df.sort_values("weighted_sorting_score", ascending=False).head(20)
df.sort_values("bar_score", ascending=False).head(20) # sadece ratinglere odaklanarak bi sıralama yaptı, fakat yorum sayıları satın almlara gözden kaçtı / tek amaç verilen puan sıralaması ise bar_score kullanılabilir

# isin 1 ve 5 indexine sahip olanlar
df[df["course_name"].index.isin([5, 1])].sort_values("bar_score", ascending=False) # kurs1 daha yukarda çıktı çünkü daha düşük puan frekansın düşük olması bunu yukarı çıkardı. puan dağılımlarına baktı ama çok mantıklı bi sonuç yine olmadı


####################
# Hybrid Sorting: BAR Score + Diğer Faktorler
####################

# Rating Products -BURASI OK
# - Average
# - Time-Based Weighted Average
# - User-Based Weighted Average
# - Weighted Rating
# - Bayesian Average Rating Score: puanları kırpar olasılıksal bi ortalamadır

# Sorting Products
# - Sorting by Rating
# - Sorting by Comment Count or Purchase Count
# - Sorting by Rating, Comment and Purchase
# - Sorting by Bayesian Average Rating Score (Sorting Products with 5 Star Rated)
# - Hybrid Sorting: BAR Score + Diğer Faktorler

# sadece yorum - puan - satın alma tek başına yemiyor, bunların hepsi ile ağırlıklı bi ortalama skor hesabı yapalım dedik, şimdi ise daha önce belirlediğimiz ağırlıklar ile olasılıksal olarak hesapladığımız bar_score'u bi araya getiricez

# bar score (baes yöntemi) ve wss(kendi hesapladığımız)
def hybrid_sorting_score(dataframe, bar_w=60, wss_w=40):
    bar_score = dataframe.apply(lambda x: bayesian_average_rating(x[["1_point",
                                                                     "2_point",
                                                                     "3_point",
                                                                     "4_point",
                                                                     "5_point"]]), axis=1)
    wss_score = weighted_sorting_score(dataframe)

    return bar_score*bar_w / 100 + wss_score*wss_w / 100


df["hybrid_sorting_score"] = hybrid_sorting_score(df)

df.sort_values("hybrid_sorting_score", ascending=False).head(20)

df[df["course_name"].str.contains("Veri Bilimi")].sort_values("hybrid_sorting_score", ascending=False).head(20)


############################################
# Uygulama: IMDB Movie Scoring & Sorting
############################################

import pandas as pd
import math
import scipy.stats as st
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

df = pd.read_csv("datasets/movies_metadata.csv",
                 low_memory=False)  # DtypeWarning kapamak icin

df = df[["title", "vote_average", "vote_count"]] # isim - ortalama puan - puan sayısı

df.head()
df.shape

########################
# Vote Average'a Göre Sıralama - ortalama puana göre sıralama
########################

# ilk 250yi sıralama yapalım bakalım

df.sort_values("vote_average", ascending=False).head(20) # ortalama pauna göre sıraladık, mantıklı değil devaaam

df["vote_count"].describe([0.10, 0.25, 0.50, 0.70, 0.80, 0.90, 0.95, 0.99]).T # puan sayılarını segmentlere ayıralım, ortalama 100

df[df["vote_count"] > 400].sort_values("vote_average", ascending=False).head(20) # puan sayılarını 400'den büyük olanları sıralayalım / 400 tercihtir  // yorum sayısı da tek başına yeterli değil, devam

#from sklearn.preprocessing import MinMaxScaler

# yorum sayısı ve puanı standartlaştıralım
df["vote_count_score"] = MinMaxScaler(feature_range=(1, 10)). \
    fit(df[["vote_count"]]). \
    transform(df[["vote_count"]])

########################
# vote_average * vote_count
########################

df["average_count_score"] = df["vote_average"] * df["vote_count_score"]

df.sort_values("average_count_score", ascending=False).head(20)

########################
# IMDB Weighted Rating
########################


# weighted_rating = (v/(v+M) * r) + (M/(v+M) * C)

# r = vote average
# v = vote count
# M = minimum votes required to be listed in the Top 250
# C = the mean vote across the whole report (currently 7.0)

# Film 1:
# r = 8
# M = 500
# v = 1000

# (1000 / (1000+500))*8 = 5.33 -- filmin oy sayısı / filmin oy sayııs + gerekli oy sayııs


# Film 2:
# r = 8
# M = 500
# v = 3000

# (3000 / (3000+500))*8 = 6.85   puanlar aynı ama daha yüksek sayıda oy aldıysa daha iyidir mük

# (1000 / (1000+500))*9.5 = 6.33  puanı 9,5 ama oy sayısı düşük

# Film 1:
# r = 8
# M = 500
# v = 1000

# Birinci bölüm:
# (1000 / (1000+500))*8 = 5.33

# İkinci bölüm:
# 500/(1000+500) * 7 = 2.33

# Toplam = 5.33 + 2.33 = 7.66


# Film 2:
# r = 8
# M = 500
# v = 3000

# Birinci bölüm:
# (3000 / (3000+500))*8 = 6.85

# İkinci bölüm:
# 500/(3000+500) * 7 = 1

# Toplam = 7.85

# çıkarılan sonuç : işyeri problemde kendine has ağırlıklı hesaplama yöntemi bulabilir, genel resimden sıralama peşindeyiz biz
# bütün kitlenin ortalaması ve min gerekli ortalama sayısı her filmin kendi içinde ki oy sayısına göre işleme tabii tutuldu

M = 2500 # gerekli oy sayısı
C = df['vote_average'].mean()

def weighted_rating(r, v, M, C):
    return (v / (v + M) * r) + (M / (v + M) * C)

df.sort_values("average_count_score", ascending=False).head(10) # her film için bu hesabı yapalım

weighted_rating(7.40000, 11444.00000, M, C) # filmin avagere, vote_count, M, C - deadpool filmi 7.080544896574546

weighted_rating(8.10000, 14075.00000, M, C) # Inception - 7.725672279809078

weighted_rating(8.50000, 8358.00000, M, C)

df["weighted_rating"] = weighted_rating(df["vote_average"],
                                        df["vote_count"], M, C)

df.sort_values("weighted_rating", ascending=False).head(10) # daha güven verdi

####################
# Bayesian Average Rating Score
####################

# 12481                                    The Dark Knight
# 314                             The Shawshank Redemption
# 2843                                          Fight Club
# 15480                                          Inception
# 292                                         Pulp Fiction


def bayesian_average_rating(n, confidence=0.95):
    if sum(n) == 0:
        return 0
    K = len(n)
    z = st.norm.ppf(1 - (1 - confidence) / 2)
    N = sum(n)
    first_part = 0.0
    second_part = 0.0
    for k, n_k in enumerate(n):
        first_part += (k + 1) * (n[k] + 1) / (N + K)
        second_part += (k + 1) * (k + 1) * (n[k] + 1) / (N + K)
    score = first_part - z * math.sqrt((second_part - first_part * first_part) / (N + K + 1))
    return score

bayesian_average_rating([34733, 4355, 4704, 6561, 13515, 26183, 87368, 273082, 600260, 1295351]) # esaretin bedeli filmi puan dağılımları

bayesian_average_rating([37128, 5879, 6268, 8419, 16603, 30016, 78538, 199430, 402518, 837905]) # baba kaç tane 2 yıldız, 2 yıldız, 3 yıldız..... 10 yıldız

df = pd.read_csv("datasets/imdb_ratings.csv") # vode_count dağılımları, oy dağılımları (yukarda elle yazdığımız paun dağılım)
df = df.iloc[0:, 1:]


df["bar_score"] = df.apply(lambda x: bayesian_average_rating(x[["one", "two", "three", "four", "five",
                                                                "six", "seven", "eight", "nine", "ten"]]), axis=1)
df.sort_values("bar_score", ascending=False).head(20)

# imbd ile aynı sonuçları gördük siteden de

# e ticarette en büyük sorun sıralama sorunudur, ağırlık skor standartlaşma; olasılıksal istatiksel kullarak sıralamaya çalıştık. imbd ile aynı sonucu bulduk

# 250 listesinden ziyade, son 5 senenin 250 listesi diye bakmak daha mantıklı olurdu yani zamana göre trend yakalama çabası lazım

# tavsiye sistemi uyguladık


# Ağırlıklı Ortalama Notlar
# IMDb ham veri ortalamaları yerine ağırlıklı oy ortalamaları yayınlar.
# Bunu açıklamanın en basit yolu, kullanıcılar tarafından alınan tüm oyları kabul etmemize ve dikkate almamıza rağmen,
# tüm oylar nihai derecelendirme üzerinde aynı etkiye (veya 'ağırlığa') sahip değildir.

# Olağandışı oylama faaliyeti tespit edildiğinde,
# Sistemimizin güvenilirliğini korumak için alternatif bir ağırlıklandırma hesaplaması uygulanabilir.
# Derecelendirme mekanizmamızın etkin kalmasını sağlamak için,
# derecelendirmeyi oluşturmak için kullanılan yöntemi tam olarak açıklamıyoruz.
# IMDb derecelendirmeleri için SSS'nin tamamına da bakın.


# Weighted Average Ratings
# IMDb publishes weighted vote averages rather than raw data averages.
# The simplest way to explain it is that although we accept and consider all votes received by users,
# not all votes have the same impact (or ‘weight’) on the final rating.

# When unusual voting activity is detected,
# an alternate weighting calculation may be applied in order to preserve the reliability of our system.
# To ensure that our rating mechanism remains effective,
# we do not disclose the exact method used to generate the rating.
# See also the complete FAQ for IMDb ratings.

