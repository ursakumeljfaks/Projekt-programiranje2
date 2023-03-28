#COMBINED SKIING WOMEN
import requests
import re
import matplotlib.pyplot as plt

def kvartili(alfa, tabela):
    """izracuna kvartile"""
    n = len(tabela)-1
    if (n*alfa) == int(n*alfa):
        kvartil = tabela[alfa*n:alfa*n+2]
    else:
        kvartil = [tabela[int(alfa*n)+1]]
    return kvartil

def spremeni_v_sekunde(cas):
    minute, sekunde = cas.split(':')
    total = float(minute)*60 + float(sekunde)
    return total
    

spletna_combined = requests.get('https://en.wikipedia.org/wiki/Alpine_skiing_at_the_2014_Winter_Olympics_–_Women%27s_combined').text
vse_comb = re.findall(r'<td align="left">.*<a href="/wiki/.+" title=".+">(.+)</a>.*</td>', spletna_combined)
imena_comb = vse_comb[::2]
drzava_comb = vse_comb[1::2]

mesta_comb = list(range(1, len(imena_comb)+1))

cas_comb_total = re.findall(r'<td>(2\:*\d\d\.\d\d)</td>', spletna_combined)

#škatla z brki
data = [spremeni_v_sekunde(cas) for cas in cas_comb_total]
plt.boxplot(data)
plt.show()

#sklovar_medalj = {drzava: stevilo medalj za vse discipline}  {drzava : [z, s, b]}
slovar_medalj = {}


for i in range(3):
    drzava = drzava_comb[i]
    if drzava not in slovar_medalj:
        slovar_medalj[drzava] = [0,0,0]
    slovar_medalj[drzava][mesta_comb[i]-1] += 1

print(slovar_medalj)


#DOWNHILL WOMEN
spletna_downhill = requests.get('https://en.wikipedia.org/wiki/Alpine_skiing_at_the_2014_Winter_Olympics_–_Women%27s_downhill').text
imena_dw = re.findall(r'<td align="left"><a href="/wiki/.+" title=".+">(.+)</a></td>', spletna_downhill) #pet manjka marianne kaufmann svicarka
drzava_dw = re.findall(r'<td align="left">.+<a href="/wiki/.+" title=".+ at the 2014 Winter Olympics">(.+)</a></td>', spletna_downhill) #ena switzerland manjka 

mesto2 = list(range(3,43)) #ko popravim za svicarko lahko do len(imena_dw)+1 
mesta_dw = [1, 1] + mesto2

cas_dw1 = re.findall(r'<td>(\d\:\d\d\.\d\d)', spletna_downhill)
dnf_dw= re.findall(r'<td><span data-sort-value="9\:99\.99.+!">(.+)</span></td>', spletna_downhill)
cas_dw = [cas_dw1[0]] + cas_dw1 + dnf_dw

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


#SLALOM WOMEN
spletna_slalom = requests.get('https://en.wikipedia.org/wiki/Alpine_skiing_at_the_2014_Winter_Olympics_–_Women%27s_slalom').text
imena_sl = re.findall(r'<td align="left"><a href="/wiki/.+" title=".+">(.+)</a></td>', spletna_slalom)
drzava_sl = re.findall(r'<td align="left">.+<a href="/wiki/.+" title=".+ at the 2014 Winter Olympics">(.+)</a></td>', spletna_slalom)

mesta_sl = list(range(1,len(imena_sl)+1))

vsi_casi_sl = re.findall(r'<td>(\d*\:*\d\d\.\d\d)</td>', spletna_slalom)
cas_sl_run1 = vsi_casi_sl[::3]
cas_sl_run2 = vsi_casi_sl[1::3]
cas_sl_total = vsi_casi_sl[2::3]


#SUPER-G WOMEN
spletna_superg = requests.get('https://en.wikipedia.org/wiki/Alpine_skiing_at_the_2014_Winter_Olympics_–_Women%27s_super-G').text
imena_sg = re.findall(r'<td align="left"><a href="/wiki/.+" title=".+">(.+)</a></td>', spletna_superg)
drzava_sg = re.findall(r'<td align="left">.+<a href="/wiki/.+" title=".+ at the 2014 Winter Olympics">(.+)</a></td>', spletna_superg)

mesta_sg = list(range(1,11)) + [11, 11] + list(range(13,len(imena_sg)+1))

vsi_casi = re.findall(r'<td>(\d*\:*\d\d\.\d\d)</td>', spletna_superg)
dnf_sg= re.findall(r'<td>(\w\w\w)</td>', spletna_superg)
vsi_casi_sg = vsi_casi[:11] + ["".join(list(vsi_casi[10]))] + vsi_casi[11:] + dnf_sg




