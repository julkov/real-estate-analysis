import requests
from bs4 import BeautifulSoup
import pandas as pd
import deep_translator
import csv


def get_offers(start_page=1, end_page=7):  # 86 stron
    offers_list = []

    for i in range(start_page, end_page + 1):
        res = requests.get(f"https://directwonen.nl/huurwoningen-huren/nederland?pageno={i}")
        soup = BeautifulSoup(res.content, "html.parser")
        # print(soup.prettify())

        tiles = soup.find_all(class_="tile")
        # print(tiles)

        for tile in tiles:
            if (tile.find_all(class_="smart-only") == []
                and tile.find_all(class_="upsell-advert") == []):
                a = tile.find("a")
                href = a.get("href")
                offers_list.append(href)
    # print(offers_list)
    return offers_list

offers = get_offers()

# print(offers)

with open("offers_list_notes.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(offers))

with open('offers_list_notes.txt', 'r') as f:
    offers_list = f.readlines()


def address(soup):
    offer_address = soup.find("div", class_= "apartment-title")
    offer_address = offer_address.find("font", class_="apartment-header")
    offer_address = offer_address.get_text(strip=True)
    offer_address = " ".join(offer_address.split()[3:])
    offer_address = offer_address.split(",")
    offer_street = offer_address[0]
    offer_city = offer_address[1].strip()
    print(offer_street)
    print(offer_city)
    return offer_street, offer_city


def price(soup):
    offer_price = soup.find(class_="apartment-price")

    if offer_price:
        span = offer_price.find("span")
        if span:
            text = span.get_text(strip=True)
            text = text.replace(",", "")
            text = text.replace(".", "")
            offer_price = float(text.split()[0])
        else:
            offer_price = None
    else:
        offer_price = None

    print(offer_price)
    return offer_price


def apartment_type(soup):
    offer_type = soup.find("div", class_= "advert-appartment")
    offer_type = offer_type.get("title")
    print(offer_type)
    return offer_type


def rooms(soup):
    offer_rooms = soup.find("div", class_="room-no")
    offer_rooms = offer_rooms.text.strip()
    offer_rooms = float(offer_rooms.replace("+", ""))
    print(offer_rooms)
    return offer_rooms


def surface(soup):
    offer_surface = soup.find("div", class_= "advert-surface")
    offer_surface = offer_surface.find("span")
    offer_surface = offer_surface.get_text()
    offer_surface = offer_surface.split()
    offer_surface = float(offer_surface[0])
    print(offer_surface)
    return offer_surface


def furnished(soup):
    offer_furnished = soup.find("div", class_="advert-furnished")

    if offer_furnished:
        span = offer_furnished.find("span")
        if span:
            offer_furnished = span.get_text(strip=True)
        else:
            offer_furnished = None

    else:
        offer_unfurnished = soup.find("div", class_="advert-unfurnished")

        if offer_unfurnished:
            span = offer_unfurnished.find("span")
            if span:
                offer_furnished = span.get_text(strip=True)
            else:
                offer_furnished = None
        else:
            offer_furnished = None

    print(offer_furnished)
    return offer_furnished


def description(soup):
    offer_description = soup.find("div", class_="contentToToggle")
    offer_description = offer_description.find_all("p")

    texts = []

    for p in offer_description:
        texts.append(p.get_text(strip=True))

    offer_description = " ".join(texts)

    # print("ORYGINAŁ:")
    # print(offer_description)
    return offer_description

# offer_description = description(soup)

def translate_text(text):
    if isinstance(text, str):
        translator = deep_translator.GoogleTranslator(
            source="auto",
            target="en"
        )
        return translator.translate(text)
    return None


# offer_description_en = translate_text(offer_description)
# print("\nTŁUMACZENIE:")
# print(offer_description_en)


def features(offer_description_en):
    description = offer_description_en.lower()

    school = ["school", "kindergarten", "daycare", "university", "college"]
    hospital = ["doctor", "GP", "hospital", "clinic", "medical"]
    public_transport = ["tram", "bus", "metro", "train", "station"]
    services = [
        "cinema",
        "gym",
        "fitness",
        "sauna",
        "parking",
        "pool",
        "coffee",
        "library",
        "bicycle lane",
        "bicycle shed"
    ]

    near_school = int(any(word in description for word in school))
    near_hospital = int(any(word in description for word in hospital))
    near_public_transport = int(any(word in description for word in public_transport))
    near_services = int(any(word in description for word in services))

    return near_school, near_hospital, near_public_transport, near_services


def photos(soup):
    pic_list = []
    picture = soup.find("div", class_="main-PhotoModal-content")  # tutaj uważać: jeśli ogłoszenie nie ma zdjęć, zwróci None i program się wywali
    picture_div = picture.find_all("div", class_="mySlides click-zoom")
    for div in picture_div:
        img = div.find_all("img")
        pic_list.append(img[0].get("src"))
    print(pic_list)
    return pic_list


def extract_offers(soup, offer_link):

    offer_street, offer_city = address(soup)
    offer_price = price(soup)
    offer_type = apartment_type(soup)
    offer_rooms = rooms(soup)
    offer_surface = surface(soup)
    offer_furnished = furnished(soup)
    offer_description = description(soup)
    offer_description_en = translate_text(offer_description)
    near_school, near_hospital, near_public_transport, near_services = features(
        offer_description_en)
    pic_list = photos(soup)

    offer_details = {
        "link": offer_link,
        "city": offer_city,
        "street": offer_street,
        "price": offer_price,
        "type": offer_type,
        "rooms": offer_rooms,
        "surface (m2)": offer_surface,
        "furnished": offer_furnished,
        "description": offer_description,
        "description_eng": offer_description_en,
        "photos": pic_list,
        "near school": near_school,
        "near hospital": near_hospital,
        "near public_transport": near_public_transport,
        "near services": near_services
    }

    return offer_details

def extract_data(start: int, end: int): #2198

    final_df = []

    for i in range(start, end + 1):

        offer_link = offers_list[i].strip()
        url = offer_link
        res = requests.get(url)
        soup = BeautifulSoup(res.content, "html.parser")
        # print(soup.prettify())
        offer = extract_offers(soup, offer_link)
        final_df.append(offer)

    final_df = pd.DataFrame(final_df)

    final_df.to_csv(
        "offers_notes.csv",
        index=False,
        encoding="utf-8-sig"
    )

    print(final_df.head())
    print(f"\nPobrano {len(final_df)} ofert.")

    return final_df


offers_all = extract_data(0, 10)
print(offers_all)