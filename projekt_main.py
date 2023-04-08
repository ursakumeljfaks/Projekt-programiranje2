#COMBINED SKIING WOMEN
import requests
import re
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def spremeni_v_sekunde(cas):
    minute, sekunde = cas.split(':')
    total = float(minute)*60 + float(sekunde)
    return total

def spremeni_v_minute(cas):
    minute = cas // 60
    sekunde = cas - minute*60
    return str(minute) + ":" + str(sekunde)

slovar_medalj = {}
def medalje_za_drzave(drzave, mesta):
    """{drzava : [zlata, srebrna, bronasta]} slovar vseh drzav in njihovih dosezkov"""
    for i in range(3):
        drzava = drzave[i]
        if drzava not in slovar_medalj:
            slovar_medalj[drzava] = [0,0,0]
        slovar_medalj[drzava][mesta[i]-1] += 1
    return slovar_medalj

spletna_combined = requests.get('https://en.wikipedia.org/wiki/Alpine_skiing_at_the_2014_Winter_Olympics_–_Women%27s_combined').text
vse_comb = re.findall(r'<td align="left">.*<a href="/wiki/.+" title=".+">(.+)</a>.*</td>', spletna_combined)
imena_comb = vse_comb[::2]
drzava_comb = vse_comb[1::2]

mesta_comb = list(range(1, len(imena_comb)+1))

cas_comb_total = re.findall(r'<td>(2\:*\d\d\.\d\d)</td>', spletna_combined)

#škatla z brki
data1 = [spremeni_v_sekunde(cas) for cas in cas_comb_total]

#sklovar_medalj = {drzava: stevilo medalj za vse discipline}  
slovar_medalj2 = {}

for i in range(3):
    drzava = drzava_comb[i]
    if drzava not in slovar_medalj2:
        slovar_medalj2[drzava] = [0,0,0]
    slovar_medalj2[drzava][mesta_comb[i]-1] += 1

#print(slovar_medalj2)
sl_comb = medalje_za_drzave(drzava_comb, mesta_comb)

#DOWNHILL WOMEN
spletna_downhill = requests.get('https://en.wikipedia.org/wiki/Alpine_skiing_at_the_2014_Winter_Olympics_–_Women%27s_downhill').text
vse_dw = re.findall(r'<td align="left">.*?<a href="/wiki/.+?" title=".+?">(.+?)</a>', spletna_downhill) # druga svica manjka
imena_dw = vse_dw[::2]
drzava_dw = vse_dw[1::2]


mesto2 = list(range(3,len(imena_dw)+1)) #range(3,43)
mesta_dw = [1, 1] + mesto2


cas_dw1 = re.findall(r'<td>(\d\:\d\d\.\d\d)', spletna_downhill)
dnf_dw= re.findall(r'<td><span data-sort-value="9\:99\.99.+!">(.+)</span></td>', spletna_downhill)
cas_dw = [cas_dw1[0]] + cas_dw1 + dnf_dw


#škatla z brki
data2 = [spremeni_v_sekunde(cas) for cas in cas_dw1]
sl_dw = medalje_za_drzave(drzava_dw, mesta_dw)

#GIANT SLALOM WOMEN
spletna_giant_slalom = requests.get('https://en.wikipedia.org/wiki/Alpine_skiing_at_the_2014_Winter_Olympics_–_Women%27s_giant_slalom').text
imena_gs = re.findall(r'<td align="left"><a href="/wiki/.+" title=".+">(.+)</a></td>', spletna_giant_slalom)
drzava_gs = re.findall(r'<td align="left">.+<a href="/wiki/.+" title=".+ at the 2014 Winter Olympics">(.+)</a></td>', spletna_giant_slalom)

mesta_gs = list(range(1,15)) + [14] + list(range(16,90))

#vsi_casi_gs = re.findall(r'<td>(\d\:\d\d\.\d\d)</td>', spletna_giant_slalom)
#cas_gs_run1 = vsi_casi_gs[::3]
#cas_gs_run2 = vsi_casi_gs[1::3]
cas_gs_total1 = re.findall(r'<td.*>([2|3]\:*\d\d\.\d\d)</td>', spletna_giant_slalom)
cas_gs_total = (cas_gs_total1[:15] + [cas_gs_total1[14]] + cas_gs_total1[15:])[1:]

#škatla z brki
data3 = [spremeni_v_sekunde(cas) for cas in cas_gs_total]
#dosežene medalje
sl_gs = medalje_za_drzave(drzava_gs, mesta_gs)

#SLALOM WOMEN
spletna_slalom = requests.get('https://en.wikipedia.org/wiki/Alpine_skiing_at_the_2014_Winter_Olympics_–_Women%27s_slalom').text
imena_sl = re.findall(r'<td align="left"><a href="/wiki/.+" title=".+">(.+)</a></td>', spletna_slalom)
drzava_sl = re.findall(r'<td align="left">.+<a href="/wiki/.+" title=".+ at the 2014 Winter Olympics">(.+)</a></td>', spletna_slalom)

mesta_sl = list(range(1,len(imena_sl)+1))

vsi_casi_sl = re.findall(r'<td>(\d*\:*\d\d\.\d\d)</td>', spletna_slalom)
#cas_sl_run1 = vsi_casi_sl[::3] narobe
#cas_sl_run2 = vsi_casi_sl[1::3] narobe
cas_sl_total = vsi_casi_sl[2::3][:-3] # prou

#škatla z brki
data4 = [spremeni_v_sekunde(cas) for cas in cas_sl_total]
sl_sl = medalje_za_drzave(drzava_sl, mesta_sl)

#SUPER-G WOMEN
spletna_superg = requests.get('https://en.wikipedia.org/wiki/Alpine_skiing_at_the_2014_Winter_Olympics_–_Women%27s_super-G').text
vse_sg = re.findall(r'<td align="left">.*?<a href="/wiki/.+?".*>(.+?)</a>', spletna_superg) 
imena_sg = vse_sg[::2]
drzava_sg = vse_sg[1::2]

mesta_sg = list(range(1,11)) + [11, 11] + list(range(13,len(imena_sg)+1))

vsi_casi = re.findall(r'<td.*>(\d*\:*\d\d\.\d\d)</td>', spletna_superg)
dnf_sg= re.findall(r'<td>(\w\w\w)</td>', spletna_superg)
vsi_casi_sg = vsi_casi[1:12] + [vsi_casi[11]] + vsi_casi[12:] #+dnf_sg

#škatla z brki
data5 = [spremeni_v_sekunde(cas) for cas in vsi_casi_sg]
data = [data1, data2, data3, data4, data5]

M = max(data1 + data2 + data3 + data4 + data5)
m = min(data1 + data2 + data3 + data4 + data5)
razmak = int((M - m)/8)
ves_data = list(range(int(m), int(M), razmak))
casi = [spremeni_v_minute(i) for i in ves_data]


fig = plt.figure(num="Box plot", figsize=(7, 7))

plt.boxplot(data)
#uporabi logaritmsko skalo da ni stisnjeno
#plt.semilogy()
plt.xticks([1, 2, 3, 4, 5], ['Combined', 'Downhill', "Giant Slalom", "Slalom", "Super-G"])
plt.yticks(ves_data, casi)
#fig.savefig("Box plot")
plt.show()


#bar chart za medalje
#print(medalje_za_drzave(drzava_sg, mesta_sg)) #zato ker manjka svica pri downhill nam da se italijo
sl_sg = medalje_za_drzave(drzava_sg, mesta_sg)
#print(sl_sg)
drzava = list(sl_sg.keys())
zlata, srebrna, bronasta = [], [], []
for tabela in sl_sg.values():
    zlata.append(tabela[0])
    srebrna.append(tabela[1])
    bronasta.append(tabela[2])

fig2, ax = plt.subplots(num="Bar chart", figsize=(10,7))

ax.barh(drzava, zlata, label='Zlata', color="gold")
ax.barh(drzava, srebrna, left=zlata, label='Srebrna', color="grey")
ax.barh(drzava, bronasta, left=[i+j for i,j in zip(zlata,srebrna)], label='Bronasta', color="brown")
ax.legend()
#fig2.savefig("Bar chart")

plt.show()




#dosežene medalje pravilno
#{Germany: [1, 1, 1], Austria: [1, 3, 2], United States: [1, 0, 1], Slovenia: [2, 0, 0], Switzerland: [1, 1, 0]}


