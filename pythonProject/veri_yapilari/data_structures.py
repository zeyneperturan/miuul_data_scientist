###############################################
# VERİ YAPILARI (DATA STRUCTURES)
###############################################
# - Veri Yapılarına Giriş ve Hızlı Özet
# - Sayılar (Numbers): int, float, complex
# - Karakter Dizileri (Strings): str
# - Boolean (TRUE-FALSE): bool
# - Liste (List)
# - Sözlük (Dictionary)
# - Demet (Tuple)
# - Set


###############################################
# Veri Yapılarına Giriş ve Hızlı Özet
##############################################

# Sayılar: integer
x = 46
type(x)

# Sayılar: float
x = 10.3
type(x)

# Sayılar: complex - çok yaygın kullanılmaz!
x = 2j + 1
type(x)

# String
x = "Hello ai era"
type(x)

# Boolean
True
False
type(True)
5 == 4
3 == 2
1 == 1
type(3 == 2)

# Liste (list) - köşeli parantez
x = ["btc", "eth", "xrp"]
type(x)

x = [1, 2, 3]
type(x)

# Sözlük (dictionary) - süslü parantez/ key-value değeleri : ile ayrılır
x = {"name": "Peter", "Age": 36}
type(x)

# Tuple (demet) - normal parantez
x = ("python", "ml", "ds")
type(x)

# Set - süslü parantez / küme gibi düşünebilir, sözlükten farkı key value değerleri yok
x = {"python", "ml", "ds"}
type(x)

# Not: Liste, tuple, set ve dictionary veri yapıları aynı zamanda Python Collections (Arrays) olarak geçmektedir.


###############################################
# Sayılar (Numbers): int, float, complex
###############################################

a = 5
b = 10.5

a * 3
a / 7
a * b / 10
a ** 2

#######################
# Tipleri değiştirmek
#######################

int(b)
float(a)

int(a * b / 10)

c = a * b / 10

int(c)


###############################################
# Karakter Dizileri (Strings)
###############################################

# tek tırnak çift tırnak ikisi de aynı sonuç
# print ekrana yazdırmak amaçlı kullanılır
print("John")
print('John')

"John"
name = "John"
name = 'John'
print(name)

#######################
# Çok Satırlı Karakter Dizileri
#######################

"""Veri Yapıları: Hızlı Özet, 
Sayılar (Numbers): int, float, complex, 
Karakter Dizileri (Strings): str, 
List, Dictionary, Tuple, Set"""

# atama yapalım ki sonrasında lazım olduğundan direk long_str diye çağıralım
long_str = """Veri Yapıları: Hızlı Özet, 
Sayılar (Numbers): int, float, complex, 
Karakter Dizileri (Strings): str, 
List, Dictionary, Tuple, Set, 
Boolean (TRUE-FALSE): bool"""

#######################
# Karakter Dizilerinin Elemanlarına Erişmek
#######################

name
name[0] # 0. index = ilk eleman
name[3]
name[2]

#######################
# Karakter Dizilerinde Slice İşlemi
#######################

name[0:2] # 0-2. KADAR index aralığı 0. ve 1. eleman
long_str[0:10]

#######################
# String İçerisinde Karakter Sorgulamak
#######################

long_str

"veri" in long_str  # long str içinde veri kelimesi var mı? küçük büyük harf duyarlı - FALSE

"Veri" in long_str

"bool" in long_str

###############################################
# String (Karakter Dizisi) Metodları
###############################################

dir(str) # veri yapılarının üzerinde çalışan özel metodlara erişmek için / string için kullanılanlar
dir(int)

#######################
# len - uzunluk verir
#######################

name = "john" # string değer
type(name)    # name tipi
type(len)     # builtin_function_or_method ?? kafası karışık / AMA FONKSİYON
len(name)     # 4

len("vahitkeskin")
len("miuul")

# yapı, class içerinde tanımlandıysa method / class yapısı içinde değilse fonksiyondur
# method ve fonksiyon aslında aynı şeydir ama method bağımlı fonksiyon bağımsızdır
# methot -- class yapısı, başında boşluk gördün self gördün, type() sorgulaması yapamadın

#######################
# upper() & lower(): küçük-büyük dönüşümleri
#######################

"miuul".upper()
"MIUUL".lower()

# type(upper) # upper bir methoddur bu yüzden hata verir. type fonksiyonu sadece fonksiyon tipi sorgular
# type(upper()) # upper bir methoddur bu yüzden hata verir. type fonksiyonu sadece fonksiyon tipi sorgular


#######################
# replace: karakter değiştirir
#######################

hi = "Hello AI Era"
hi.replace("l", "p") # eski ve yeni argümanlarını girmeni ister

#######################
# split: böler
#######################

"Hello AI Era".split() # argümanın ön tanımlı değeri boşluktur ve boşluklara göre bölüp, liste gibi tutar

#######################
# strip: kırpar
#######################

" ofofo ".strip() # ön tanımı olan boşluk değerine göre kırpar, boşlukları sildi
"ofofo".strip("o") # baştan sonra o harflerini kırptı


#######################
# capitalize: ilk harfi büyütür
#######################

"foo".capitalize()

dir("foo") # dir(str) ile aynı şeyi verir

#######################
# startswith: ilk harf kontrolü
#######################

"foo".startswith("f") # verilmiş olan argüman olan f ile başlayıp başlamadığını verir, TRUE

###############################################
# Liste (List) - en yaygın veri yapılarındandır
###############################################

# - Değiştirilebilir
# - Sıralıdır. Index işlemleri yapılabilir.
# - Kapsayıcıdır. - birden fazla veri yapısını bi arada tutar - not_nam gibi

notes = [1, 2, 3, 4]
type(notes)
names = ["a", "b", "v", "d"]
not_nam = [1, 2, 3, "a", "b", True, [1, 2, 3]]

not_nam[0]    # 0. index 1
not_nam[5]    # 5. index True
not_nam[6]    # 6. index [1, 2, 3]
not_nam[6][1] # 6. indexin 1. indexi 2

type(not_nam[6])  # 6. indexin tipi List
type(not_nam[6][1]) # 6. indexin 1. indexinin tipi int

notes[0] = 99 # notes listesinin 0. indexini 99 yapalım
notes

not_nam[0:4]


###############################################
# Liste Metodları (List Methods)
###############################################

dir(notes) # liste metodları nelerdir?

#######################
# len: builtin python fonksiyonu, boyut bilgisi.
#######################

len(notes)
len(not_nam)

#######################
# append: eleman ekler
#######################

notes
notes.append(100) # sonuna ekler

#######################
# pop: indexe göre siler
#######################

notes.pop(0) # 0. indexi sil

#######################
# insert: indexe ekler
#######################

notes.insert(2, 99) # 2. indexe 99 ekledik


###############################################
# Sözlük (Dictonary)
###############################################

# Değiştirilebilir.
# Sırasız. (3.7 sonra sıralı.)
# Kapsayıcı - int string liste gibi değerleri içinde bulundurabilir

# key-value çiftlerinden oluşur

dictionary = {"REG": "Regression",
              "LOG": "Logistic Regression",
              "CART": "Classification and Reg"}

dictionary["REG"] # key çağır value gelsin


dictionary = {"REG": ["RMSE", 10],
              "LOG": ["MSE", 20],
              "CART": ["SSE", 30]}

dictionary["CART"][1]

dictionary = {"REG": 10,
              "LOG": 20,
              "CART": 30}

#######################
# Key Sorgulama
#######################

"YSA" in dictionary  #dictionary sözlüğü içerisinde YSA var mı? FALSE

#######################
# Key'e Göre Value'ya Erişmek
#######################

# her iki kullanım da aynı ama ilki daha kullanışlı
dictionary["REG"]
dictionary.get("REG")

#######################
# Value Değiştirmek
#######################

dictionary["REG"] = ["YSA", 10] # REG keyinin değerini YSA, 10 olarak değiştir
dictionary["REG"]

#######################
# Tüm Key'lere Erişmek
#######################

dictionary.keys()

#######################
# Tüm Value'lara Erişmek
#######################

dictionary.values()

#######################
# Tüm Çiftleri Tuple Halinde Listeye Çevirme
#######################

dictionary.items()

#######################
# Key-Value Değerini Güncellemek
#######################

dictionary.update({"REG": 11}) # key değerini REG olanı 11 olarak güncelle

dictionary["REG"]

#######################
# Yeni Key-Value Eklemek
#######################

dictionary.update({"RF": 10}) # RF yoktu, yenisini ekledi

###############################################
# Demet (Tuple) - Listelerin değişime kapalı kardeşi
###############################################

# - Değiştirilemez.
# - Sıralıdır. - elamanlarına indexe erişim
# - Kapsayıcıdır. - bi çok veri tipini barındırır

t = ("john", "mark", 1, 2)
type(t)

t[0]
t[0:3]

t[0] = 99 # hata verecektir, güncelleme desteklemiyor ama bi yolu aşağıda ama istenmez;

t = list(t) # tupple'ı listeye çevir
t[0] = 99 # güncelle
t = tuple(t) # sobrasunda tekrar tupple


###############################################
# Set - küme işlemleri gibi, kesişim fark vs görülmek istendiğinde ama kullanım düşük
###############################################

# - Değiştirilebilir.
# - Sırasız + Eşsizdir.
# - Kapsayıcıdır.

#######################
# difference(): İki kümenin farkı
#######################

set1 = set([1, 3, 5])
set2 = set([1, 2, 3])

type(set1)

# set1'de olup set2'de olmayanlar.
set1.difference(set2)
set1 - set2 # mis gibi basit kullanım

# set2'de olup set1'de olmayanlar.
set2.difference(set1)
set2 - set1 # mis gibi basit kullanım

#######################
# symmetric_difference(): İki kümede de birbirlerine göre olmayanlar
#######################

# her ikisi de aynı sonucu verecektir
set1.symmetric_difference(set2)
set2.symmetric_difference(set1)

#######################
# intersection(): İki kümenin kesişimi
#######################

set1 = set([1, 3, 5])
set2 = set([1, 2, 3])

# her ikisi de aynı sonucu verecektir
set1.intersection(set2)
set2.intersection(set1)

set1 & set2 # mis gibi basit kullanım


#######################
# union(): İki kümenin birleşimi
#######################

# her ikisi de aynı sonucu verecektir
set1.union(set2)
set2.union(set1)

#######################
# isdisjoint(): İki kümenin kesişimi boş mu? başında is varsa TRUE FALSE dönüşü bekliyordur
#######################

set1 = set([7, 8, 9])
set2 = set([5, 6, 7, 8, 9, 10])

# her ikisi de aynı sonucu verecektir
set1.isdisjoint(set2)
set2.isdisjoint(set1)

#######################
# isdisjoint(): Bir küme diğer kümenin alt kümesi mi?
#######################

set1.issubset(set2)
set2.issubset(set1)

#######################
# issuperset(): Bir küme diğer kümeyi kapsıyor mu?
#######################

set2.issuperset(set1)
set1.issuperset(set2)
