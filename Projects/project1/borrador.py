import requests
res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "pEhwApK0Hah2deHLG5Qjyg", "isbns": "9781632168146"})
print(res.json())
