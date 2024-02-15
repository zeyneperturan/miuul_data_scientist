###############################################
# FONKSİYONLAR, KOŞULLAR, DÖNGÜLER, COMPREHENSIONS
###############################################
# - Fonksiyonlar (Functions)
# - Koşullar (Conditions)
# - Döngüler (Loops)
# - Comprehesions


###############################################
# FONKSİYONLAR (FUNCTIONS)
###############################################

#######################
# Fonksiyon Okuryazarlığı
#######################

help(print) # print kullanımı hakkında bilgiler, hangi argümanlar gerekli vs dökümantasyonu

print("a", "b") # içerisinde girilen değeri yazdırma
print("a", "b", sep="__") # a ve b arasına __ koyalım / sep argümanı ile birlikte

#######################
# Fonksiyon Tanımlama
#######################

# def - isimlendirme - argüman: bi alt satırda yapılacak işlem

def calculate(x): # def ile fonksiyon tanımına başlıyoruz
    print(x * 2) # yapılacak işlem

calculate(5) # calculate fonksiyonun argümanı olan x gördüğümüz yere 5 yazdık


# İki argümanlı/parametreli bir fonksiyon tanımlayalım.
def summer(arg1, arg2):
    print(arg1 + arg2)


summer(7, 8) # summer(7, 8)

summer(8, 7)

summer(arg2=8, arg1=7) # summer(arg2=8, arg1=7) değişkenlerin yerlerini değişik kullanmak istiyorsak


#######################
# Docstring - fonskyiona herkesin anlayabileceği dilde bi döküman yazma işi """ """
#######################

def summer(arg1, arg2):
    print(arg1 + arg2)


def summer(arg1, arg2):
    """
    Sum of two numbers

    Args:
        arg1: int, float
        arg2: int, float

    Returns:
        int, float

    """

    print(arg1 + arg2)


summer(1, 3)


#######################
# Fonksiyonların Statement/Body Bölümü
#######################

# def function_name(parameters/arguments): - argüman zorunlu değildir
#     statements (function body)

def say_hi():
    print("Merhaba")
    print("Hi")
    print("Hello")


say_hi()


def say_hi(string):
    print(string)
    print("Hi")
    print("Hello")

say_hi("miuul") # argüman varsa argüman kullanmak zorundayız


def multiplication(a, b):
    c = a * b
    print(c)

multiplication(10, 9)

# girilen değerleri bir liste içinde saklayacak fonksiyon.

list_store = [] # boş liste oluşturduk

def add_element(a, b):
    c = a * b
    list_store.append(c) # list_store'a a * b yi atadığımız c'yi eklicez
    print(list_store) # listeyi yazdıralım


add_element(1, 8)
add_element(18, 8)
add_element(180, 10)

list_store  # [8, 144, 1800]

#######################
# Ön Tanımlı Argümanlar/Parametreler (Default Parameters/Arguments)
#######################

def divide(a, b):
    print(a / b)

divide(1, 2)


def divide(a, b): # b=1 ön tanım verilebilir
    print(a / b)

divide(10) # tek argüman hata verdi  ya yukarı daki argüman tanım yerine b= 1 gibi ön tanım verilebilir


def say_hi(string="Merhaba"): # ön tanım verilmiş
    print(string)
    print("Hi")
    print("Hello")


say_hi("mrb")

#######################
# Ne Zaman Fonksiyon Yazma İhtiyacımız Olur?
#######################

# belediyede işe girdik diyelim sokak lamba sinyalleri ısı nem pil durumu verilerine göre bazı hesaplamalar

# varm, moisture, charge

(56 + 15) / 80
(17 + 45) / 70
(52 + 45) / 80


# DRY

def calculate(varm, moisture, charge): # ısı nem pil durumu argümanlı olarak fonksiyon yazalım
    print((varm + moisture) / charge) # istenilen matematiksel hesaplama


calculate(98, 12, 78) # girilmesi istenilen değerler


#######################
# Return: Fonksiyon Çıktılarını Girdi Olarak Kullanmak
######################

def calculate(varm, moisture, charge):
    print((varm + moisture) / charge)


# calculate(98, 12, 78) * 10 - hata verir calculte tipi noneType olduğundan intle çarpamadık bu yüzden return lazım

def calculate(varm, moisture, charge):
    return (varm + moisture) / charge


calculate(98, 12, 78) * 10

a = calculate(98, 12, 78)


def calculate(varm, moisture, charge): # argümanların yeni değeleri ve bu üç değer üstünden hesaplanan değeri çıktı olarak alalım
    varm = varm * 2
    moisture = moisture * 2
    charge = charge * 2
    output = (varm + moisture) / charge
    return varm, moisture, charge, output


type(calculate(98, 12, 78))

varma, moisturea, chargea, outputa = calculate(98, 12, 78)


#######################
# Fonksiyon İçerisinden Fonksiyon Çağırmak
######################

def calculate(varm, moisture, charge):
    return int((varm + moisture) / charge)


calculate(90, 12, 12) * 10


def standardization(a, p):
    return a * 10 / 100 * p * p


standardization(45, 1)

# yeni yazılan fonksiyonda, çağırılan fonk argümanları verildi, a'yı yazmadık çünkü yeni yazılan fonksiyon içinde değerlendirilecek / dışardan biçimlendirilmeyecek
def all_calculation(varm, moisture, charge, p):
    a = calculate(varm, moisture, charge) # ilk fonksiyonu çağırıyoruz
    b = standardization(a, p) # ikinci fonksiyonu çağırıyoruz
    print(b * 10)


all_calculation(1, 3, 5, 12)

# a içerde oluşturulmayacağından argüman yerine yazdık
def all_calculation(varm, moisture, charge, a, p):
    print(calculate(varm, moisture, charge))
    b = standardization(a, p)
    print(b * 10)


all_calculation(1, 3, 5, 19, 12)

#######################
# Lokal & Global Değişkenler (Local & Global Variables)
#######################

list_store = [1, 2] # global, varolan bi değişken, her yerden erişim var

def add_element(a, b):
    c = a * b # c lokal değişken
    list_store.append(c) # append ile, lokalden globale etki yaratıyoruz
    print(list_store)

add_element(1, 9)


###############################################
# KOŞULLAR (CONDITIONS)
###############################################

# True-False'u hatırlayalım.
1 == 1
1 == 2

# if
if 1 == 1:
    print("something")

if 1 == 2:
    print("something")

number = 11

if number == 10:
    print("number is 10")

number = 10
number = 20


#number'a farklı değerler verip kendimizi terkrarladık, fonksiyon yazalım
def number_check(number):
    if number == 10:
        print("number is 10")

number_check(12)

#######################
# else
#######################

def number_check(number):
    if number == 10:
        print("number is 10")

number_check(12)


def number_check(number):
    if number == 10:
        print("number is 10")
    else:
        print("number is not 10")

number_check(12)

#######################
# elif
#######################

def number_check(number):
    if number > 10:
        print("greater than 10")
    elif number < 10:
        print("less than 10")
    else:
        print("equal to 10")

number_check(6)

###############################################
# DÖNGÜLER (LOOPS)
###############################################
# for loop
# 1) nerede gezilecek 2) temsili isim (farketmez)

students = ["John", "Mark", "Venessa", "Mariam"]

# listeye erişelim, bi tekrar hali oldu yine
students[0]
students[1]
students[2]

# students nesnesi içinde student temsili ile geziyoruz
for student in students:
    print(student) # bütün listeyi yazdırdık

# yakalanan her nesnenin harflerini büyütmek istedik
for student in students:
    print(student.upper())

# maaş listesi
salaries = [1000, 2000, 3000, 4000, 5000]

# maaşları yazdıralım
for salary in salaries:
    print(salary)

# her bir maaş için %20 zam uygulama işlemi, int olsun
for salary in salaries:
    print(int(salary*20/100 + salary))

# %30 zam
for salary in salaries:
    print(int(salary*30/100 + salary))

# %50 zam, tekrarlamaya başladık seri fonksiyon
for salary in salaries:
    print(int(salary*50/100 + salary))

# hem maaşı hem zammı biçimlendirecek fonksiyon, maaş ve zam argümanlı
def new_salary(salary, rate):
    return int(salary*rate/100 + salary)

# haydaaa yine kendimizi tekrarladık
new_salary(1500, 10)
new_salary(2000, 20)

# genel bi fonksiyon yazdık mis, şimdi her departman bunu kullanabilir
for salary in salaries:
    print(new_salary(salary, 20))

# başka departmanın maaş listesi
salaries2 = [10700, 25000, 30400, 40300, 50200]

# genel bi fonksiyon yazdık mis, şimdi her departman bunu kullanabilir
for salary in salaries2:
    print(new_salary(salary, 15))

# maaşları gezelim, maaş 3000 üstü ise şu kadar altı ise şu kadar zam
for salary in salaries:
    if salary >= 3000:
        print(new_salary(salary, 10))
    else:
        print(new_salary(salary, 20))



#######################
# Uygulama - Mülakat Sorusu
#######################
# Amaç: Çift index büyük harf tek index küçük - çift olanlar 2ye tam bölünür mantığı
# Amaç: Aşağıdaki şekilde string değiştiren fonksiyon yazmak istiyoruz.

# before: "hi my name is john and i am learning python"
# after: "Hi mY NaMe iS JoHn aNd i aM LeArNiNg pYtHoN"

range(len("miuul")) # range: iki değer arasında sayı üretme / 0'dan 5'e kadar gez
range(0, 5)

for i in range(len("miuul")):
    print(i)

# 4 % 2 == 0
# m = "miuul"
# m[0]

def alternating(string):
    new_string = ""  # yapılan değişiklikleri buraya kaydetmek üzere boş bir string
    # girilen string'in index'lerinde gez.
    for string_index in range(len(string)):
        # index çift ise büyük harfe çevir.
        if string_index % 2 == 0:
            new_string += string[string_index].upper() # stringe bi değer ekleme, üstüne ekleme +=
        # index tek ise küçük harfe çevir.
        else:
            new_string += string[string_index].lower()
    print(new_string)

alternating("zeynep erturan şahin")

#######################
# break & continue & while
#######################

salaries = [1000, 2000, 3000, 4000, 5000]

# break: aranan koşul yakalandığında çalışmayı kes

for salary in salaries:
    if salary == 3000:
        break
    print(salary)

# continue: aranan koşul yakalandığında bu değeri atla devam et
for salary in salaries:
    if salary == 3000:
        continue
    print(salary)


# while = şart sağlandı sürece çalışmayı sürdürür
number = 1
while number < 5:
    print(number)
    number += 1

#######################
# Enumerate: Otomatik Counter/Indexer ile for loop
#######################

# örneğin bir listede gezerken, işlem uygulanan bilgi ve indexini tutar

students = ["John", "Mark", "Venessa", "Mariam"]

for student in students:
    print(student)

for index, student in enumerate(students): # index ve indexe ait değer yazdırıcaz
    print(index, student)

A = []
B = []

for index, student in enumerate(students):
    if index % 2 == 0:
        A.append(student)
    else:
        B.append(student)


#######################
# Uygulama - Mülakat Sorusu
#######################
# divide_students fonksiyonu yazınız.
# Çift indexte yer alan öğrencileri bir listeye alınız.
# Tek indexte yer alan öğrencileri başka bir listeye alınız.
# Fakat bu iki liste tek bir liste olarak return olsun.

students = ["John", "Mark", "Venessa", "Mariam"]

# ey python ben geliyorum fonksiyon tanımlicam tamam gel
def divide_students(students):
    groups = [[], []] # yazdırmak için bir liste içinde iki liste
    for index, student in enumerate(students):
        if index % 2 == 0:
            groups[0].append(student)
        else:
            groups[1].append(student)
    print(groups)
    return groups

st = divide_students(students)
st[0]
st[1]


#######################
# alternating fonksiyonunun enumerate ile yazılması - eski mülakat sorusuuuu !!!!
#######################

def alternating_with_enumerate(string):
    new_string = "" # boş string oluşturduk
    for i, letter in enumerate(string): # hem string hem indexinde geziyoruz
        if i % 2 == 0:
            new_string += letter.upper()
        else:
            new_string += letter.lower()
    print(new_string)

alternating_with_enumerate("hi my name is john and i am learning python")

#######################
# Zip x kadar farklı listeleri birarada değelendirme imkanı sağlar -
#######################

# eleman sayıları 4 - 4 - 3 iken tüm listelerde ki ilk 3 ü eşleştirdi!!!

students = ["John", "Mark", "Venessa", "Mariam"]

departments = ["mathematics", "statistics", "physics", "astronomy"]

ages = [23, 30, 26, 22]

list(zip(students, departments, ages))

###############################################
# lambda, map, filter, reduce
###############################################

def summer(a, b):
    return a + b

summer(1, 3) * 9

# lambda: kullan at fonksiyonu tanımlama şekli
new_sum = lambda a, b: a + b

new_sum(4, 5)

# map: döngü yazmaktan kurtarız, nesne ver ve nesneye uygulanacak işlemi ver yeter
salaries = [1000, 2000, 3000, 4000, 5000]

def new_salary(x):
    return x * 20 / 100 + x

new_salary(5000)

for salary in salaries:
    print(new_salary(salary))

list(map(new_salary, salaries)) # döngü yazmaktan kurtulduk


# del new_sum -- woooooowwwwww
list(map(lambda x: x * 20 / 100 + x, salaries))
list(map(lambda x: x ** 2 , salaries))

# FILTER : koşula göre filtreleyip liste formunda sonuçları tutalım
list_store = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
list(filter(lambda x: x % 2 == 0, list_store))

# REDUCE : indirgeme - elemanlara tek tek işlem yap
from functools import reduce
list_store = [1, 2, 3, 4]
reduce(lambda a, b: a + b, list_store) # 1 artı 1 2, 2 artı 2 4.....


###############################################
# COMPREHENSIONS
###############################################

#######################
# List Comprehension - birden fazla satırlık işi tek satırda yapmaca, çıktı liste
#######################

salaries = [1000, 2000, 3000, 4000, 5000]

def new_salary(x):
    return x * 20 / 100 + x

for salary in salaries:
    print(new_salary(salary))

null_list = [] # boş bi liste uluşturduk, işlem yapılan maaşları buraya ekle

for salary in salaries:
    null_list.append(new_salary(salary))

null_list = []

for salary in salaries: # salariste gezdi her gezişinde salary olarak isimlendirdi
    if salary > 3000:
        null_list.append(new_salary(salary))
    else:
        null_list.append(new_salary(salary * 2))

# maaşlar listesinde ki her bi maaşı 2 ile çarpalım
[salary * 2 for salary in salaries]
# maaşı 3000den az olanları 2 ile çarpalım
[salary * 2 for salary in salaries if salary < 3000] # tek if var sağda
# maaşı 3000den büyük olanları 2 ile çarp, küçük olanları 0 ile çarp
[salary * 2 if salary < 3000 else salary * 0 for salary in salaries] # if else kullanım yerine dikkat, if else varsa for sonda
# var olan bi fonksiyonu da kullanalım
[new_salary(salary * 2) if salary < 3000 else new_salary(salary * 0.2) for salary in salaries]

# List Comprehension ile tek satırda yapalım - oooiiiiyyyyyyyy
[new_salary(salary * 2) if salary < 3000 else new_salary(salary) for salary in salaries]

# tüm öğlenciler, istemediğin öğrenciler listeleri iki listeye ayrı ayrı işlem yap
students = ["John", "Mark", "Venessa", "Mariam"]
students_no = ["John", "Venessa"]

# student listesinde ki öğrenci student no'da varsa küçük yaz, diğerleri büyük
[student.lower() if student in students_no else student.upper() for student in students]
# studetda ki öğrenciler, student no da yoksa büyük yaz - üstte ki ile aynı sonucu verecektir
[student.upper() if student not in students_no else student.lower() for student in students]

#######################
# Dict Comprehension - tek satırda bam bam
#######################

dictionary = {'a': 1,
              'b': 2,
              'c': 3,
              'd': 4}

dictionary.keys() # key değerleri
dictionary.values() # key değerleri
dictionary.items() # item çiftlerine her bir değerine tupple olarak, elemanlı key value

{k: v ** 2 for (k, v) in dictionary.items()} # key sabit, valuelerinin karesi, liste içi tupple

{k.upper(): v for (k, v) in dictionary.items()} # keyleri büyült, value aynı

{k.upper(): v*2 for (k, v) in dictionary.items()} # key value değiştir



#######################
# Uygulama - Mülakat Sorusu
#######################

# Amaç: çift sayıların karesi alınarak bir sözlüğe eklenmek istemektedir
# Key'ler orjinal değerler value'lar ise değiştirilmiş değerler olacak.


numbers = range(10)
new_dict = {}

for n in numbers: # numbers içinde gezilecek 0 1 2 3 4....
    if n % 2 == 0: # değerimiz çift ise
        new_dict[n] = n ** 2 # değerin kendisini key'e, karesini value'ye eklicez

# çok iyi olay, key aynı value değişmiş olacak
{n: n ** 2 for n in numbers if n % 2 == 0} # numbers gezildi çiftlerin karesi

#######################
# List & Dict Comprehension Uygulamalar
#######################

#######################
# Bir Veri Setindeki Değişken İsimlerini Değiştirmek
#######################

# before:
# ['total', 'speeding', 'alcohol', 'not_distracted', 'no_previous', 'ins_premium', 'ins_losses', 'abbrev']

# after:
# ['TOTAL', 'SPEEDING', 'ALCOHOL', 'NOT_DISTRACTED', 'NO_PREVIOUS', 'INS_PREMIUM', 'INS_LOSSES', 'ABBREV']

import seaborn as sns
df = sns.load_dataset("car_crashes")
df.columns

# eski yöntem
for col in df.columns: # df.colums üstünde gez
    print(col.upper())

# eski yöntem ile bunu listede tutalım
A = []

for col in df.columns:
    A.append(col.upper())

df.columns = A

# yeni şekille
df = sns.load_dataset("car_crashes")

df.columns = [col.upper() for col in df.columns] # df.columsta gez her bi elemanı büyült ve listede tut

#######################
# İsminde "INS" olan değişkenlerin başına FLAG diğerlerine NO_FLAG eklemek istiyoruz.
#######################

# before:
# ['TOTAL',
# 'SPEEDING',
# 'ALCOHOL',
# 'NOT_DISTRACTED',
# 'NO_PREVIOUS',
# 'INS_PREMIUM',
# 'INS_LOSSES',
# 'ABBREV']

# after:
# ['NO_FLAG_TOTAL',
#  'NO_FLAG_SPEEDING',
#  'NO_FLAG_ALCOHOL',
#  'NO_FLAG_NOT_DISTRACTED',
#  'NO_FLAG_NO_PREVIOUS',
#  'FLAG_INS_PREMIUM',
#  'FLAG_INS_LOSSES',
#  'NO_FLAG_ABBREV']

[col for col in df.columns if "INS" in col] # içinde INS olanları getir

["FLAG_" + col for col in df.columns if "INS" in col] # INS varsa FLAG_ ekle

["FLAG_" + col if "INS" in col else "NO_FLAG_" + col for col in df.columns] # .. yoksa NO_FLAG

df.columns = ["FLAG_" + col if "INS" in col else "NO_FLAG_" + col for col in df.columns] # kalıcı olarak df'in isimleri haline getirelim

#######################
# Amaç key'i string, value'su aşağıdaki gibi bir liste olan sözlük oluşturmak.
# Sadece sayısal değişkenler için yapmak istiyoruz.
#######################

# Output:
# {'total': ['mean', 'min', 'max', 'var'],
#  'speeding': ['mean', 'min', 'max', 'var'],
#  'alcohol': ['mean', 'min', 'max', 'var'],
#  'not_distracted': ['mean', 'min', 'max', 'var'],
#  'no_previous': ['mean', 'min', 'max', 'var'],
#  'ins_premium': ['mean', 'min', 'max', 'var'],
#  'ins_losses': ['mean', 'min', 'max', 'var']}

import seaborn as sns
df = sns.load_dataset("car_crashes")
df.columns

# uzun yol

# df[col].dtype != "O" - O: kategorik (object) olmayan değişkenleri seçiyoruz
num_cols = [col for col in df.columns if df[col].dtype != "O"]
soz = {}
agg_list = ["mean", "min", "max", "sum"] # value kısmı

for col in num_cols:
    soz[col] = agg_list # key yerine değişken, value yerine agg_list listesini yazıcaz

# kısa yol
new_dict = {col: agg_list for col in num_cols}

df[num_cols].head() # sayısal değerler gelecek sadece object olanları almamıştık

# agg fonskyionuna sözlük yollayıp df uygularsak, df içinde varsa ki var; istediğimiz min max mean... olarak uyguluyor. ŞOK
df[num_cols].agg(new_dict)

liste = [1,2,3,4,5]
yeni_liste = [i for i in liste]
print(yeni_liste)

print([i*2 for i in range(1,5)])


def tek_mi(x):
    if x % 2 == 0:
        return False
    if x % 2 != 0:
        return True


tek_sayi = [i for i in range(1, 11) if tek_mi(i)]

print(tek_sayi)


eski_fiyat = {'süt': 1.02, 'kahve': 2.5, 'ekmek': 2.5}

dolar_tl = 0.76
yeni_fiyat = {item: value*dolar_tl for (item, value) in eski_fiyat.items()}
print(yeni_fiyat)


original_dict = {'ahmet': 38, 'mehmet': 48, 'ali': 57, 'veli': 33}

dict2 = {k: v for (k, v) in original_dict.items() if v % 2 == 0}
print(dict2)