import requests
import re
import matplotlib.pyplot as plt
import numpy as np


class Tekmovalka:
    def __init__(self, ime, drzava):
        self._ime = ime
        self._drzava = drzava
        self._medalje = {'zlato':0, 'srebro':0, 'bron':0}
        self._rezultati = dict()
    
    def ime(self):
        return self._ime

    def drzava(self):
        return self._drzava
    
    def medalje(self):
        return self._medalje
    
    def rezultati(self):
        return self._rezultati
    
    def dodaj_disciplino(self, disciplina, mesto, cas):
        self._rezultati[disciplina] = {'mesto':mesto, 'cas':cas}
        if mesto == 1:
            self._medalje['zlato'] += 1
        elif mesto == 2:
            self._medalje['srebro'] += 1
        elif mesto == 3:
            self._medalje['bron'] += 1
    
    def __repr__(self):
        return self.__class__.__name__ + "(" + self._ime + ", " + self._drzava + ", " + str(self._medalje) + ", " + str(self._rezultati) + ")"
    
    def __str__(self):
        return "Ime: {},\nDržava: {},\nMedalje: {},\nRezultati: {}".format(self._ime, self._drzava, self._medalje, self._rezultati)



def spremeni_v_sekunde(cas):
    minute, sekunde = cas.split(':')
    total = float(minute)*60 + float(sekunde)
    return total

def spremeni_v_minute(cas):
    minute = cas // 60
    sekunde = cas - minute*60
    return '{:.0f}:{:.2f}'.format(minute, sekunde)

slovar_medalj = {}
def medalje_za_drzave(slovar, drzave, mesta):
    """{drzava : [zlata, srebrna, bronasta]} slovar vseh drzav in njihovih dosezkov"""
    for i in range(3):
        drzava = drzave[i]
        if drzava not in slovar:
            slovar[drzava] = [0,0,0]
        slovar[drzava][mesta[i]-1] += 1


#### slovar objektov (ime:objekt)
vse_tekmovalke = dict()

def slovar_objektov(disciplina, imena, drzave, casi, mesta):
    for i in range(len(casi)):
        #print(i)
        ime = imena[i]
        drzava = drzave[i]
        mesto = mesta[i]
        cas = casi[i]
        if ime not in vse_tekmovalke:
            vse_tekmovalke[ime] = Tekmovalka(ime, drzava)
        vse_tekmovalke[ime].dodaj_disciplino(disciplina, mesto, cas)


data = []

#COMBINED SKIING WOMEN=================================================================================================================
url = 'https://en.wikipedia.org/wiki/Alpine_skiing_at_the_2014_Winter_Olympics_–_Women%27s_combined'
spletna = requests.get(url).text
disciplina = 'Combined'
vse = re.findall(r'<td align="left">.*?<a href="/wiki/.+?" title=".+?">(.+?)</a>', spletna)
imena = vse[::2]
drzave = vse[1::2]
casi = re.findall(r'<td>(2\:*\d\d\.\d\d)</td>', spletna)
mesta = list(range(1, len(imena)+1))
dnf = ["dnf" for _ in range(len(mesta)-len(casi))]

slovar_objektov(disciplina, imena, drzave, casi+dnf, mesta)
data.append([spremeni_v_sekunde(cas) for cas in casi])
medalje_za_drzave(slovar_medalj, drzave, mesta)


#DOWNHILL WOMEN=================================================================================================================================
url = 'https://en.wikipedia.org/wiki/Alpine_skiing_at_the_2014_Winter_Olympics_–_Women%27s_downhill'
spletna = requests.get(url).text
disciplina = 'Downhill'
vse = re.findall(r'<td align="left">.*?<a href="/wiki/.+?" title=".+?">(.+?)</a>', spletna)
imena = vse[::2]
drzave = vse[1::2]
casi = re.findall(r'<td.*>(\d\:\d\d\.\d\d)', spletna)
mesta = [1, 1] + list(range(3,len(imena)+1))
dnf = ["dnf" for _ in range(len(mesta)-len(casi))]

slovar_objektov(disciplina, imena, drzave, casi+dnf, mesta)
data.append([spremeni_v_sekunde(cas) for cas in casi])
medalje_za_drzave(slovar_medalj, drzave, mesta)


#GIANT SLALOM WOMEN===========================================================================================================================================
url = 'https://en.wikipedia.org/wiki/Alpine_skiing_at_the_2014_Winter_Olympics_–_Women%27s_giant_slalom'
spletna = requests.get(url).text
disciplina = 'Giant-Slalom'
vse = re.findall(r'<td align="left">.*?<a href="/wiki/.+?" title=".+?">(.+?)</a>', spletna)
imena = vse[::2]
drzave = vse[1::2]
casi = re.findall(r'<td.*>([2|3]\:*\d\d\.\d\d)</td>', spletna)
mesta = list(range(1,15)) + [14] + list(range(16,90))
dnf = ["dnf" for _ in range(len(mesta)-len(casi))]

slovar_objektov(disciplina, imena, drzave, casi+dnf, mesta)
data.append([spremeni_v_sekunde(cas) for cas in casi])
medalje_za_drzave(slovar_medalj, drzave, mesta)


#SLALOM WOMEN===================================================================================================================================
url = 'https://en.wikipedia.org/wiki/Alpine_skiing_at_the_2014_Winter_Olympics_–_Women%27s_slalom'
spletna = requests.get(url).text
disciplina = 'Slalom'
vse = re.findall(r'<td align="left">.*?<a href="/wiki/.+?" title=".+?">(.+?)</a>', spletna)
imena = vse[::2]
drzave = vse[1::2]
casi = re.findall(r'<td>(\d*\:*\d\d\.\d\d)</td>', spletna)[2::3][:-3]
mesta = list(range(1, len(imena)+1))
dnf = ["dnf" for _ in range(len(mesta)-len(casi))]

slovar_objektov(disciplina, imena, drzave, casi+dnf, mesta)
data.append([spremeni_v_sekunde(cas) for cas in casi])
medalje_za_drzave(slovar_medalj, drzave, mesta)


# #SUPER-G WOMEN============================================================================================================================
url = 'https://en.wikipedia.org/wiki/Alpine_skiing_at_the_2014_Winter_Olympics_–_Women%27s_super-G'
spletna = requests.get(url).text
disciplina = 'Super-G'
vse = re.findall(r'<td align="left">.*?<a href="/wiki/.+?" title=".+?">(.+?)</a>', spletna)
imena = vse[::2]
drzave = vse[1::2]
casi = re.findall(r'<td.*>(\d*\:*\d\d\.\d\d)</td>', spletna)
casi = casi[1:12] + [casi[11]] + casi[12:]
mesta = list(range(1,11)) + [11, 11] + list(range(13,len(imena)+1))
dnf = ["dnf" for _ in range(len(mesta)-len(casi))]

slovar_objektov(disciplina, imena, drzave, casi+dnf, mesta)
data.append([spremeni_v_sekunde(cas) for cas in casi])
medalje_za_drzave(slovar_medalj, drzave, mesta)



#korelacijski koeficienti============================================================================================================================
coef_comb_dw = round(np.corrcoef(data[0], data[1][:len(data[0])])[0, 1], 3)
coef_comb_gs = round(np.corrcoef(data[0], data[2][:len(data[0])])[0, 1], 3)
coef_comb_sl = round(np.corrcoef(data[0], data[3][:len(data[0])])[0, 1], 3)
coef_comb_sg = round(np.corrcoef(data[0], data[4][:len(data[0])])[0, 1], 3)
coef_dw_gs = round(np.corrcoef(data[1], data[2][:len(data[1])])[0, 1], 3)
coef_dw_sl = round(np.corrcoef(data[1], data[3][:len(data[1])])[0, 1], 3)
coef_dw_sg = round(np.corrcoef(data[4], data[1][:len(data[4])])[0, 1], 3)
coef_gs_sl = round(np.corrcoef(data[3], data[2][:len(data[3])])[0, 1], 3)
coef_gs_sg = round(np.corrcoef(data[4], data[2][:len(data[4])])[0, 1], 3)
coef_sl_sg = round(np.corrcoef(data[4], data[3][:len(data[4])])[0, 1], 3)

#pisanje v datoteko===============================================================================================================================================
with open("prikaz_podatkov.txt", "w", encoding='utf8') as dat:
    dat.write("IME".ljust(30) + "DRZAVA".ljust(20) + "GIANT-SLALOM".ljust(25) + "SUPER-G".ljust(25) + "SLALOM".ljust(25) + "COMBINED".ljust(25) + "DOWNHILL\n")
    
    # 'Ragnhild Mowinckel': Tekmovalka(Ragnhild Mowinckel, Norway, {'zlato': 0, 'srebro': 0, 'bron': 0}, {'Combined': {'mesto': 6, 'cas': '2:36.15'}}) 
    for ime, objekt in vse_tekmovalke.items():
        drzava = objekt.drzava()
        #ljust(30) = left align za 30 presledkov 
        dat.write(f"{ime.ljust(30)}{drzava.ljust(20)}")
        
        for disciplina in ["Giant-Slalom", "Super-G", "Slalom", "Combined", "Downhill"]:
            if disciplina in objekt.rezultati():
                cas = objekt.rezultati()[disciplina]['cas']
                mesto = objekt.rezultati()[disciplina]['mesto']
                dat.write(f"{str((mesto, cas)).ljust(25)}")
            else:
                dat.write("did not participate".ljust(25))
        
        dat.write("\n")
    dat.write("\n")
    dat.write("\n")
    dat.write("\n")
    dat.write("DISCIPLINA 1".ljust(17) + "DISCIPLINA 2".ljust(20) + "KORELACIJSKI KOEFICIENT".ljust(25) + "STOPNJA POVEZANOSTI\n")
    dat.write("Combined".ljust(17) + "Downhill".ljust(20) + str(coef_comb_dw).ljust(25) + "Visoka\n")
    dat.write("Combined".ljust(17) + "Giant-Slalom".ljust(20) + str(coef_comb_gs).ljust(25) + "Visoka\n")
    dat.write("Combined".ljust(17) + "Slalom".ljust(20) + str(coef_comb_sl).ljust(25) + "Visoka\n")
    dat.write("Combined".ljust(17) + "Super-G".ljust(20) + str(coef_comb_sg).ljust(25) + "Visoka\n")
    dat.write("Downhill".ljust(17) + "Giant Slalom".ljust(20) + str(coef_dw_gs).ljust(25) + "Zelo visoka\n")
    dat.write("Downhill".ljust(17) + "Slalom".ljust(20) + str(coef_dw_sl).ljust(25) + "Zelo visoka\n")
    dat.write("Downhill".ljust(17) + "Super-G".ljust(20) + str(coef_dw_sg).ljust(25) + "Zelo visoka\n")
    dat.write("Giant Slalom".ljust(17) + "Slalom".ljust(20) + str(coef_gs_sl).ljust(25) + "Zelo visoka\n")
    dat.write("Giant Slalom".ljust(17) + "Super-G".ljust(20) + str(coef_gs_sg).ljust(25) + "Zelo visoka\n")
    dat.write("Slalom".ljust(17) + "Super-G".ljust(20) + str(coef_sl_sg).ljust(25) + "Zelo visoka\n")



#===========================================================================================================================================
def box_plot():
    plt.rcParams['toolbar'] = 'None'

    M = max(data[0] + data[1] + data[2] + data[3] + data[4])
    m = min(data[0] + data[1] + data[2] + data[3] + data[4])
    razmak = int((M - m)/8)
    ves_data = list(range(int(m), int(M), razmak))
    casi = [spremeni_v_minute(i) for i in ves_data]
    fig1 = plt.figure(num="Box plot", figsize=(7, 7))

    plt.boxplot(data)
    plt.semilogy()
    plt.minorticks_off()
    plt.xticks([1, 2, 3, 4, 5], ['Combined', 'Downhill', "Giant Slalom", "Slalom", "Super-G"])
    plt.yticks(ves_data, casi)
    plt.ylabel('Časi [min:s]')
    plt.title('Škatla z brki za posamezno smučarsko disciplino').set_fontweight('bold')
    plt.show()


drzava = list(slovar_medalj.keys())
zlata, srebrna, bronasta = [], [], []
for tabela in slovar_medalj.values():
    zlata.append(tabela[0])
    srebrna.append(tabela[1])
    bronasta.append(tabela[2])

def bar_chart_medalje():
    plt.rcParams['toolbar'] = 'None'
    fig2, ax = plt.subplots(num="Bar chart", figsize=(10,7))
    ax.set_title('Skupno število doseženih medalj na Olimpijskih igrah 2014').set_fontweight('bold')
    ax.barh(drzava, zlata, label='Zlata', color="gold")
    ax.barh(drzava, srebrna, left=zlata, label='Srebrna', color="grey")
    ax.barh(drzava, bronasta, left=[i+j for i,j in zip(zlata,srebrna)], label='Bronasta', color="brown")
    ax.set_xlabel("Skupno število medalj")
    ax.legend()
    plt.show()

#Primerjava stevila medalj glede na velikost populacije
def bar_chart_delezi():
    drzave_spletna = requests.get("https://simple.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population").text
    drzave = re.findall(r'<tr>.*?<td align="left">.*?<a .*?>([a-zA-Z ,()]*?)</a>.*?<td .*?>(.*?)</td>', drzave_spletna, re.MULTILINE + re.DOTALL)
    Usa = drzave[2][1].replace(",","")
    Germany = drzave[18][1].replace(",","")
    Austria = drzave[98][1].replace(",","")
    Switzerland = drzave[99][1].replace(",","")
    Slovenia = drzave[146][1].replace(",","")

    delez_germany = format((sum(slovar_medalj["Germany"])/int(Germany))*100, ".2e")
    delez_austria = format((sum(slovar_medalj["Austria"])/int(Austria))*100, ".2e")
    delez_usa = format((sum(slovar_medalj["United States"])/int(Usa))*100, ".2e")
    delez_switzerland = format((sum(slovar_medalj["Switzerland"])/int(Switzerland))*100, ".2e")
    delez_slovenia = format((sum(slovar_medalj["Slovenia"])/int(Slovenia))*100, ".2e")
    delezi = [delez_germany, delez_austria, delez_usa, delez_slovenia, delez_switzerland]

    fig3, ax = plt.subplots(num="Bar chart medalje/populacije", figsize=(10,7))
    ax.set_title('Delež doseženih medalj v primerjavi z velikostjo populacije').set_fontweight('bold')
    ax.bar(drzava, delezi, color="green")
    ax.set_ylabel("Delež [%]")
    plt.show()
    
#input=================================================================================================================================================================
while True:
    print("==================================================================")
    print("ŽENSKO ALPSKO SMUČANJE NA OLIMPIJSKIH IGRAH 2014 V SOČIJU")
    print("Kaj vas zanima?")
    print("1. Rezultati posamezne tekmovalke")
    print("2. Prikaz rezultatov in povezanost")
    print("3. Graf škatel z brki")
    print("4. Stolpični diagram doseženih medalj posamezne države")
    print("5. Stolpični diagram deležov doseženih medalj posamezne populacije")
    print("6. Zaustavitev programa")
    odgovor = input("Prosim vpišite število vaše izbire: ")
    if odgovor == "1":
        ime = input("Vpišite ime tekmovalke v obliki 'Tina Maze': ")
        if ime not in vse_tekmovalke:
            print("\n")
            print("Prosim vpišite ime v veljavni obliki, pazite na velike začetnice!")
            print("\n")
        else:
            print("\n")
            print(vse_tekmovalke[ime])
            print("\n")
    elif odgovor == "2":
        print("Poglejte si datoteko z imenom 'prikaz_podatkov.txt'.")
    elif odgovor == "3":
        box_plot()
    elif odgovor == "4":
        bar_chart_medalje()
    elif odgovor == "5":
        bar_chart_delezi()
    elif odgovor == "6":
        break
    else:
        print("Vpišite '1', '2', '3', '4', '5' ali '6'!")
    input("Pritisnite enter za nadaljevanje!")
    
