import unittest
from crawler_klasy import RentalScraper
from bs4 import BeautifulSoup


class TestRentalScraper(unittest.TestCase):
    def test_process_page(self):
        scraper = RentalScraper()
        result = scraper.process_page("""
        <html>
            <body>
                <div class="tile">
                    <a href="url1"></a>
                </div>
                <div class="tile">
                    <a href="url2"></a>
                    <div class="smart-only">
                    </div>
                </div>
            </body>
        </html>
        """)
        assert result == ["url1"]


    def test_address(self):
        scraper = RentalScraper()
        soup = BeautifulSoup( """
                <html>
                    <body>
                        <div class="apartment-title">
                            <font class="apartment-header">Kamer te huur Wolfgang Straat, Amsterdam</font>
                        </div>
                    </body>
                </html>
                """, "html.parser")

        street, city  = scraper.address(soup)
        assert street == "Wolfgang Straat"
        assert city == "Amsterdam"

    def test_price(self):
        scraper = RentalScraper()
        soup = BeautifulSoup( """
            <html>
                <body>
                    <font class="apartment-price">
                        <span> 517 </span>
                    </font>
                </body>
            </html>
            """, "html.parser")

        price = scraper.price(soup)
        assert price == 517

    def test_apartment_type(self):
        scraper = RentalScraper()
        soup = BeautifulSoup( """
            <html>
                <body>
                    <div class="advert-appartment" title="STUDIO-ROOM">
                    </div>
                </body>
            </html>
        """, "html.parser")
        apartment_type = scraper.apartment_type(soup)
        assert apartment_type == "STUDIO-ROOM"

    def test_rooms(self):
        scraper = RentalScraper()
        soup = BeautifulSoup( """
            <html>
                <body>
                    <div class="room-no">2</div>
                </body>
            </html>
        """, "html.parser")
        rooms = scraper.rooms(soup)
        assert rooms == 2

    def test_surface(self):
        scraper = RentalScraper()
        soup = BeautifulSoup( """
            <html>
                <body>
                    <div class="advert-surface">
                        <span> 16 m2</span>
                    </div>
                </body>
            </html>
        """, "html.parser")
        surface = scraper.surface(soup)
        assert surface == float("16")

    def test_furnished(self):
        scraper = RentalScraper()
        soup = BeautifulSoup( """
            <html>
                <body>
                    <div class="advert-furnished">
                        <span> Gemeubileerd </span>
                    </div>
                </body>
            </html>
        """, "html.parser")
        furnished = scraper.furnished(soup)
        assert furnished == "Gemeubileerd"

    def test_description(self):
        scraper = RentalScraper()
        soup = BeautifulSoup( """
            <html>
                <body>
                    <div class="contentToToggle">Great place to rent.</div>
                </body>
            </html>
        """, "html.parser")
        description = scraper.description(soup)
        assert description == "Great place to rent."

    # def test_transtation(self):
    #     scraper = RentalScraper()

    def test_school(self):
        scraper = RentalScraper()
        description = "Close to school."
        near_school = scraper.school(description)
        assert near_school == 1

    def test_hospital(self):
        scraper = RentalScraper()
        description = "Close to hospital."
        hospital = scraper.hospital(description)
        assert hospital == 1

    def test_public_transport(self):
        scraper = RentalScraper()
        description = "Close to public transport."
        public_transport = scraper.public_transport(description)
        assert public_transport == 1

    def test_services(self):
        scraper = RentalScraper()
        description = "Close to the gym."
        services = scraper.services(description)
        assert services == 1

    def test_photos(self):
        scraper = RentalScraper()
        soup = BeautifulSoup( """
            <html>
                <body>
                    <div class="main-PhotoModal-content">
                        <div class="mySlides click-zoom">
                            <img src="https://resources.directwonen.nl/image/">
                        </div>
                    </div>
                </body>
            </html>
        """, "html.parser")
        photos = scraper.photos(soup)
        assert photos == ["https://resources.directwonen.nl/image/"]




