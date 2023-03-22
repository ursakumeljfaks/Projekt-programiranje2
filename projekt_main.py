import requests
import re

spletna = requests.get('https://en.wikipedia.org/wiki/Alpine_skiing_at_the_2014_Winter_Olympics_–_Women%27s_combined').text

imena = re.findall(r'<td align="left"><a href="/wiki/.+" title=".+">(.+)</a></td>', spletna)
drzava = re.findall(r'<td align="left">.+<a href="/wiki/.+" title=".+ at the 2014 Winter Olympics">(.+)</a></td>', spletna)

mesto_did_not_finish = re.findall(r'<td><span data-sort-value="(\d+)" style="display:none;"></span></td>', spletna)
mesto_prej = re.findall(r'<td><span data-sort-value=".+!">(.+)</span></td>', spletna)#[3:9]
prvo_drugo_tretje = re.findall(r'<img alt="(.+) place, .+ medalist(s)" src=".+" decoding="async" width="16" height="16" srcset=".+" data-file-width="16" data-file-height="16"/>', mesto_prej[1]) #ne dela

#vsi casi
cas = re.findall(r'<td>(\d\:\d\d\.\d\d)', spletna)
did_not_finish = re.findall(r'<td><span data-sort-value="9\:99\.99.+!">(.+)</span></td>', spletna)
#dodani se DNF=did not finish v seznam vseh casov
cas.extend(did_not_finish)
print(prvo_drugo_tretje)






