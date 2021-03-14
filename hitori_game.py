oyun_dosyasini_ac = open("hitori_bulmaca.txt", "r")
oyun_dosyasi = oyun_dosyasini_ac.readlines()
oyun_dosyasini_ac.close()

asil_oyun = []  # İçi doldurulduktan sonra değişmeyen liste.
oyun = []  # Her giriş yapıldığında güncellenen liste.
ulasilabilen_ogeler = []  # Tabloda birbirlerine aşağı,yukarı,sola ve sağa hareket ederek ulaşabilen öğelerin ekleneceği liste.


# Boş listelere "hitori_bulmaca.txt" dosyasından okunan verileri aktarır.
def veriyi_bos_listeye_aktar(bos_liste):
    for i in range(len(oyun_dosyasi)):
        bos_liste.insert(i, [])
        for j in range(len(oyun_dosyasi)):
            bos_liste[i].insert(j, oyun_dosyasi[i][j * 2])


veriyi_bos_listeye_aktar(asil_oyun)
veriyi_bos_listeye_aktar(oyun)


# Liste içindeki rakamların önüne ve arkasına tire işareti("-") koyar.
def liste_ici_tire_donusumu(liste):
    for a in range(len(liste)):
        for b in range(len(liste)):
            liste[a][b] = "-" + str(liste[a][b]) + "-"


# Oyunun güncel halini ekrana yazdırır.
def hitori_anlik(liste):
    print("")
    print(4 * " ", end="")
    for a in range(len(liste)):
        print(format(str(a+1), "3"), end="")
    print("\n")
    for a in range(len(liste)):
        print(str(a+1) + 2 * " ", end="")
        for b in range(len(liste)):
            print(liste[a][b], end="")
        print("")
    print("")


# Oyunda yapılacak hamle girişlerini alır.
def girdi_al():
    try:
        girdi = input("Satır numarasını (1-3), sütun numarasını (1-3) ve işlem kodunu "
                      "(B:boş, D:dolu, N:normal/işaretsiz) aralarında boşluk bırakarak giriniz: ")
        while not (len(girdi) == 5) or not (0 < int(girdi[0]) <= len(oyun)) or not (0 < int(girdi[2]) <= len(oyun)) \
                or not (girdi[4] in ["B", "D", "N"]) or not (girdi[1] == " ") or not (girdi[3] == " "):
            girdi = input("Hatalı Giriş Yaptınız. \nSatır numarasını (1-3), sütun numarasını (1-3) ve işlem kodunu "
                          "(B:boş, D:dolu, N:normal/işaretsiz) aralarında boşluk bırakarak giriniz: ")
        return girdi
    except ValueError:
        print("Hatalı Giriş Yaptınız.")
        girdi_al()


# Girişi yapılan hamleyi oyuna işler.
def hamleyi_oyuna_isle(liste, girdi_sonucu):
    if girdi_sonucu[4] == "B":
        liste[int(girdi_sonucu[0]) - 1][int(girdi_sonucu[2]) - 1] = "-X-"
    elif girdi_sonucu[4] == "D":
        liste[int(girdi_sonucu[0]) - 1][int(girdi_sonucu[2]) - 1] = \
            "(" + str(asil_oyun[int(girdi_sonucu[0]) - 1][int(girdi_sonucu[2]) - 1]) + ")"
    else:
        liste[int(girdi_sonucu[0]) - 1][int(girdi_sonucu[2]) - 1] =\
            "-" + str(asil_oyun[int(girdi_sonucu[0]) - 1][int(girdi_sonucu[2]) - 1]) + "-"


# Bir listedeki 1. ve 2. boyuttaki öğeleri birbirine dönüştürür. (Satırları sütunlara, sütunları satırlara dönüştürür.)
def satir_sutun_donusum(liste):
    yeni_liste = []
    for i in range(len(liste)):
        yeni_liste.insert(i, [])
        for j in range(len(liste)):
            yeni_liste[i].insert(j, liste[j][i])
    return yeni_liste


# Listedeki her öğeyi parantez yerine tire içine alır. ("(5)" -> "-5-")
def parantezsiz_liste(liste):
    gecici_liste = []
    for i in range(len(liste)):
        gecici_liste.insert(i, [])
        for j in range(len(liste)):
            gecici_liste[i].insert(j, "-" + liste[i][j][1] + "-")
    return gecici_liste


# Listedeki dolu(örnek: "-1" veya "(1)") öğelerin indexleriyle başka bir liste oluşturur.
def dolu_ogelerin_koordinatlarini_listele(liste):
    gecici_liste = []
    for i in range(len(liste)):
        for j in range(len(liste)):
            if liste[i][j] != "-X-":
                gecici_liste.append(str(i)+"/"+str(j))
    return gecici_liste


# Aşağı, yukarı, sağa ve sola hamlelerle ulaşılabilen dolu öğelerin koordinatlarını ulasilabilen_ogeler listesine ekler.
def dort_bir_yani_kontrol_et_ve_listeye_ekle(satir, sutun):
    if oyun[satir][sutun] != "-X-":
        try:
            if oyun[satir+1][sutun] != "-X-":
                ulasilabilen_ogeler.append(str(satir + 1) + "/" + str(sutun))
        except IndexError:
            pass
        try:
            if oyun[satir][sutun+1] != "-X-":
                ulasilabilen_ogeler.append(str(satir) + "/" + str(sutun + 1))
        except IndexError:
            pass
        if oyun[satir-1][sutun] != "-X-":
            if satir != 0:
                ulasilabilen_ogeler.append(str(satir - 1) + "/" + str(sutun))
        if oyun[satir][sutun-1] != "-X-":
            if sutun != 0:
                ulasilabilen_ogeler.append(str(satir) + "/" + str(sutun - 1))
    else:
        dort_bir_yani_kontrol_et_ve_listeye_ekle(satir + 1, sutun)


# Bir listenin içinde tekrar eden öğe bulunmayan ve öğelerinin alfabetik şekilde sıralanmış halini geri döndürür.
def ideal_liste(liste):
    return sorted(list(set(liste)))


liste_ici_tire_donusumu(oyun)
hitori_anlik(oyun)


# Oyunu başlatır ve bulmaca kurallara uygun bir şekilde çözülene kadar devam ettirir.
def oyunu_baslat():
    while True:
        hamleyi_oyuna_isle(oyun, girdi_al())
        hitori_anlik(oyun)
        for i in range(len(oyun)):
            # Satırlarda tekrar eden rakam olup olmadığını kontrol eder.
            for j in parantezsiz_liste(oyun)[i]:
                if j != "-X-" and parantezsiz_liste(oyun)[i].count(j) > 1:
                    oyunu_baslat()
            # Sütunlarda tekrar eden rakam olup olmadığını kontrol eder.
            for j in satir_sutun_donusum(parantezsiz_liste(oyun))[i]:
                if j != "-X-" and satir_sutun_donusum(parantezsiz_liste(oyun))[i].count(j) > 1:
                    oyunu_baslat()
            # Boş("-X-") karakterlerin yan yana veya alt alta gelip gelmediğini kontrol eder.
            for j in range(len(oyun)):
                try:
                    if oyun[i][j] == "-X-" and (oyun[i][j] == oyun[i][j+1] or oyun[i][j] == oyun[i+1][j]):
                        oyunu_baslat()
                except IndexError:
                    continue
# Tablodaki öğelerin birbirlerine aşağı,yukarı,sola ve sağa hareket ederek ulaşıp ulaşamadığı kontrol edilir.
# (döngünün sonundaki break komutuna kadar olan kısım)
        dort_bir_yani_kontrol_et_ve_listeye_ekle(0, 0)
        ideal_liste(ulasilabilen_ogeler)
        for a in range(30):
            for i in range(len(ideal_liste(ulasilabilen_ogeler))):
                dort_bir_yani_kontrol_et_ve_listeye_ekle(int(ideal_liste(ulasilabilen_ogeler)[i][0]), int(ideal_liste(ulasilabilen_ogeler)[i][2]))
        for i in range(len(dolu_ogelerin_koordinatlarini_listele(oyun))):
            try:
                if ideal_liste(ulasilabilen_ogeler)[i] != dolu_ogelerin_koordinatlarini_listele(oyun)[i]:
                    oyunu_baslat()
            except IndexError:
                oyunu_baslat()
        break


oyunu_baslat()
print("Tebrikler, " + str(len(oyun)) + "x" + str(len(oyun)) + " Hitori Bulmacayı Çözdünüz!")
