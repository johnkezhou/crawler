
import request
import re
url = "https://www.shanbay.com/bdc/learnings/library/#familiar_tab_p1"
cookie = '__utmt=1; locale=zh-cn; userid=42436729; __utma=183787513.2053541015.1481640632.1483290973.1483364012.24; __utmb=183787513.7.10.1483364012; __utmc=183787513; __utmz=183787513.1481640632.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; csrftoken=nTzCNBzssPv8HgBCPFOGF11LlRfS3cv4; auth_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IndlY2hhdF94N3B2ZGxidiIsImRldmljZSI6MCwiaXNfc3RhZmYiOmZhbHNlLCJpZCI6NDI0MzY3MjksImV4cCI6MTQ4NDIyODQzOX0.D3nzmXAB97PDGbelehdWGaFplQ7QKm5BlBJz-HClpnw; userid=42436729; sessionid=".eJzNVNtyokAQ_ReeE0UERd9EIomJNyJi3N2iBhxhuAzIzCiylX_fRndT2ao87OO-cJnuOXW6T_f5KZ1xECHuMY44lobSIq8PpVzKUV9xks1ukUbHeYft_RlJbLk3XUh3EssDglIPCR55KWLcS_OQUM9HQYLpHjBukJBZoJI3qQUpcEoo4P-UkjMqQ9Z8CdIk52Z9eYuTfeBvTH0eCnqMFmO33r_OkweAIMyj-CwNDyhl-E4qMStyyq5IRZmfCA0a1rsIxwTREC7kBaY3YGOr2kzD6Mly4pFCxUwxFKxZUeiqkBcCV1xKw86dFGG0J1koyhSuRZwXw3b7XLWOUFfeCmg7yxrQ9lZ3mMme3J02OWpvu0wzxwQ6Qfy1uXpekyB78fXKimNU-od1par-zEofdmZwrrcK8VWV-JY7nlj5xV9mdJZZtAidmvjy42uCpkc2x345j3dqWwZ2_9SbFCoWKGwaUEfeeA5HAeEX-H2ESB3lAk5QEGDGPJ6DOBDRq9eeeZhusJxkoxVG44dyoi9HR_pqdw5az3Sfo12Y4-K-v9i75XhfCddJhVGv6Mu9sY1GfJoHycp4nuujwplN1KdurOBRvhSPwZOx01Ix6r3YKWXufSOGoCSn_1IKrgoC2noEOPYVWYYpw9VVHHRCHJX_jTBBLigvmx5f-12U5ERS3Gjw7QeQDoAQxBhlqCC3xYAsSoKEoqyJfBf9Ptbg2RkMpGaeD1B29CHPQHVlbUnipT7tHo8GmwlhT5adY8FwZ2Cf6svK1FJ0eXHJ-eTa4Vv-6FyeNcueWj2xsWORbg-Rq4pe9naq5hEXdLqtnHAtCvMwczcbViWC4HV3axtOw-sLTu93f_Z3yEsBK7fHHJH0urGfdubrcv4rsd4_rEqwhjU4RiINFa0zUHRFByn5pRFLGeiQ-YV7ge94iF0hOIzxhwd9RlMVtdvrK4MPtO7712A302tmhOIKeqtC2s1CG7hP5vnJXVu_T1kryGHoiN-6wbXc68v4fecvoGbZ_pB6_wXqZPqf:1cO2qt:cMY0hhY_q0iLEdT8WZI0E3s-LgQ"'
html = requests.get(url, cookies=each['cookie']).text
print html