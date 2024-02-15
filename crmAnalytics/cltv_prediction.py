##############################################################
# BG-NBD ve Gamma-Gamma ile CLTV Prediction
##############################################################

# 1. Verinin Hazırlanması (Data Preperation)
# 2. BG-NBD Modeli ile Expected Number of Transaction
# 3. Gamma-Gamma Modeli ile Expected Average Profit
# 4. BG-NBD ve Gamma-Gamma Modeli ile CLTV'nin Hesaplanması
# 5. CLTV'ye Göre Segmentlerin Oluşturulması
# 6. Çalışmanın fonksiyonlaştırılması


##############################################################
# 1. Verinin Hazırlanması (Data Preperation)
##############################################################

# Bir e-ticaret şirketi müşterilerini segmentlere ayırıp bu segmentlere göre
# pazarlama stratejileri belirlemek istiyor.

# Veri Seti Hikayesi

# https://archive.ics.uci.edu/ml/datasets/Online+Retail+II

# Online Retail II isimli veri seti İngiltere merkezli online bir satış mağazasının
# 01/12/2009 - 09/12/2011 tarihleri arasındaki satışlarını içeriyor.

# Değişkenler

# InvoiceNo: Fatura numarası. Her işleme yani faturaya ait eşsiz numara. C ile başlıyorsa iptal edilen işlem.
# StockCode: Ürün kodu. Her bir ürün için eşsiz numara.
# Description: Ürün ismi
# Quantity: Ürün adedi. Faturalardaki ürünlerden kaçar tane satıldığını ifade etmektedir.
# InvoiceDate: Fatura tarihi ve zamanı.
# UnitPrice: Ürün fiyatı (Sterlin cinsinden)
# CustomerID: Eşsiz müşteri numarası
# Country: Ülke ismi. Müşterinin yaşadığı ülke.


##########################
# Gerekli Kütüphane ve Fonksiyonlar
##########################

# !pip install lifetimes - terminalden yükledik
import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
from lifetimes import BetaGeoFitter
from lifetimes import GammaGammaFitter
from lifetimes.plotting import plot_period_transactions

pd.set_option('display.max_columns', None) # bütün sütunlar
pd.set_option('display.width', 500) # yan yana 500
pd.set_option('display.float_format', lambda x: '%.4f' % x) # vigülden sonra 4 basamak göster
from sklearn.preprocessing import MinMaxScaler # 0-1 yada 0-100 değerlerine çekme

# kendisine girilen değer için eşik değer belirleme,
# çeyrek değerler belirleniyor önce farkı hesapla
# 3. çeyreğin 1.5 üstü ve 1. çeyreğin 1.5 altı eşik değerleri belirlendi

def outlier_thresholds(dataframe, variable):
    quartile1 = dataframe[variable].quantile(0.01) # normalde %25 - kişisel tercih 0.01 eşik aralığı genişliği için
    quartile3 = dataframe[variable].quantile(0.99) # normalde %75 - kişisel tercih 0.99
    interquantile_range = quartile3 - quartile1
    up_limit = quartile3 + 1.5 * interquantile_range
    low_limit = quartile1 - 1.5 * interquantile_range
    return low_limit, up_limit

# aykırı değer baskılama (silme değil, baskılama)
# aykırı değer 360 olsun threshold 300 ise 360 yerine 300 yazıyor
def replace_with_thresholds(dataframe, variable):
    low_limit, up_limit = outlier_thresholds(dataframe, variable)
    # dataframe.loc[(dataframe[variable] < low_limit), variable] = low_limit
    dataframe.loc[(dataframe[variable] > up_limit), variable] = up_limit


#########################
# Verinin Okunması
#########################

df_ = pd.read_excel("datasets/online_retail_II.xlsx",
                    sheet_name="Year 2010-2011")
df = df_.copy()
df.describe().T # sayısal değişkenleri getirdik
df.head()
df.isnull().sum() # eksik değerleri gör

#########################
# Veri Ön İşleme
#########################

df.dropna(inplace=True) # eksik değerleri sil
df = df[~df["Invoice"].str.contains("C", na=False)] #invoice içinde C (iade) olmayanları al
df = df[df["Quantity"] > 0] # miktar 0'dan büyükleri al
df = df[df["Price"] > 0] # fiyatı 0'dan büyük olanları al

# aykırı değerlerini eşik değerleriyle değiştir
replace_with_thresholds(df, "Quantity")
replace_with_thresholds(df, "Price")

df["TotalPrice"] = df["Quantity"] * df["Price"]

today_date = dt.datetime(2011, 12, 11) # analizdeki en büyük tarihin üstüne 1-2 gün koyarak çalışalım

#########################
# Lifetime Veri Yapısının Hazırlanması
#########################

# recency: Son satın alma üzerinden geçen zaman. Haftalık. (kullanıcı özelinde) // müşterinin kendi içindeki son satın alma - ilk satın alma durumu
# T: Müşterinin yaşı. Haftalık. (analiz tarihinden ne kadar süre önce ilk satın alma yapılmış) // analiz günü - ilk satın alma = müşteri yaşı haftalık çevir
# frequency: tekrar eden toplam satın alma sayısı (frequency>1) // müşteri en az 2. kez alışveriş yapmış = bizim müşteri
# monetary: satın alma başına ortalama kazanç // burası için ortalaması alınacak


cltv_df = df.groupby('Customer ID').agg(
    {'InvoiceDate': [lambda InvoiceDate: (InvoiceDate.max() - InvoiceDate.min()).days,
                     lambda InvoiceDate: (today_date - InvoiceDate.min()).days], # bugünün tarihi - min (ilk) tarih
     'Invoice': lambda Invoice: Invoice.nunique(),
     'TotalPrice': lambda TotalPrice: TotalPrice.sum()})

cltv_df.columns = cltv_df.columns.droplevel(0)

cltv_df.columns = ['recency', 'T', 'frequency', 'monetary']

cltv_df["monetary"] = cltv_df["monetary"] / cltv_df["frequency"] # işlem başına ortalama kazanç

cltv_df.describe().T

cltv_df = cltv_df[(cltv_df['frequency'] > 1)]

cltv_df["recency"] = cltv_df["recency"] / 7 # /7 ile haftalık

cltv_df["T"] = cltv_df["T"] / 7 # /7 ile haftalık

cltv_df.describe().T
# recency : müşterilen kendi içinde kaç haftadır alışveriş yapmadığı
# T : müşteri kaç haftadır müşterimiz, yaşı yani
# frequency : satın alma sıklığı
# monetary : sipariş başına bırakılan ortalama gelir

##############################################################
# 2. BG-NBD Modelinin Kurulması : beta ve gamma dağılımlarını parametlerini bulmakta ve tahmin için iligli modeli bulma
##############################################################

bgf = BetaGeoFitter(penalizer_coef=0.001) # model nesnesi oluşturucam, frequency recency ve T yi ver // penalizer_coef=0.001 ceza kat sayısı

bgf.fit(cltv_df['frequency'],
        cltv_df['recency'],
        cltv_df['T']) # fit ile her müşteri için f, r


# fitted with 2845 subjects, a: 0.12, alpha: 11.41, b: 2.49, r: 2.18

################################################################
# 1 hafta içinde en çok satın alma beklediğimiz 10 müşteri kimdir? -- KIYMETLİ
################################################################

# conditional_expected_number_of_purchases_up_to_time: belirli bi zaman periyodu, haftalık cinsten = 1

bgf.conditional_expected_number_of_purchases_up_to_time(1,
                                                        cltv_df['frequency'],
                                                        cltv_df['recency'],
                                                        cltv_df['T']).sort_values(ascending=False).head(10) # tüm tahmin sonucu azanalan şekilde ver

# conditional_expected_number_of_purchases_up_to_time = predict BG-NBD için geçerli ama gamma gamma için değil

bgf.predict(1,
            cltv_df['frequency'],
            cltv_df['recency'],
            cltv_df['T']).sort_values(ascending=False).head(10)

cltv_df["expected_purc_1_week"] = bgf.predict(1,
                                              cltv_df['frequency'],
                                              cltv_df['recency'],
                                              cltv_df['T']) # tüm müşter için 1 haftalık duruma bakıp cltv_df at

################################################################
# 1 ay içinde en çok satın alma beklediğimiz 10 müşteri kimdir? // 1 ay = 4 hafta
################################################################

bgf.predict(4,
            cltv_df['frequency'],
            cltv_df['recency'],
            cltv_df['T']).sort_values(ascending=False).head(10)

cltv_df["expected_purc_1_month"] = bgf.predict(4,
                                               cltv_df['frequency'],
                                               cltv_df['recency'],
                                               cltv_df['T']) # tüm müşteriler için yapalım


# bir aylık periyotta şirketin beklediği satış sayısı 1776.8934732202938
bgf.predict(4,
            cltv_df['frequency'],
            cltv_df['recency'],
            cltv_df['T']).sum()

################################################################
# 3 Ayda Tüm Şirketin Beklenen Satış Sayısı Nedir? = 4 * 3
################################################################

bgf.predict(4 * 3,
            cltv_df['frequency'],
            cltv_df['recency'],
            cltv_df['T']).sum() # 3 ayda şirketin beklediği satış 5271.1124338263635

cltv_df["expected_purc_3_month"] = bgf.predict(4 * 3,
                                               cltv_df['frequency'],
                                               cltv_df['recency'],
                                               cltv_df['T'])
################################################################
# Tahmin Sonuçlarının Değerlendirilmesi
################################################################
# gerçekler :  mavi ,tahminler : turuncu

plot_period_transactions(bgf)
plt.show()

##############################################################
# 3. GAMMA-GAMMA Modelinin Kurulması
##############################################################

ggf = GammaGammaFitter(penalizer_coef=0.01) # model  nesnesini çağır

ggf.fit(cltv_df['frequency'], cltv_df['monetary']) # model nesnesini kullanarak model kur ggf.fit
# <lifetimes.GammaGammaFitter: fitted with 2845 subjects, p: 3.79, q: 0.34, v: 3.73>

ggf.conditional_expected_average_profit(cltv_df['frequency'],
                                        cltv_df['monetary']).head(10) # toplam işlem sayısı ve ortalama değeri yolladık

ggf.conditional_expected_average_profit(cltv_df['frequency'],
                                        cltv_df['monetary']).sort_values(ascending=False).head(10) # azalan şekilde sırala, beklenen karı getirdik müşteriler için

cltv_df["expected_average_profit"] = ggf.conditional_expected_average_profit(cltv_df['frequency'],
                                                                             cltv_df['monetary'])

cltv_df.sort_values("expected_average_profit", ascending=False).head(10) # 1 hafta 1 ay... beklenren satoş değerleri

##############################################################
# 4. BG-NBD ve GG modeli ile CLTV'nin hesaplanması. - asıl amaç
##############################################################

cltv = ggf.customer_lifetime_value(bgf,
                                   cltv_df['frequency'],
                                   cltv_df['recency'],
                                   cltv_df['T'],
                                   cltv_df['monetary'],
                                   time=3,  # 3 aylık !!! - haftalık olması lazım???????
                                   freq="W",  # T'nin frekans bilgisi. - haftalık
                                   discount_rate=0.01)

cltv.head() # müşteri ve cltv değerlerini getirdi

cltv = cltv.reset_index() # customer ID'yi indexten kurtaralım

cltv_final = cltv_df.merge(cltv, on="Customer ID", how="left") # cltv_df ile cltv'yi customer ID'ye göre merge
cltv_final.sort_values(by="clv", ascending=False).head(10) #

# bgnbd !! senin için düzenli olan bi müşteri kendi içinde ki recency değeri arttıkça müşterinin satın alması yaklaşıyor, her an alışveriş yapabilir, müşternin terkar satın alma ihtiyacı doğar, yaş ve recency yakınsa her an alışveriş yapabilir??

# sadece yaşa frekansa ya da monetary'e göre yorum yapmak doğru olmaz ama bu model her şeyi veriyor

##############################################################
# 5. CLTV'ye Göre Segmentlerin Oluşturulması
##############################################################

cltv_final

cltv_final["segment"] = pd.qcut(cltv_final["clv"], 4, labels=["D", "C", "B", "A"])

cltv_final.sort_values(by="clv", ascending=False).head(50)

cltv_final.groupby("segment").agg(
    {"count", "mean", "sum"})


##############################################################
# 6. Çalışmanın Fonksiyonlaştırılması
##############################################################

def create_cltv_p(dataframe, month=3): # tahmin periyodunu özellik olarak girdik, 1 - 3 - 6 aylık //
    # 1. Veri Ön İşleme
    dataframe.dropna(inplace=True)
    dataframe = dataframe[~dataframe["Invoice"].str.contains("C", na=False)]
    dataframe = dataframe[dataframe["Quantity"] > 0]
    dataframe = dataframe[dataframe["Price"] > 0]
    replace_with_thresholds(dataframe, "Quantity")
    replace_with_thresholds(dataframe, "Price")
    dataframe["TotalPrice"] = dataframe["Quantity"] * dataframe["Price"]
    today_date = dt.datetime(2011, 12, 11)

    cltv_df = dataframe.groupby('Customer ID').agg(
        {'InvoiceDate': [lambda InvoiceDate: (InvoiceDate.max() - InvoiceDate.min()).days,
                         lambda InvoiceDate: (today_date - InvoiceDate.min()).days],
         'Invoice': lambda Invoice: Invoice.nunique(),
         'TotalPrice': lambda TotalPrice: TotalPrice.sum()})

    cltv_df.columns = cltv_df.columns.droplevel(0)
    cltv_df.columns = ['recency', 'T', 'frequency', 'monetary']
    cltv_df["monetary"] = cltv_df["monetary"] / cltv_df["frequency"]
    cltv_df = cltv_df[(cltv_df['frequency'] > 1)]
    cltv_df["recency"] = cltv_df["recency"] / 7
    cltv_df["T"] = cltv_df["T"] / 7

    # 2. BG-NBD Modelinin Kurulması
    bgf = BetaGeoFitter(penalizer_coef=0.001)
    bgf.fit(cltv_df['frequency'],
            cltv_df['recency'],
            cltv_df['T'])

    cltv_df["expected_purc_1_week"] = bgf.predict(1,
                                                  cltv_df['frequency'],
                                                  cltv_df['recency'],
                                                  cltv_df['T'])

    cltv_df["expected_purc_1_month"] = bgf.predict(4,
                                                   cltv_df['frequency'],
                                                   cltv_df['recency'],
                                                   cltv_df['T'])

    cltv_df["expected_purc_3_month"] = bgf.predict(12,
                                                   cltv_df['frequency'],
                                                   cltv_df['recency'],
                                                   cltv_df['T'])

    # 3. GAMMA-GAMMA Modelinin Kurulması
    ggf = GammaGammaFitter(penalizer_coef=0.01)
    ggf.fit(cltv_df['frequency'], cltv_df['monetary'])
    cltv_df["expected_average_profit"] = ggf.conditional_expected_average_profit(cltv_df['frequency'],
                                                                                 cltv_df['monetary'])

    # 4. BG-NBD ve GG modeli ile CLTV'nin hesaplanması.
    cltv = ggf.customer_lifetime_value(bgf,
                                       cltv_df['frequency'],
                                       cltv_df['recency'],
                                       cltv_df['T'],
                                       cltv_df['monetary'],
                                       time=month,  # 3 aylık
                                       freq="W",  # T'nin frekans bilgisi.
                                       discount_rate=0.01)

    cltv = cltv.reset_index()
    cltv_final = cltv_df.merge(cltv, on="Customer ID", how="left")
    cltv_final["segment"] = pd.qcut(cltv_final["clv"], 4, labels=["D", "C", "B", "A"])

    return cltv_final


df = df_.copy()

cltv_final2 = create_cltv_p(df)

cltv_final2.to_csv("cltv_prediction.csv")













