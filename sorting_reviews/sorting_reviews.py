############################################
# SORTING REVIEWS - yorum sıralama
############################################

# iş bilgisi faktörleri, birden fazla etken varsa bunlar standartlaştırılmalı ve ağırlıklı hesaplanmalı,
# iş bilgisi ile harmanlayarak kullanmamız

# yorumlar nasıl sıralanmalı: düşük yüksek puanla ilgilenmiyoruz, kullanıcıya en doğru sosyal ispatı sunmaya çalışıyoruz, yorumlar tarihe göre mi sıralanmalı ne olmalı? "yorumu faydalı bulma" ya göre sıralamak daha iyi - user qualtiy score

import pandas as pd
import math
import scipy.stats as st

pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

###################################################
# Up-Down Diff Score = (up ratings) − (down ratings)
###################################################

# Review 1: 600 up 400 down total 1000 -  600 beğeni 200 dislike toplam 1000
# Review 2: 5500 up 4500 down total 10000 -

# frekansı kaçırıyoruz

def score_up_down_diff(up, down):
    return up - down

# Review 1 Score:
score_up_down_diff(600, 400)  # 200

# Review 2 Score
score_up_down_diff(5500, 4500) # 1000

# hangi yorum daha yukarıdadır? review1'in yüzdesi daha yüksek olduğundan üsttedir


# örnek soru
score_up_down_diff(750,400)

#I. up, down = (580,480) # 100
#II. up, down = (1000,200) # 800
#III. up, down = (950,450) # 500
#IV. up, down = (750,400) # 350


###################################################
# Score = Average rating = (up ratings) / (all ratings)    : ortalama puan -- bu daha mantıklı
###################################################
# like oranı üstünden scor hesabı

def score_average_rating(up, down):
    if up + down == 0:
        return 0
    return up / (up + down)

score_average_rating(600, 400) # 0.6    -- oran olarak daha büyüktür
score_average_rating(5500, 4500) # 0.55


# Review 1: 2 up 0 down total 2
# Review 2: 100 up 1 down total 101

score_average_rating(2, 0) # 1.0  -- bu daha iyi, daha üsttedir -- ama saçma oldu, sayıyı bulamadık
score_average_rating(100, 1) # 0.9900990099009901


###################################################
# Wilson Lower Bound Score - wlb
###################################################

# bize ikili etkişelim barındıran reviewi skorlama imkanı, like-dislike
# güven aralığı hesaplar, alt sınırı wlb olarak kabul eder
#

# up 600 - down 400
# oran 0.6
# güven aralığı 0.5  0.7
# alt sınır : skor: 0.5


# fonksiyonu bilelim
def wilson_lower_bound(up, down, confidence=0.95): # oran istatistiği güven aralığı
    """
    Wilson Lower Bound Score hesapla

    - Bernoulli parametresi p için hesaplanacak güven aralığının alt sınırı WLB skoru olarak kabul edilir.
    - Hesaplanacak skor ürün sıralaması için kullanılır.
    - Not:
    Eğer skorlar 1-5 arasıdaysa 1-3 negatif, 4-5 pozitif olarak işaretlenir ve bernoulli'ye uygun hale getirilebilir.
    Bu beraberinde bazı problemleri de getirir. Bu sebeple bayesian average rating yapmak gerekir.

    Parameters
    ----------
    up: int
        up count
    down: int
        down count
    confidence: float
        confidence

    Returns
    -------
    wilson score: float

    """
    n = up + down
    if n == 0:
        return 0
    z = st.norm.ppf(1 - (1 - confidence) / 2)
    phat = 1.0 * up / n
    return (phat + z * z / (2 * n) - z * math.sqrt((phat * (1 - phat) + z * z / (4 * n)) / n)) / (1 + z * z / n)


wilson_lower_bound(600, 400) # 0.5693094295142663 -- artık eminimiz bu yorum daha üstte, daha faydalı bulunmuş bi yorum
wilson_lower_bound(5500, 4500) # 0.5402319557715324

wilson_lower_bound(2, 0) # 0.3423802275066531
wilson_lower_bound(100, 1) # 0.9460328420055449 -- bakın 100 beğeni olan daha faydalı daha üstte olan bi yorum


###################################################
# Case Study
###################################################

up = [15, 70, 14, 4, 2, 5, 8, 37, 21, 52, 28, 147, 61, 30, 23, 40, 37, 61, 54, 18, 12, 68] #
down = [0, 2, 2, 2, 15, 2, 6, 5, 23, 8, 12, 2, 1, 1, 5, 1, 2, 6, 2, 0, 2, 2] #
comments = pd.DataFrame({"up": up, "down": down})


# score_pos_neg_diff
comments["score_pos_neg_diff"] = comments.apply(lambda x: score_up_down_diff(x["up"],
                                                                             x["down"]), axis=1)

# score_average_rating
comments["score_average_rating"] = comments.apply(lambda x: score_average_rating(x["up"], x["down"]), axis=1)

# wilson_lower_bound
comments["wilson_lower_bound"] = comments.apply(lambda x: wilson_lower_bound(x["up"], x["down"]), axis=1)

# sıralama bu şekilde mi olmalı bilemiyoruz bi bakıcaz, -13 olan buralarda olmamalı...


# bu sıralamayı wlb'ye göre azalan şekilde yapmalıyız.
comments.sort_values("wilson_lower_bound", ascending=False)

# 147 like en tepeye geldi..

# RATİNG - PUANLAMA
# elimizde bi puan hesabı var diyelim, bir average alabilirim ama bunu daha fazla hassaslaştırabilirim, zaman - kullanıcı davranışı...
# 5 yıldızlı bi rating olduğundan bunu Bayesian Avarege Ratinf ile hesaplatabilirim
# hepsini birleştirip  ağırlıklarını özel  biçimlendirip birden falz akoşulla hasaslaştabilirim.


# SORTING PRODUCTS- ÜRÜN SIRALAMA
# birden fazla faktör için ağırlık vermek gerek, ilgili puana yazılmış özel bi formül bulunabilir
# puanladıktan sıraladık
# olasılıksal ortalama... nihai ortalama

# SORTGIN REVİEWS - YORUM SIRALAMA
# wls







