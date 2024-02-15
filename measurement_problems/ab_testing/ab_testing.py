######################################################
# Temel İstatistik Kavramları
######################################################
# veri bilimi en çok kullanılan yöntemdir,a ve b grupları arasında farklılık var mı diye bakılır

# "istatisliğe dayalı olmaksızın veri bilimci data lab. asistanıdır"

import itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# !pip install statsmodels
import statsmodels.stats.api as sms
from scipy.stats import ttest_1samp, shapiro, levene, ttest_ind, mannwhitneyu, \
    pearsonr, spearmanr, kendalltau, f_oneway, kruskal
from statsmodels.stats.proportion import proportions_ztest

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 10)
pd.set_option('display.float_format', lambda x: '%.5f' % x)


############################
# Sampling (Örnekleme)
############################
# bir ana kitle içinden özellikleri iyi temsil ettiği varsayılan alt kümedir, temsilci
# yapay zekanın geleceği daha az veri ile ilgilidir, daha fazla değil (az ve kalite)

populasyon = np.random.randint(0, 80, 10000) # varsayalım 100000 tane yaş var
populasyon.mean() # 39.6485

np.random.seed(115)

orneklem = np.random.choice(a=populasyon, size=100)
orneklem.mean() # 38.86

# daha az veri ile genelleme yapmamızı sağlayan kaliteli bir örneklem, 10000 kişiyi gezip yaş sormak yerine örneklem üstünden, belirli bi yanılma payı ile 100 kişiye sorsak, zaman para iş gücü faydası sağlar

np.random.seed(10)
orneklem1 = np.random.choice(a=populasyon, size=100)
orneklem2 = np.random.choice(a=populasyon, size=100)
orneklem3 = np.random.choice(a=populasyon, size=100)
orneklem4 = np.random.choice(a=populasyon, size=100)
orneklem5 = np.random.choice(a=populasyon, size=100)
orneklem6 = np.random.choice(a=populasyon, size=100)
orneklem7 = np.random.choice(a=populasyon, size=100)
orneklem8 = np.random.choice(a=populasyon, size=100)
orneklem9 = np.random.choice(a=populasyon, size=100)
orneklem10 = np.random.choice(a=populasyon, size=100)

(orneklem1.mean() + orneklem2.mean() + orneklem3.mean() + orneklem4.mean() + orneklem5.mean()
 + orneklem6.mean() + orneklem7.mean() + orneklem8.mean() + orneklem9.mean() + orneklem10.mean()) / 10 # 39.733999999999995 ana kitle ortalamına biraz daha yaşlaştı

# örneklem sayısı arttığında, bu örneklem dağılıma ilişkin ortalama ana kitlenin ortalamasın yakın veri arttığında yakınlık artar gibi, bu şekilde birden fazla örneklem olduğunda daha iyi bir sonuç olacaktır


############################
# Descriptive Statistics (Betimsel İstatistikler)
############################
# keşifçi veri analizi, betimleyici açıklayıcı tanımlayıcı istatiksel olarak geçebilir, betimlemeye çalışma çabası

df = sns.load_dataset("tips")
df.describe().T  # count  mean   std   min    25%    50%    75%    max

# değişken çarpık ise bu değişkeni temsilen medyan kullanmak daha doğru olacaktır. ortalama yanıltıcı olabilir

############################
# Confidence Intervals (Güven Aralıkları)
############################

# anakütle parametresinin tahmini değerini (istatistik değeri) kapsayabilecek iki sayıdan oluşan bir aralık bulunmasıdır.
# sitede geçirilen ortama sürenin güven aralığı? : ort: 180 ss: 40  // %95 güven aralığı : 172 - 188 demek daha güvenilir
# tek bir değer olması yerine belli bi aralık vermek daha zengin bir veri olur // ortalama +-

# Tips Veri Setindeki Sayısal Değişkenler için Güven Aralığı Hesabı
df = sns.load_dataset("tips")
df.describe().T # total_bill ortalaması 19.78594

df.head()

# amaç total_bill için güven aralığını verelim, kötü senaryoda ne kazanırım iyi senaryoda ne kazanırım  bilgisi bizim için planlamalarımızda iyi olacaktır

# total_bill ortalaması 19.78594
# total_bill güven aralığı %95 oranla : (18.663331704358477, 20.90855354154317)

sms.DescrStatsW(df["total_bill"]).tconfint_mean() # tconfint_mean : değişkenin güven aralığı

# 2.99828
# (2.823799306281822, 3.1727580707673604)
sms.DescrStatsW(df["tip"]).tconfint_mean()

# Titanic Veri Setindeki Sayısal Değişkenler için Güven Aralığı Hesabı
df = sns.load_dataset("titanic")
df.describe().T

# 29.69912
# (28.631790041821507, 30.766445252296133)
sms.DescrStatsW(df["age"].dropna()).tconfint_mean()

# 32.20421
# (28.93683123456731, 35.47158470258192)
sms.DescrStatsW(df["fare"].dropna()).tconfint_mean()

# güven aralığı hesabında, ortalama üstüne eklenecek değer : stantart sapmanın ortalamasını (ss bölü kök n(ortalama açısından bi stantard sapma))

# elimdeki sayısal değişkenlerin tek bir değer yerine, olası çekilebilecek başka ortalamalar olsaydı, yani 100 defa ortalama hesaplama yapılsaydı belirlenen aralığa düşecektir = işletme olarak yapılacak planlarda bi güvenlilik

######################################################
# Correlation (Korelasyon)
######################################################

# kolerasyon : değişkenlerin arasındaki ilişki ve bu ilişki yönü ve şiddeti ile ilgili bilgiler sağlayan istatiksel yöntem
# 1 ve -1 arasında değişir, 0 kolerasyon yok demektir
# pozitif ve negatif kolerasyon // 1 : mükemmel pozitif kolerasyon, -1 : mükemmel negatif kolerasyon
# pozitif kolerasyon : bir eğer artartken diğeri de artar (pozitif kolerasyon) // negatif kolerasyon: ters ortantı

# Bahşiş veri seti:
# total_bill: yemeğin toplam fiyatı (bahşiş ve vergi dahil)
# tip: bahşiş
# sex: ücreti ödeyen kişinin cinsiyeti (0=male, 1=female)
# smoker: grupta sigara içen var mı? (0=No, 1=Yes)
# day: gün (3=Thur, 4=Fri, 5=Sat, 6=Sun)
# time: ne zaman? (0=Day, 1=Night)
# size: grupta kaç kişi var?

df = sns.load_dataset('tips')
df.head()

df["total_bill"] = df["total_bill"] - df["tip"] # toplam ücret - bahşiş = asıl ücret

# bahşiş ve toplam ücert arasında bi ilişki var mı diye merak ediyoruz? beklediğimiz; pozitif yönlü bir ilişki
df.plot.scatter("tip", "total_bill")  # saçılım grafiği
plt.show()

df["tip"].corr(df["total_bill"]) # kolerasyon : 0.5766634471096378 // pozifit, orta şiddetli -- orta şiddetli pozitif ilişki // ödenen hesap arttıkça bahşiş artacaktır diyoruz

######################################################
# AB Testing Açıklama Örnek - Bağımsız İki Örneklem T Testi-
######################################################

# bir inanışı bir savı test etmek için kullanılan istatiksel yöntem
# grup karşılaştırmalarında temel amaç olası farklılıkların "şans eseri" ortaya çıkıp çıkmadığını göstermeye çalışmaktadır

# örneğiiin mobil uygulamada arayüz değişikliği sonrasında kullanıcıların uygulamada geçirdiği günlük süre arttı mı? değişiklik öncesi : a , değişiklik sonrası: b
# kullanıcıların ortalama süre arasında fark vardır yoktur diyip test ediyoruz AB test
# a : 55 dk, b : 58 dk amaç buradaki farkı değerlendirmek // 2. tasarım iyi diye bi ifade edilebilir mi? matemaiktsel olarak evet belki ama istatiksek olarak hayır edilemez bu 58 dk şans eseri ortaya çıkmış olabilir sonuçta ortalama bi kitle üzerinden bu değerlendirme yapıldı

# örneğiiin kayıt ekranı sadeleştirmesinden sonra çarpan (bu sayfaya gelmek) kayıt olma oranı arttı mı?
# a: 0.42 kayıt b: 0.38 yeni tasarım daha iyi diyemeyiz şans eseri ortaya çıkmış olabilir, istatiki olarak test etmemiz gerekir

# örneğiiiin iki farklı aşı firmasının geliştirdiği aşıların belirli bi süre içerisindeki koruma oranları birbirinden farklı mı? 1 aylık sürede a : 0.80 virüsü yenmiş b: 0.84 verisü yenmiş // bu iki oran üzerinden 2. aşı daha iyi diyemeyiz

# AB testi deyince, çok yaygınca ya iki grubun ortalaması ya iki gruba ilişkin oranlar
# iki grup ortalamasını arasında karşılaştırma yapılmak istendiğinde;

######################################################
# AB Testing (Bağımsız İki Örneklem T Testi)
######################################################

# 1. Hipotezleri Kur / iki grup ortalaması arasında fark yoktur gibi bi hipotez grup test edicez gibi
# 2. Varsayım Kontrolü
#   - 1. Normallik Varsayımı
#   - 2. Varyans Homojenliği
# 3. Hipotezin Uygulanması
#   - 1. Varsayımlar sağlanıyorsa bağımsız iki örneklem t testi (parametrik test)
#   - 2. Varsayımlar sağlanmıyorsa mannwhitneyu testi (non-parametrik test)
# Not:
# - Normallik sağlanmıyorsa direk 2 numara. Varyans homojenliği sağlanmıyorsa 1 numaraya arguman girilir.
# - Normallik incelemesi öncesi aykırı değer incelemesi ve düzeltmesi yapmak faydalı olabilir.
# 4. p-value değerine göre sonuçları yorumla

############################
# Uygulama 1: Sigara İçenler ile İçmeyenlerin Hesap Ortalamaları Arasında İst Ol An Fark var mı?
############################

# garsonlar diyor ki, en az 1 sigara içen varsa daha fazla bahşiş bırakıyor olabilir diyor: hipotez

df = sns.load_dataset("tips")
df.head()

df.groupby("smoker").agg({"total_bill": "mean"}) # sigara içme içmeme kırılımda ortalama hesap

# Yes       20.75634
# No        19.18828  matematiksel olarak fark var ama istatiksel olarak test etmemiz gerekiyor

############################
# 1. Hipotezi Kur
############################

# biz bu hipotezi kullanıcaz // iki grup ortalması fark var yok kıyası
# H0: M1 = M2 (yokluk hipotezi, iki grup arası fark yok, eşittir)
# H1: M1 != M2 (iki grup arasında fark var, eşit değil)

# not:
# HO: H1 <= H2, HI: H1 > H2 // HO: H1 >= H2, H2: H1 < H2
# p < 0.05 ise HO ret diyerek yorumlarımızı gerçekleştiricez

############################
# 2. Varsayım Kontrolü
############################

# Normallik Varsayımı: iki grubunda ayrı ayrı normal dağılması gerekir
# Varyans Homojenliği: iki grubun dağımlarının birbirine benzer olup olmaması

############################
# Normallik Varsayımı
############################

# H0: Normal dağılım varsayımı sağlanmaktadır.
# H1:..sağlanmamaktadır.


test_stat, pvalue = shapiro(df.loc[df["smoker"] == "Yes", "total_bill"]) # shapiro : dağılım normal mi değil mi?
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# Test Stat = 0.9367, p-value = 0.0002

# p-value < ise 0.05'ten HO RED.
# p-value < değilse 0.05 H0 REDDEDILEMEZ.

# HO RED - Varsayımlar sağlanmıyorsa mannwhitneyu testi (non-parametrik test)

test_stat, pvalue = shapiro(df.loc[df["smoker"] == "No", "total_bill"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# Test Stat = 0.9045, p-value = 0.0000

# HO RED - Varsayımlar sağlanmıyorsa mannwhitneyu testi (non-parametrik test)

############################
# Varyans Homojenligi Varsayımı
############################

# H0: Varyanslar Homojendir
# H1: Varyanslar Homojen Değildir

test_stat, pvalue = levene(df.loc[df["smoker"] == "Yes", "total_bill"],
                           df.loc[df["smoker"] == "No", "total_bill"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# Test Stat = 4.0537, p-value = 0.0452

# p-value < ise 0.05 'ten HO RED.
# p-value < değilse 0.05 H0 REDDEDILEMEZ.

# HO RED : Varyanslar Homojen Değildir

# İKİ VARSAYIMDA SAĞLANMADI

############################
# 3 ve 4. Hipotezin Uygulanması
############################

# 1. Varsayımlar sağlanıyorsa bağımsız iki örneklem t testi (parametrik test)
# 2. Varsayımlar sağlanmıyorsa mannwhitneyu testi (non-parametrik test) -- BİZ BUNU YAPIYORUZ

############################ sağlanmış gibi yapalım bi
# 1.1 Varsayımlar sağlanıyorsa bağımsız iki örneklem t testi (parametrik test)
############################

test_stat, pvalue = ttest_ind(df.loc[df["smoker"] == "Yes", "total_bill"],
                              df.loc[df["smoker"] == "No", "total_bill"],
                              equal_var=True)

print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# Test Stat = 1.3384, p-value = 0.1820

# p-value < ise 0.05 'ten HO RED.
# p-value < değilse 0.05 H0 REDDEDILEMEZ.

# HO REDDEDILEMEZ : M1 = M2 // bu iki grup arasında istatiksel bi fark yoktur

############################ bu test için asıl yapacağımız test:
# 1.2 Varsayımlar sağlanmıyorsa mannwhitneyu testi (non-parametrik test)
############################

test_stat, pvalue = mannwhitneyu(df.loc[df["smoker"] == "Yes", "total_bill"],
                                 df.loc[df["smoker"] == "No", "total_bill"])

print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# Test Stat = 7531.5000, p-value = 0.3413

# p-value < ise 0.05 'ten HO RED.
# p-value < değilse 0.05 H0 REDDEDILEMEZ.

# HO REDDEDILEMEZ : M1 = M2 // bu iki grup arasında istatiksel bi fark yoktur, sigara içen içmeyen hesap ödemesi ortalamaları arasında bi fark yoktur yani
# asıl noktamız HO reddedilebilir ya da reddedilemez olayımız.



############################
# Uygulama 2: Titanic Kadın ve Erkek Yolcuların Yaş Ortalamaları Arasında İstatistiksel Olarak Anl. Fark. var mıdır?
############################

df = sns.load_dataset("titanic")
df.head()

df.groupby("sex").agg({"age": "mean"}) # cinsiyet kırılımda yaş ortalamaları dağılımı
# fark var gibi görünüyor ama şans eseri mi bu buna bakıcaz?


# 1. Hipotezleri kur:
# H0: M1  = M2 (Kadın ve Erkek Yolcuların Yaş Ortalamaları Arasında İstatistiksel Olarak Anl. Fark. Yoktur)
# H1: M1! = M2 (... vardır)


# 2. Varsayımları İncele

# Normallik varsayımı - shapiro testi
# H0: Normal dağılım varsayımı sağlanmaktadır.
# H1:..sağlanmamaktadır


test_stat, pvalue = shapiro(df.loc[df["sex"] == "female", "age"].dropna()) # shapiro : dağılım normal mi değil mi? dropna(): eksileri uçur
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# Test Stat = 0.9848, p-value = 0.0071 HO REDDEDİLİR     p-value < ise 0.05 'ten HO RED.


test_stat, pvalue = shapiro(df.loc[df["sex"] == "male", "age"].dropna())
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# Test Stat = 0.9747, p-value = 0.0000 HO REDDEDİLİR     p-value < ise 0.05 'ten HO RED.

# İKİ GRUP İÇİNDE VARSAYIM SAĞLANMADI -- Varsayımlar sağlanmıyorsa mannwhitneyu testi (non-parametrik test) -- BİZ BUNU YAPIYORUZ ASLINDA

# Varyans homojenliği
# H0: Varyanslar Homojendir
# H1: Varyanslar Homojen Değildir

test_stat, pvalue = levene(df.loc[df["sex"] == "female", "age"].dropna(),
                           df.loc[df["sex"] == "male", "age"].dropna()) #
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# Test Stat = 0.0013, p-value = 0.9712 --HO REDDEDİLEMEZ VARYANSALAR HOMEJEN AMA BUNLA İŞİMİZ YOK



# Varsayımlar sağlanmadığı için nonparametrik BİZİM İÇİN BU

test_stat, pvalue = mannwhitneyu(df.loc[df["sex"] == "female", "age"].dropna(),
                                 df.loc[df["sex"] == "male", "age"].dropna())
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# Test Stat = 53212.5000, p-value = 0.0261  -- HO REDDEDİLİR, KADIN VE ERKEK YAŞ ORTALAMALARI ARASINDA İSTATİSKİ OLARAK DA FARK VARDIR


# 90 280



############################
# Uygulama 3: Diyabet Hastası Olan ve Olmayanların Yaşları Ort. Arasında İst. Ol. Anl. Fark var mıdır?
############################

df = pd.read_csv("datasets/diabetes.csv")
df.head()

df.groupby("Outcome").agg({"Age": "mean"}) # Outcome : diyabet olup olmama
# 0       31.19000
# 1       37.06716
# yaş ile diyabet arasında bi ilişki var mıdır?


# 1. Hipotezleri kur
# H0: M1 = M2
# Diyabet Hastası Olan ve Olmayanların Yaşları Ort. Arasında İst. Ol. Anl. Fark Yoktur
# H1: M1 != M2
# .... vardır.

# p-value < ise 0.05 'ten HO RED.

# 2. Varsayımları İncele

# Normallik Varsayımı (H0: Normal dağılım varsayımı sağlanmaktadır.)
test_stat, pvalue = shapiro(df.loc[df["Outcome"] == 1, "Age"].dropna())
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# Test Stat = 0.9546, p-value = 0.0000 - p-value < ise 0.05 'ten HO RED.


test_stat, pvalue = shapiro(df.loc[df["Outcome"] == 0, "Age"].dropna())
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# Test Stat = 0.8012, p-value = 0.0000 - p-value < ise 0.05 'ten HO RED.


# Normallik varsayımı sağlanmadığı için nonparametrik.

# Hipotez (H0: M1 = M2)
test_stat, pvalue = mannwhitneyu(df.loc[df["Outcome"] == 1, "Age"].dropna(),
                                 df.loc[df["Outcome"] == 0, "Age"].dropna())
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# Test Stat = 92050.0000, p-value = 0.0000 - p-value < ise 0.05 'ten HO RED.

# ikisi arasında fark yoktur hipotezini reddettik, yani yaş ve diyabet olma olayının varlığını istatiki olarak ispatladık.

###################################################
# İş Problemi: Kursun Büyük Çoğunluğunu İzleyenler ile İzlemeyenlerin Puanları Birbirinden Farklı mı?
###################################################

# H0: M1 = M2 (... iki grup ortalamaları arasında ist ol.anl.fark yoktur.)
# H1: M1 != M2 (...vardır)

df = pd.read_csv("datasets/course_reviews.csv")
df.head()

df[(df["Progress"] > 75)]["Rating"].mean() # 4.860491071428571

df[(df["Progress"] < 25)]["Rating"].mean() # 4.7225029148853475
# kursu daha çok izleyenlerin puanları daha yüksek olması şans mı?


test_stat, pvalue = shapiro(df[(df["Progress"] > 75)]["Rating"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# Test Stat = 0.3160, p-value = 0.0000 HO RED - normallik varsayımı sağlanmadı

test_stat, pvalue = shapiro(df[(df["Progress"] < 25)]["Rating"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# Test Stat = 0.5710, p-value = 0.0000 HO RED - normallik varsayımı sağlanmadı


# Normallik varsayımı sağlanmadığı için nonparametrik.

test_stat, pvalue = mannwhitneyu(df[(df["Progress"] > 75)]["Rating"],
                                 df[(df["Progress"] < 25)]["Rating"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# Test Stat = 661481.5000, p-value = 0.0000 HO RED

# # H0: M1 = M2 (... iki grup ortalamaları arasında ist ol.anl.fark yoktur.) REDDETTİK. YANİ: iki grup ortalamaları arasında istatiki olarak bi fark vardır, yani kursun büyük çoğunluğunu bitirenlerin puanları daha fazla puan verilmiş ( 4.860491071428571 > 4.7225029148853475)


# grup ortalamaları grup medyanlarını kıyasladık. şimdi ise iki oran karşılaştırması....


######################################################
# AB Testing (İki Örneklem Oran Testi)
######################################################

# H0: p1 = p2 : Yeni Tasarımın Dönüşüm Oranı ile Eski Tasarımın Dönüşüm Oranı Arasında İst. Ol. Anlamlı Farklılık Yoktur.
# H1: p1 != p2 : ... Fark Vardır.

basari_sayisi = np.array([300, 250]) # 300 kayıt, 250 kayıt // başarılı sayıları tek array
gozlem_sayilari = np.array([1000, 1100]) # 1000 kişi, 1100 kişi // gözlem sayısı tek array

proportions_ztest(count=basari_sayisi, nobs=gozlem_sayilari) # proportions_ztest metodu ile kıyaslama yap
# (3.7857863233209255, 0.0001532232957772221) HO REDDEDİLİR, fark vardır

basari_sayisi / gozlem_sayilari # array([0.3    , 0.22727273])  0.3 daha başarılı


############################
# Uygulama: Kadın ve Erkeklerin Hayatta Kalma Oranları Arasında İst. Olarak An. Farklılık var mıdır?
############################

# H0: p1 = p2
# Kadın ve Erkeklerin Hayatta Kalma Oranları Arasında İst. Olarak An. Fark yoktur

# H1: p1 != p2
# .. vardır

df = sns.load_dataset("titanic")
df.head()

# p-value < ise 0.05 'ten HO RED.
# p-value < değilse 0.05 H0 REDDEDILEMEZ.

df.loc[df["sex"] == "female", "survived"].mean() # 0.7420382165605095

df.loc[df["sex"] == "male", "survived"].mean() # 0.18890814558058924


female_succ_count = df.loc[df["sex"] == "female", "survived"].sum() # kadınlar için başarı sayısı
male_succ_count = df.loc[df["sex"] == "male", "survived"].sum()


test_stat, pvalue = proportions_ztest(count=[female_succ_count, male_succ_count], # başarı sayısı
                                      nobs=[df.loc[df["sex"] == "female", "survived"].shape[0], # gözlem sayısı
                                            df.loc[df["sex"] == "male", "survived"].shape[0]])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# Test Stat = 16.2188, p-value = 0.0000  p-value < ise 0.05 'ten HO RED.

# kadın ve erkeklerin hayatta kalma oranları arasında bi fark vardır.

######################################################
# ANOVA (Analysis of Variance)
######################################################

# İkiden fazla grup ortalamasını karşılaştırmak için kullanılır.


# HAFTANIN GÜNLERİ VE TOPLAM KAZANÇ ARASINDA İSTATİKİ Bİ FARK VAR MI?

df = sns.load_dataset("tips")
df.head()

df.groupby("day")["total_bill"].mean() # günlere göre toplam kazanç

# Thur   17.68274  hi
# Fri    17.15158  hi
# Sat    20.44138  hs
# Sun    21.41000  hs

# hi hs arası fark şans eseri mi?

# 1. Hipotezleri kur

# HO: m1 = m2 = m3 = m4 -- Grup ortalamaları arasında fark yoktur.
# H1: .. fark vardır


# 2. Varsayım kontrolü

# Normallik varsayımı
# Varyans homojenliği varsayımı

# Varsayım sağlanıyorsa: one way anova testi
# Varsayım sağlanmıyorsa: kruskal testi


# H0: Normal dağılım varsayımı sağlanmaktadır.

for group in list(df["day"].unique()):
    pvalue = shapiro(df.loc[df["day"] == group, "total_bill"])[1]
    print(group, 'p-value: %.4f' % pvalue)
# Sun p-value: 0.0036   -   pvalue < 0. 5 HO red
# Sat p-value: 0.0000   -   pvalue < 0. 5 HO red
# Thur p-value: 0.0000  -   pvalue < 0. 5 HO red
# Fri p-value: 0.0409   -   pvalue < 0. 5 HO red

# hiçbiri için normallik varsayımı sağlanmadı


# H0: Varyans homojenliği varsayımı sağlanmaktadır.

test_stat, pvalue = levene(df.loc[df["day"] == "Sun", "total_bill"],
                           df.loc[df["day"] == "Sat", "total_bill"],
                           df.loc[df["day"] == "Thur", "total_bill"],
                           df.loc[df["day"] == "Fri", "total_bill"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# Test Stat = 0.6654, p-value = 0.5741   pvalue > 0,5 HO REDDEDİLEMEZ

# varyans homejenliği sağlandı ama bunla işimiz yok, çünkü normallik varsayımı sağlanmamıştı zaten


# 3. Hipotez testi ve p-value yorumu

# Hiç biri için varsayım sağlamıyordy.
df.groupby("day").agg({"total_bill": ["mean", "median"]})

# day      mean   median
# Thur   17.68274 16.20000
# Fri    17.15158 15.38000
# Sat    20.44138 18.24000
# Sun    21.41000 19.63000


# HO: Grup ortalamaları arasında ist ol anl fark yoktur

# parametrik anova testi: işimiz bunla değil
f_oneway(df.loc[df["day"] == "Thur", "total_bill"],
         df.loc[df["day"] == "Fri", "total_bill"],
         df.loc[df["day"] == "Sat", "total_bill"],
         df.loc[df["day"] == "Sun", "total_bill"])
# F_onewayResult(statistic=2.7674794432863363, pvalue=0.04245383328952047) HO RED, gruplar arası fark var İŞİMİZ BUNLA DEĞİL AMA


# Nonparametrik anova testi:
kruskal(df.loc[df["day"] == "Thur", "total_bill"],
        df.loc[df["day"] == "Fri", "total_bill"],
        df.loc[df["day"] == "Sat", "total_bill"],
        df.loc[df["day"] == "Sun", "total_bill"])
# KruskalResult(statistic=10.403076391437086, pvalue=0.01543300820104127) HO RED, bu gruplar arasında istatiki bi fark vardır.


# istatiki fark var ama hangi gruptan kaynaklanıyor? tukey testii  // (0.05)' göre ilerlemeliyiz
from statsmodels.stats.multicomp import MultiComparison
comparison = MultiComparison(df['total_bill'], df['day']) # ödenen hesap ve grup değişkeni
tukey = comparison.tukeyhsd(0.05)
print(tukey.summary())


# Multiple Comparison of Means - Tukey HSD, FWER=0.05
# ====================================================
# group1 group2 meandiff p-adj   lower   upper  reject
# ----------------------------------------------------
#   Fri    Sat   3.2898 0.4541 -2.4799  9.0595  False
#   Fri    Sun   4.2584 0.2371 -1.5856 10.1025  False
#   Fri   Thur   0.5312 0.9957 -5.4434  6.5057  False
#   Sat    Sun   0.9686 0.8968 -2.6088   4.546  False
#   Sat   Thur  -2.7586 0.2374 -6.5455  1.0282  False
#   Sun   Thur  -3.7273 0.0668 -7.6264  0.1719  False
#----------------------------------------------------

# cuma ve cumartesi arasında ki fark 3.2898 düzeltilmiş plavue: 0.4541 HO RED değil fark yok.
# ..... çok istediğimiz gibi olmadı sonuç.
# ikili karlılaştırmada bi fark yok. bütün grupta bi fark var, bu yüzden fark yoktur gibi de davranılabilir....

# Sun   Thur  -3.7273 0.0668 -7.6264  0.1719  False  // en düşük plaue perşembe pazar farkı


# comparison.tukeyhsd(0.10) yaptık sadece durumu görebilmek için,
from statsmodels.stats.multicomp import MultiComparison
comparison = MultiComparison(df['total_bill'], df['day']) # ödenen hesap ve grup değişkeni
tukey = comparison.tukeyhsd(0.10)
print(tukey.summary())


# Multiple Comparison of Means - Tukey HSD, FWER=0.10
# ===================================================
# group1 group2 meandiff p-adj   lower  upper  reject
# ---------------------------------------------------
#    Fri    Sat   3.2898 0.4541 -1.8481 8.4277  False
#    Fri    Sun   4.2584 0.2371 -0.9457 9.4626  False
#    Fri   Thur   0.5312 0.9957 -4.7892 5.8515  False
#    Sat    Sun   0.9686 0.8968  -2.217 4.1543  False
#    Sat   Thur  -2.7586 0.2374 -6.1308 0.6135  False
#    Sun   Thur  -3.7273 0.0668 -7.1995 -0.255   True
# ---------------------------------------------------


#    Sun   Thur  -3.7273 0.0668 -7.1995 -0.255   True farkın sebebi

