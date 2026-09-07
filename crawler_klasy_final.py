"""
Rental Scraper - moduł pobierający dane

Autor: Julia Kowalczyk

Licencja: MIT
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import deep_translator
from pathlib import Path


class ApartmentOffer:
    """Klasa przechowuje informacje o jednym ogłoszeniu."""

    def __init__(self, offer_link,
                 offer_city, offer_street,
                 offer_price, apartment_type,
                 offer_rooms, offer_surface,
                 offer_furnished,
                 offer_description, offer_description_en,
                 near_school, near_hospital,
                 near_public_transport, near_services,
                 photos):
        """Tworzy obiekt zawierający dane jednego ogłoszenia."""

        self.offer_link = offer_link
        self.offer_city = offer_city
        self.offer_street = offer_street
        self.offer_price = offer_price
        self.offer_apartment_type = apartment_type
        self.offer_rooms = offer_rooms
        self.offer_surface = offer_surface
        self.offer_furnished = offer_furnished
        self.offer_description = offer_description
        self.offer_description_en = offer_description_en
        self.near_school = near_school
        self.near_hospital = near_hospital
        self.near_public_transport = near_public_transport
        self.near_services = near_services
        self.photos = photos

    def to_dict(self):
        """Zamienia dane ogłoszenia na słownik."""

        return {
            "link": self.offer_link,
            "city": self.offer_city,
            "street": self.offer_street,
            "price": self.offer_price,
            "type": self.offer_apartment_type,
            "rooms": self.offer_rooms,
            "surface": self.offer_surface,
            "furnished": self.offer_furnished,
            "description": self.offer_description,
            "description_eng": self.offer_description_en,
            "near_school": self.near_school,
            "near_hospital": self.near_hospital,
            "near_public_transport": self.near_public_transport,
            "near_services": self.near_services,
            "photos": self.photos
        }


class RentalScraper:
    """Klasa odpowiada za pobieranie danych o mieszkaniach."""

    def __init__(self):
        """Tworzy scraper i ustawia adres strony."""

        self.base_url = "https://directwonen.nl/huurwoningen-huren/nederland?pageno="
        self.offers_list = []

    def get_offers(self, start_page, end_page):  # 90 stron
        """Pobiera linki do ofert z podanego zakresu stron."""

        a = Path("offers_list.txt")
        if a.exists():
            self.load_offers()
            return self.offers_list

        for i in range(start_page, end_page + 1):
            print(f"Processing page with offers no. {i}")
            res = requests.get(f"{self.base_url}{i}")
            offers = self.process_page(res.content)
            self.offers_list.extend(offers)

        return self.offers_list

    def process_page(self, html):
        """Przetwarza stronę i wyszukuje linki do ofert."""

        soup = BeautifulSoup(html, "html.parser")

        tiles = soup.find_all(class_="tile")
        offers = []
        for tile in tiles:
            if (tile.find_all(class_="smart-only") == []
                    and tile.find_all(class_="upsell-advert") == []):
                a = tile.find("a")
                href = a.get("href")
                offers.append(href)

        return offers

    def save_offers(self, filename="offers_list.txt"):
        """Zapisuje listę ofert do pliku tekstowego."""

        with open(filename, "w", encoding="utf-8") as f:
            f.write("\n".join(self.offers_list))

    def load_offers(self, filename="offers_list.txt"):
        """Wczytuje listę ofert z pliku tekstowego."""

        with open(filename, "r", encoding="utf-8") as f:
            self.offers_list = [line.strip() for line in f]

    def address(self, soup):
        """Pobiera ulicę i miasto z ogłoszenia."""

        offer_address = soup.find("div", class_="apartment-title")
        offer_address = offer_address.find("font", class_="apartment-header")
        offer_address = offer_address.get_text(strip=True)
        offer_address = " ".join(offer_address.split()[3:])
        offer_address = offer_address.split(",")
        offer_street = offer_address[0]
        offer_city = offer_address[1].strip()

        return offer_street, offer_city

    def price(self, soup):
        """Pobiera cenę mieszkania z ogłoszenia."""

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

        return offer_price

    def apartment_type(self, soup):
        """Pobiera typ mieszkania z ogłoszenia."""

        offer_type = soup.find("div", class_="advert-appartment")
        offer_type = offer_type.get("title")
        return offer_type

    def rooms(self, soup):
        """Pobiera liczbę pokoi w mieszkaniu."""

        offer_rooms = soup.find("div", class_="room-no")
        offer_rooms = offer_rooms.text.strip()
        offer_rooms = float(offer_rooms.replace("+", ""))
        return offer_rooms

    def surface(self, soup):
        """Pobiera powierzchnię mieszkania."""

        offer_surface = soup.find("div", class_="advert-surface")
        offer_surface = offer_surface.find("span")
        offer_surface = offer_surface.get_text()
        offer_surface = offer_surface.split()
        offer_surface = float(offer_surface[0])

        return offer_surface

    def furnished(self, soup):
        """Sprawdza, czy mieszkanie jest umeblowane."""

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

        return offer_furnished

    def description(self, soup):
        """Pobiera opis mieszkania z ogłoszenia."""

        offer_description = soup.find("div", class_="contentToToggle")

        if offer_description is None:
            return None

        paragraphs = offer_description.find_all("p")

        if paragraphs:
            texts = [p.get_text(" ", strip=True) for p in paragraphs]
            result = " ".join(texts).strip()
            return result if result else None

        result = offer_description.get_text(" ", strip=True)
        return result if result else None

    def translate_text(self, text, chunk_size=4999):
        """Tłumaczy opis mieszkania na język angielski."""

        if not isinstance(text, str) or not text.strip():
            return None

        translator = deep_translator.GoogleTranslator(source="auto", target="en")
        translated_chunks = []

        for i in range(0, len(text), chunk_size):
            chunk = text[i:i + chunk_size].strip()

            if not chunk:
                continue

            try:
                translated_chunk = translator.translate(chunk)
                if translated_chunk and translated_chunk.strip():
                    translated_chunks.append(translated_chunk)
                else:
                    translated_chunks.append(chunk)
            except Exception as e:
                print(f"Błąd tłumaczenia fragmentu: {e}")
                translated_chunks.append(chunk)

        result = " ".join(translated_chunks).strip()
        return result if result else text

    def school(self, offer_description_en):
        """Sprawdza, czy w opisie znajduje się informacja o szkole."""

        if not offer_description_en:
            return 0
        description = offer_description_en.lower()
        school = ["school", "kindergarten", "daycare", "university", "college"]
        near_school = int(any(word in description for word in school))
        return near_school

    def hospital(self, offer_description_en):
        """Sprawdza, czy w opisie znajduje się informacja o szpitalu."""

        if not offer_description_en:
            return 0
        description = offer_description_en.lower()
        hospital = ["doctor", "hospital", "clinic", "medical"]
        near_hospital = int(any(word in description for word in hospital))
        return near_hospital

    def public_transport(self, offer_description_en):
        """Sprawdza, czy w opisie znajduje się informacja o transporcie publicznym."""

        if not offer_description_en:
            return 0
        description = offer_description_en.lower()
        public_transport = ["tram", "bus", "metro", "train", "station", "public transport"]
        near_public_transport = int(any(word in description for word in public_transport))
        return near_public_transport

    def services(self, offer_description_en):
        """Sprawdza, czy w opisie znajduje się informacja o usługach."""

        if not offer_description_en:
            return 0
        description = offer_description_en.lower()
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
        near_services = int(any(word in description for word in services))
        return near_services

    def photos(self, soup):
        """Pobiera zdjęcia z ogłoszenia."""

        pic_list = []
        picture = soup.find("div", class_="main-PhotoModal-content")

        """Jeśli ogłoszenie nie ma zdjęć, funkcja zwraca None."""

        if picture is None:
            return None

        picture_div = picture.find_all("div", class_="mySlides click-zoom")

        for div in picture_div[:5]:
            img = div.find("img")
            if img and img.get("src"):
                pic_list.append(img.get("src"))
        return pic_list if pic_list else None

    def extract_offer(self, soup, offer_link):
        """Pobiera wszystkie informacje z jednego ogłoszenia."""

        offer_street, offer_city = self.address(soup)
        offer_price = self.price(soup)
        apartment_type = self.apartment_type(soup)
        offer_rooms = self.rooms(soup)
        offer_surface = self.surface(soup)
        offer_furnished = self.furnished(soup)
        offer_description = self.description(soup)
        offer_description_en = self.translate_text(offer_description)
        near_school = self.school(offer_description_en)
        near_hospital = self.hospital(offer_description_en)
        near_public_transport = self.public_transport(offer_description_en)
        near_services = self.services(offer_description_en)
        pic_list = self.photos(soup)

        offer = ApartmentOffer(offer_link=offer_link,
                               offer_street=offer_street,
                               offer_city=offer_city,
                               offer_price=offer_price,
                               apartment_type=apartment_type,
                               offer_rooms=offer_rooms,
                               offer_surface=offer_surface,
                               offer_furnished=offer_furnished,
                               offer_description=offer_description,
                               offer_description_en=offer_description_en,
                               near_school=near_school,
                               near_hospital=near_hospital,
                               near_public_transport=near_public_transport,
                               near_services=near_services,
                               photos=pic_list)

        return offer

    def extract_data(self):
        """Pobiera dane ze wszystkich ofert i zapisuje je do pliku."""

        offers = []

        for idx, offer_link in enumerate(self.offers_list):
            print(f"Processing offer no. {idx}")
            res = requests.get(offer_link)
            soup = BeautifulSoup(res.content, "html.parser")
            offer = self.extract_offer(soup, offer_link)
            offers.append(offer)

        final_df = pd.DataFrame([offer.to_dict() for offer in offers])

        print(final_df.head())

        final_df.to_parquet(
            "offers_df.parquet",
            index=False,
        )

        print(final_df.head())
        print(f"\nPobrano {len(final_df)} ofert.")

        return final_df
