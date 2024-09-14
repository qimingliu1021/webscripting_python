import requests
import json

url = "https://textileframe.en.alibaba.com/event/app/alisite/render.htm"

headers = {
  "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
  "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"
}

data = {
  "bizId": "-1000032",
  "language": "en_US",
  "envMode": "product",
  "hostToken": "V1xtLCFHyTZ70ECzught2qfjSyH6gp/ociY6tlbMXryHPir8Bq6N/UU/6D9gAuPCHwT8PEkl/qwW/jaLbIKYYghQ==",
  "siteId": "5009253001",
  "pageId": "5127243001",
  "esiteSubDomain": "https://textileframe.en.alibaba.com",
  "renderType": "module",
  "clientType": "PC",
  "moduleIds": "8941320006"
}

cookies = {
    "acs_usuc_t": "acs_rt=da7b44e36be049e2a86d6498c2c439ab",
    "ali_apache_id": "33.1.238.182.171806474980.845282.9",
    "c_csrf": "b8cf35b8-6747-405f-af61-c42f453ad810",
    "cna": "boTuHqJ1ljQCAdilX7MhXRZR",
    "cookie2": "ab2443371cab3ffa6be20fdd84228cf3",
    "icbu_s_tag": "9_11",
    "isg": "BDo6VnapCFeewoQ-4s2VJ6jxiWZc677FEtdUC0Qzdk2XN9txLHlz1ZkEh1vrvDZd",
    "JSESSIONID": "94F986A518B257426263610A5816B85E",
    "NWG": "NNW",
    "tfstk": "fI_S30qwd9Q2OzISNvF2cZuFsIYhP9awJXOds63r9ULJ921l6_8UZWxpRtW6vg5F9eNCU9Putufpd962nMPuEpWBv_JVL25PLbjcQ13PzuYERU8HJRya7PllZe8p9mCSjLfAiBKRTPcCZ_YniRya7P5oAvdkk9LdpECv9CYKv03LGEdw9e3Jv4nxHKvvpepJvnUv6CO-233LGspD9epp_SEkgX9cNSpgTrT_AzI6h231nQTJqPvjJf7XNAJOwm3KJZOW2wrrb6fkJgCPhhS7C4sAwTs9XaUij3CRFGKOyzMM3hjPeAJ1yuiIGh0pG0VbGDmHaPjlWOSM30xJiIlLGSiZr3dDGeVbGDmH2IA4jSNjb4f..",
    "ug_se_c": "organic_1726167979544",
    "xlly_s": "1",
    "xman_f": "2UZq+F+OGOCKSp5ZhVuhiTCblpFVBG3rR3V5GsW21JC/1WwwXOdu3QoyYrrlS/k8UvwngVAN+XAGqPxUrXTBLsvIEY1Hxps7HsivsrJl3cZDvBR17K7OeA==",
    "xman_t": "jc4f++8ohlgdiVewdtiz39PeiAmo8ikffUffrVHn75DlA12Gn08yh+5wnFhET2Cf",
    "xman_us_f": "x_l=0"
}

# Send the POST request and get the response
response = requests.post(url, headers=headers, data=data, cookies=cookies)

print(response)
print(response.text)

# # Parse the JSON response
# json_data = json.loads(response.text)

# # Access the data
# profile_data = json_data.get('data', {}).get('8941320006', {}).get('data', {})

# # For example, extracting floor space
# floor_space = profile_data.get('authFactoryAreaSize', {}).get('value', 'N/A')

# # Check if authProfiles exists and is not empty
# auth_profiles = profile_data.get('authProfiles', [])
# if len(auth_profiles) > 0:
#     # Extract data from the first profile if available
#     company_year_established = auth_profiles[0].get('value', {}).get('companyYearEstablished', 'N/A')
#     years_in_industry = auth_profiles[0].get('value', {}).get('companyIndustryExperience', 'N/A')
# else:
#     company_year_established = 'N/A'
#     years_in_industry = 'N/A'

# # Extract data from the second profile if available
# if len(auth_profiles) > 1:
#     patents = auth_profiles[1].get('value', {}).get('patentsSize', 'N/A')
# else:
#     patents = 'N/A'

# # Output the extracted data
# print(f"Floor Space: {floor_space}")
# print(f"Company Year Established: {company_year_established}")
# print(f"Years in Industry: {years_in_industry}")
# print(f"Patents: {patents}")
