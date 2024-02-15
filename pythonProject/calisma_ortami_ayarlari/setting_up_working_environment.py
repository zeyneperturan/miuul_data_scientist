###############################################
# Sayılar (Numbers) ve Karakter Dizileri (Strings)
###############################################

print("Hello world")
print("Hello AI Era")

#sayılar: int, float, kompleks
#karakter dizisi: " ", ''

print(9)
9.2
type(9.2) #type fonksiyonu ile sayı ve karakter tiplerini öğreniyoruz
type("Mrb")

###############################################
# Atamalar ve Değişkenler (Assignments & Variables)
###############################################

#programın akışında daha sonra kullanmak istediğimizde atama işlemi yaparız

a = 9
a

b = "hello ai era"
b

c = 10
a * c
a * 10
d = a - c

###############################################
# Virtual Environment (Sanal Ortam)  ve (Package Managment) Paket Yönetimi
###############################################

# VE - sanal ortam: izole çalışma ortamları oluşturmak için kullanılan araçlardır
# Farklı çalışma ortamları oluşturabilecek farklı kütüphane ve versiyon ihtiyaçlarını çalışmalar birbirini etkilemeyecek şekilde oluşturma imkanı sağlar.

# Sanal ortam araçları: venv, virtualadenv, pipenv , conda**
# Paket yönetim araçları: pip, pipenv, conda**

# venv vw virtualenv paket yönetim aracı olarak pip'i kullanıyor.
# conda ve pipenv hem sanal ortam hem de paket yönetici <3 / Paket yönetimi ve bağımlılık kontrolleri


# Sanal ortamların listelenmesi:
# conda env list

# Sanal ortam oluşturma:
# conda create –n myenv

# Sanal ortamı aktif etme:
# conda activate myenv

# Yüklü paketlerin listelenmesi:
# conda list

# Paket yükleme:
# conda install numpy

# Aynı anda birden fazla paket yükleme:
# conda install numpy scipy pandas

# Paket silme:
# conda remove package_name

# Belirli bir versiyona göre paket yükleme:
# conda install numpy=1.20.1

# Paket yükseltme:
# conda upgrade numpy

# Tüm paketlerin yükseltilmesi:
# conda upgrade –all

# pip: pypi (python package index) paket yönetim aracı

# Paket yükleme:
# pip install pandas

# Paket yükleme versiyona göre:
# pip install pandas==1.2.1

# Paket bilgilerini kişiye aktarmamız gerektiğinde:
# conda env export > environment.yaml

