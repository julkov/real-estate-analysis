import requests
from bs4 import BeautifulSoup


offers_list = []

for i in range(1, 88):
    res = requests.get(f"https://directwonen.nl/huurwoningen-huren/nederland?pageno={i}")
    soup = BeautifulSoup(res.content, "html.parser")
    # print(soup.prettify())

    tiles = soup.find_all(class_='tile')
    # print(tiles)

    for tile in tiles:
        if tile.find_all(class_="smart-only") == [] and tile.find_all(class_="upsell-advert") == []:
            a = tile.find("a")
            href = a.get("href")
            offers_list.append(href)
            print(href)

print(offers_list)

with open('offers_list_ex.txt', 'w+') as f:
    f.write("\n".join(offers_list))