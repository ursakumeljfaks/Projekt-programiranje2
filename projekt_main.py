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

# url = 'https://en.wikipedia.org/wiki/Alpine_skiing_at_the_2014_Winter_Olympics_–_Women%27s_combined'
# spletna = requests.get(url).text
# vse = re.findall(r'<td align="left">.*<a href="/wiki/.+" title=".+">(.+)</a>.*</td>', spletna)
# imena = vse[::2]
# drzave = vse[1::2]
# mesta = list(range(1, len(imena)+1))
# casi = re.findall(r'<td>(2\:*\d\d\.\d\d)</td>', spletna)
# dnf = ["dnf" for _ in range(len(imena)-len(casi))]

# slovar_objektov('Combined', imena, drzave, casi+dnf, mesta)

# #škatla z brki
# data.append([spremeni_v_sekunde(cas) for cas in casi])

# slovar_medalj = medalje_za_drzave(slovar_medalj, drzave, mesta)


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


# spletna_downhill = requests.get('https://en.wikipedia.org/wiki/Alpine_skiing_at_the_2014_Winter_Olympics_–_Women%27s_downhill').text
# vse_dw = re.findall(r'<td align="left">.*?<a href="/wiki/.+?" title=".+?">(.+?)</a>', spletna_downhill) # druga svica manjka
# imena_dw = vse_dw[::2]
# drzava_dw = vse_dw[1::2]

# mesto2 = list(range(3,len(imena_dw)+1)) #range(3,43)
# mesta_dw = [1, 1] + mesto2

# cas_dw = re.findall(r'<td.*>(\d\:\d\d\.\d\d)', spletna_downhill) 
# dnf_dw = ["dnf" for _ in range(7)]

# slovar_objektov('Downhill', imena_dw, drzava_dw, cas_dw+dnf_dw, mesta_dw)

# #škatla z brki
# data2 = [spremeni_v_sekunde(cas) for cas in cas_dw]
# slovar_medalj = medalje_za_drzave(slovar_medalj, drzava_dw, mesta_dw)


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

# spletna_giant_slalom = requests.get('https://en.wikipedia.org/wiki/Alpine_skiing_at_the_2014_Winter_Olympics_–_Women%27s_giant_slalom').text
# imena_gs = re.findall(r'<td align="left"><a href="/wiki/.+" title=".+">(.+)</a></td>', spletna_giant_slalom)
# drzava_gs = re.findall(r'<td align="left">.+<a href="/wiki/.+" title=".+ at the 2014 Winter Olympics">(.+)</a></td>', spletna_giant_slalom)

# mesta_gs = list(range(1,15)) + [14] + list(range(16,90))

# cas_gs_total1 = re.findall(r'<td.*>([2|3]\:*\d\d\.\d\d)</td>', spletna_giant_slalom)
# cas_gs_total = (cas_gs_total1[:15] + [cas_gs_total1[14]] + cas_gs_total1[15:])[1:]
# dnf_gs = ["dnf" for _ in range(22)]


# slovar_objektov('Giant-Slalom', imena_gs, drzava_gs, cas_gs_total+dnf_gs, mesta_gs)


#škatla z brki
#data3 = [spremeni_v_sekunde(cas) for cas in cas_gs_total]
#dosežene medalje
#slovar_medalj = medalje_za_drzave(slovar_medalj, drzava_gs, mesta_gs)

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

# spletna_slalom = requests.get('https://en.wikipedia.org/wiki/Alpine_skiing_at_the_2014_Winter_Olympics_–_Women%27s_slalom').text
# imena_sl = re.findall(r'<td align="left"><a href="/wiki/.+" title=".+">(.+)</a></td>', spletna_slalom)
# drzava_sl = re.findall(r'<td align="left">.+<a href="/wiki/.+" title=".+ at the 2014 Winter Olympics">(.+)</a></td>', spletna_slalom)

# mesta_sl = list(range(1,len(imena_sl)+1))

# vsi_casi_sl = re.findall(r'<td>(\d*\:*\d\d\.\d\d)</td>', spletna_slalom)
# #cas_sl_run1 = vsi_casi_sl[::3] narobe
# #cas_sl_run2 = vsi_casi_sl[1::3] narobe
# cas_sl_total = vsi_casi_sl[2::3][:-3] # prou
# dnf_sl = ["dnf" for _ in range(38)]


# slovar_objektov('Slalom', imena_sl, drzava_sl, cas_sl_total+dnf_sl, mesta_sl)

# #škatla z brki
# data4 = [spremeni_v_sekunde(cas) for cas in cas_sl_total]
# slovar_medalj = medalje_za_drzave(slovar_medalj, drzava_sl, mesta_sl)


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




# spletna_superg = requests.get('https://en.wikipedia.org/wiki/Alpine_skiing_at_the_2014_Winter_Olympics_–_Women%27s_super-G').text
# vse_sg = re.findall(r'<td align="left">.*?<a href="/wiki/.+?".*>(.+?)</a>', spletna_superg) 
# imena_sg = vse_sg[::2]
# drzava_sg = vse_sg[1::2]

# mesta_sg = list(range(1,11)) + [11, 11] + list(range(13,len(imena_sg)+1))

# vsi_casi = re.findall(r'<td.*>(\d*\:*\d\d\.\d\d)</td>', spletna_superg)
# dnf_sg= re.findall(r'<td>(\w\w\w)</td>', spletna_superg)
# vsi_casi_sg = vsi_casi[1:12] + [vsi_casi[11]] + vsi_casi[12:] #+dnf_sg

# dnf_sg = ["dnf" for _ in range(19)]


# slovar_objektov('Super-G', imena_sg, drzava_sg, vsi_casi_sg+dnf_sg, mesta_sg)

# #škatla z brki
# data5 = [spremeni_v_sekunde(cas) for cas in vsi_casi_sg]

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
#data = [data1, data2, data3, data4, data5]
plt.rcParams['toolbar'] = 'None'

M = max(data[0] + data[1] + data[2] + data[3] + data[4])
m = min(data[0] + data[1] + data[2] + data[3] + data[4])
razmak = int((M - m)/8)
ves_data = list(range(int(m), int(M), razmak))
casi = [spremeni_v_minute(i) for i in ves_data]
fig = plt.figure(num="Box plot", figsize=(7, 7))

plt.boxplot(data)
#uporabi logaritmsko skalo da ni stisnjeno
plt.semilogy()
plt.minorticks_off()
plt.xticks([1, 2, 3, 4, 5], ['Combined', 'Downhill', "Giant Slalom", "Slalom", "Super-G"])
plt.yticks(ves_data, casi)
plt.ylabel('Časi [min:s]')
plt.title('Škatla z brki za posamezno smučarsko disciplino').set_fontweight('bold')
#fig.savefig("Box plot")
#plt.show()


#bar chart za medalje
#print(medalje_za_drzave(drzava_sg, mesta_sg)) #zato ker manjka svica pri downhill nam da se italijo
#slovar_medalj = medalje_za_drzave(slovar_medalj, drzava_sg, mesta_sg)

drzava = list(slovar_medalj.keys())
zlata, srebrna, bronasta = [], [], []
for tabela in slovar_medalj.values():
    zlata.append(tabela[0])
    srebrna.append(tabela[1])
    bronasta.append(tabela[2])


fig2, ax = plt.subplots(num="Bar chart", figsize=(10,7))

ax.set_title('Skupno število doseženih medalj na Olimpijskih igrah 2014').set_fontweight('bold')
ax.barh(drzava, zlata, label='Zlata', color="gold")
ax.barh(drzava, srebrna, left=zlata, label='Srebrna', color="grey")
ax.barh(drzava, bronasta, left=[i+j for i,j in zip(zlata,srebrna)], label='Bronasta', color="brown")
ax.set_xlabel("Skupno število medalj")
ax.legend()

#fig2.savefig("Bar chart")

#plt.show()

#Primerjava stevila medalj glede na velikost populacije
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
delezi = [delez_germany, delez_austria, delez_usa, delez_switzerland, delez_slovenia]

fig3, ax = plt.subplots(num="Bar chart medalje/populacije", figsize=(10,7))
ax.set_title('Delež doseženih medalj v primerjavi z velikostjo populacije').set_fontweight('bold')
ax.bar(drzava, delezi, color="green")
ax.set_ylabel("Delež [%]")
plt.show()
