import requests

#Make an API call and store the responses

url = 'https://api.github.com/search/repositories?q=language:python&sort=stars'
headers = {'Accept':'application/vnd.github.v3+json'}
r=requests.get(url, headers=headers)
print(f"status code : {r.status_code}")

#store API response in a variable
response_dict = r.json()
print(f"Total repositories : {response_dict['total_count']}")

#process results
print(response_dict.keys())