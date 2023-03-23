#COMBINED SKIING WOMEN

import requests
import re

spletna_combined = requests.get('https://en.wikipedia.org/wiki/Alpine_skiing_at_the_2014_Winter_Olympics_–_Women%27s_combined').text
imena_comb = re.findall(r'<td align="left"><a href="/wiki/.+" title=".+">(.+)</a></td>', spletna_combined)
drzava_comb = re.findall(r'<td align="left">.+<a href="/wiki/.+" title=".+ at the 2014 Winter Olympics">(.+)</a></td>', spletna_combined)

mesto_dnf = re.findall(r'<td><span data-sort-value="(\d+)" style="display:none;"></span></td>', spletna_combined)
mesto1 = re.findall(r'<td><span data-sort-value="(\d+).+!">.+</span></td>', spletna_combined)
mesta_comb = [int(i) for i in mesto1[:9]] + list(range(10,23)) + [int(i) for i in mesto_dnf]

cas_comb1 = re.findall(r'<td>(\d\:\d\d\.\d\d)', spletna_combined)
dnf_comb = re.findall(r'<td><span data-sort-value="9\:99\.99.+!">(.+)</span></td>', spletna_combined)
cas_comb = cas_comb1 + dnf_comb


#DOWNHILL WOMEN
spletna_downhill = requests.get('https://en.wikipedia.org/wiki/Alpine_skiing_at_the_2014_Winter_Olympics_–_Women%27s_downhill').text
imena_dw = re.findall(r'<td align="left"><a href="/wiki/.+" title=".+">(.+)</a></td>', spletna_downhill)
drzava_dw = re.findall(r'<td align="left">.+<a href="/wiki/.+" title=".+ at the 2014 Winter Olympics">(.+)</a></td>', spletna_downhill) #ena switzerland manjka 

mesto2 = list(range(3,43))
mesta_dw = [1, 1] + mesto2

cas_dw1 = re.findall(r'<td>(\d\:\d\d\.\d\d)', spletna_downhill)
dnf_dw= re.findall(r'<td><span data-sort-value="9\:99\.99.+!">(.+)</span></td>', spletna_downhill)
cas_dw = [cas_dw1[0]] + cas_dw1 + dnf_dw


#GIANT SLALOM WOMEN
spletna_giant_slalom = requests.get('https://en.wikipedia.org/wiki/Alpine_skiing_at_the_2014_Winter_Olympics_–_Women%27s_giant_slalom').text
imena_gs = re.findall(r'<td align="left"><a href="/wiki/.+" title=".+">(.+)</a></td>', spletna_giant_slalom)
drzava_gs = re.findall(r'<td align="left">.+<a href="/wiki/.+" title=".+ at the 2014 Winter Olympics">(.+)</a></td>', spletna_giant_slalom)

mesto_prej_gs = re.findall(r'<td><span data-sort-value="(\d+).+!">.+</span></td>', spletna_giant_slalom)
mesta_gs = [int(i) for i in mesto_prej_gs] + list(range(10,91))

vsi_casi_gs = re.findall(r'<td>(\d\:\d\d\.\d\d)</td>', spletna_giant_slalom)
cas_gs_run1 = vsi_casi_gs[::3]
cas_gs_run2 = vsi_casi_gs[1::3]
cas_gs_total = vsi_casi_gs[2::3]


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




