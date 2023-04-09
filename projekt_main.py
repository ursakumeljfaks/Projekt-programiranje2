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
    return slovar

slovar_vseh_podatkov = {}
disciplina = ["COMBINED", "DOWNHILL", "GIANT-SLALOM", "SLALOM", "SUPER-G"]
def zberi_podatke(disciplina, imena, drzava, cas, mesta):
    """{ime: drzava, [disciplina, cas, mesto]}"""
    pass
#COMBINED SKIING WOMEN=================================================================================================================

spletna_combined = requests.get('https://en.wikipedia.org/wiki/Alpine_skiing_at_the_2014_Winter_Olympics_–_Women%27s_combined').text
vse_comb = re.findall(r'<td align="left">.*<a href="/wiki/.+" title=".+">(.+)</a>.*</td>', spletna_combined)
imena_comb = vse_comb[::2]
drzava_comb = vse_comb[1::2]
dnf_comb = ["dnf" for _ in range(17)]

mesta_comb = list(range(1, len(imena_comb)+1))

cas_comb_total = re.findall(r'<td>(2\:*\d\d\.\d\d)</td>', spletna_combined)
zapis_comb = [("combined",i,j,k,l) for i,j,k,l in zip(mesta_comb, imena_comb, drzava_comb, cas_comb_total+dnf_comb)]

#škatla z brki
data1 = [spremeni_v_sekunde(cas) for cas in cas_comb_total]

slovar_medalj = medalje_za_drzave(slovar_medalj, drzava_comb, mesta_comb)


#DOWNHILL WOMEN=================================================================================================================================
spletna_downhill = requests.get('https://en.wikipedia.org/wiki/Alpine_skiing_at_the_2014_Winter_Olympics_–_Women%27s_downhill').text
vse_dw = re.findall(r'<td align="left">.*?<a href="/wiki/.+?" title=".+?">(.+?)</a>', spletna_downhill) # druga svica manjka
imena_dw = vse_dw[::2]
drzava_dw = vse_dw[1::2]

mesto2 = list(range(3,len(imena_dw)+1)) #range(3,43)
mesta_dw = [1, 1] + mesto2

cas_dw = re.findall(r'<td.*>(\d\:\d\d\.\d\d)', spletna_downhill) 
dnf_dw = ["dnf" for _ in range(7)]

zapis_dw = [("downhill",i,j,k,l) for i,j,k,l in zip(mesta_dw, imena_dw, drzava_dw, cas_dw+dnf_dw)]

#škatla z brki
data2 = [spremeni_v_sekunde(cas) for cas in cas_dw]
slovar_medalj = medalje_za_drzave(slovar_medalj, drzava_dw, mesta_dw)


#GIANT SLALOM WOMEN===========================================================================================================================================
spletna_giant_slalom = requests.get('https://en.wikipedia.org/wiki/Alpine_skiing_at_the_2014_Winter_Olympics_–_Women%27s_giant_slalom').text
imena_gs = re.findall(r'<td align="left"><a href="/wiki/.+" title=".+">(.+)</a></td>', spletna_giant_slalom)
drzava_gs = re.findall(r'<td align="left">.+<a href="/wiki/.+" title=".+ at the 2014 Winter Olympics">(.+)</a></td>', spletna_giant_slalom)

mesta_gs = list(range(1,15)) + [14] + list(range(16,90))

cas_gs_total1 = re.findall(r'<td.*>([2|3]\:*\d\d\.\d\d)</td>', spletna_giant_slalom)
cas_gs_total = (cas_gs_total1[:15] + [cas_gs_total1[14]] + cas_gs_total1[15:])[1:]
dnf_gs = ["dnf" for _ in range(22)]
zapis_gs = [("giant-slalom",i,j,k,l) for i,j,k,l in zip(mesta_gs, imena_gs, drzava_gs, cas_gs_total+dnf_gs)]

#škatla z brki
data3 = [spremeni_v_sekunde(cas) for cas in cas_gs_total]
#dosežene medalje
slovar_medalj = medalje_za_drzave(slovar_medalj, drzava_gs, mesta_gs)

#SLALOM WOMEN===================================================================================================================================
spletna_slalom = requests.get('https://en.wikipedia.org/wiki/Alpine_skiing_at_the_2014_Winter_Olympics_–_Women%27s_slalom').text
imena_sl = re.findall(r'<td align="left"><a href="/wiki/.+" title=".+">(.+)</a></td>', spletna_slalom)
drzava_sl = re.findall(r'<td align="left">.+<a href="/wiki/.+" title=".+ at the 2014 Winter Olympics">(.+)</a></td>', spletna_slalom)

mesta_sl = list(range(1,len(imena_sl)+1))

vsi_casi_sl = re.findall(r'<td>(\d*\:*\d\d\.\d\d)</td>', spletna_slalom)
#cas_sl_run1 = vsi_casi_sl[::3] narobe
#cas_sl_run2 = vsi_casi_sl[1::3] narobe
cas_sl_total = vsi_casi_sl[2::3][:-3] # prou
dnf_sl = ["dnf" for _ in range(38)]

zapis_sl = [("slalom",i,j,k,l) for i,j,k,l in zip(mesta_sl, imena_sl, drzava_sl, cas_sl_total+dnf_sl)]


#škatla z brki
data4 = [spremeni_v_sekunde(cas) for cas in cas_sl_total]
slovar_medalj = medalje_za_drzave(slovar_medalj, drzava_sl, mesta_sl)


#SUPER-G WOMEN============================================================================================================================
spletna_superg = requests.get('https://en.wikipedia.org/wiki/Alpine_skiing_at_the_2014_Winter_Olympics_–_Women%27s_super-G').text
vse_sg = re.findall(r'<td align="left">.*?<a href="/wiki/.+?".*>(.+?)</a>', spletna_superg) 
imena_sg = vse_sg[::2]
drzava_sg = vse_sg[1::2]

mesta_sg = list(range(1,11)) + [11, 11] + list(range(13,len(imena_sg)+1))

vsi_casi = re.findall(r'<td.*>(\d*\:*\d\d\.\d\d)</td>', spletna_superg)
dnf_sg= re.findall(r'<td>(\w\w\w)</td>', spletna_superg)
vsi_casi_sg = vsi_casi[1:12] + [vsi_casi[11]] + vsi_casi[12:] #+dnf_sg

dnf_sg = ["dnf" for _ in range(19)]

zapis_sg = [("super-g",i,j,k,l) for i,j,k,l in zip(mesta_sg, imena_sg, drzava_sg, vsi_casi_sg+dnf_sg)]

#škatla z brki
data5 = [spremeni_v_sekunde(cas) for cas in vsi_casi_sg]

#===========================================================================================================================================================
skupaj = zapis_comb + zapis_dw + zapis_gs + zapis_sl + zapis_sg
skupen_zapis = {}

discipline = set(nabor[0] for nabor in skupaj)

for nabor in skupaj:
    if len(nabor) >= 5:
        disciplina, mesto, ime, drzava, cas = nabor
        if ime not in skupen_zapis:
            skupen_zapis[ime] = {"drzava": drzava}
            #ustvarim vse discipline in dodam "none"
            for i in discipline:
                skupen_zapis[ime][i] = ["did not participate"]
        #ce vsebuje cas pri tej disciplini -> zamenjaj ta "none" s casom in mestom
        if skupen_zapis[ime][disciplina][0] == "did not participate":
            skupen_zapis[ime][disciplina] = [(cas, mesto)]



#pisanje v datoteko===============================================================================================================================================
with open("prikaz_podatkov.txt", "w") as dat:
    dat.write("IME".ljust(30) + "DRZAVA".ljust(20) + "GIANT-SLALOM".ljust(25) + "SUPER-G".ljust(25) + "SLALOM".ljust(25) + "COMBINED".ljust(25) + "DOWNHILL\n")
    
    #'Marion Bertrand': {'drzava': 'France', 'super-g': ['none'], 'slalom': ['none'], 
    #'giant-slalom': [('-', 79)], 'combined': ['none'], 'downhill': ['none']} 
    for ime, podatki in skupen_zapis.items():
        drzava = podatki["drzava"]
        #ljust(30) = left align za 30 presledkov 
        dat.write(f"{ime.ljust(30)}{drzava.ljust(20)}")
        
        for disciplina in ["giant-slalom", "super-g", "slalom", "combined", "downhill"]:
            if disciplina in podatki:
                casi = podatki[disciplina]
                if len(casi) == 1:
                    dat.write(f"{str(casi[0]).ljust(25)}")
                elif len(casi) == 2:
                    dat.write(f"{str(casi[0]).ljust(25)}")
        
        dat.write("\n")





#===========================================================================================================================================
data = [data1, data2, data3, data4, data5]

M = max(data1 + data2 + data3 + data4 + data5)
m = min(data1 + data2 + data3 + data4 + data5)
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
#fig.savefig("Box plot")
#plt.show()


###drugi nacin, men zgleda prvi bols ker so okrogle cifre na grafu
#vsi_casi = data1+data2+data3+data4+data5
#razmak = (max(vsi_casi) - min(vsi_casi)) / 8
#napisi_sek = [min(vsi_casi)+i*razmak for i in range(9)]
#napisi_min = [spremeni_v_minute(i) for i in napisi_sek[::len(napisi_sek)//5]]
#fig = plt.figure(num="Box plot", figsize=(7, 7))
#plt.boxplot(data)
#plt.semilogy()
#plt.minorticks_off()
#plt.xticks([1, 2, 3, 4, 5], ['Combined', 'Downhill', "Giant Slalom", "Slalom", "Super-G"])
#plt.yticks(napisi_sek, napisi_min)
#plt.show()


#bar chart za medalje
#print(medalje_za_drzave(drzava_sg, mesta_sg)) #zato ker manjka svica pri downhill nam da se italijo
slovar_medalj = medalje_za_drzave(slovar_medalj, drzava_sg, mesta_sg)

drzava = list(slovar_medalj.keys())
zlata, srebrna, bronasta = [], [], []
for tabela in slovar_medalj.values():
    zlata.append(tabela[0])
    srebrna.append(tabela[1])
    bronasta.append(tabela[2])

fig2, ax = plt.subplots(num="Bar chart", figsize=(10,7))

ax.barh(drzava, zlata, label='Zlata', color="gold")
ax.barh(drzava, srebrna, left=zlata, label='Srebrna', color="grey")
ax.barh(drzava, bronasta, left=[i+j for i,j in zip(zlata,srebrna)], label='Bronasta', color="brown")
ax.legend()
#fig2.savefig("Bar chart")

#plt.show()




#dosežene medalje pravilno
#{Germany: [1, 1, 1], Austria: [1, 3, 2], United States: [1, 0, 1], Slovenia: [2, 0, 0], Switzerland: [1, 1, 0]}

