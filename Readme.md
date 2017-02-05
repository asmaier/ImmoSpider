# Usage

   $ scrapy crawl immoscout -o appartments.csv -s GM_KEY=<Google Maps API Key> -a url=https://www.immobilienscout24.de/Suche/S-2/Wohnung-Miete/Berlin/Berlin/Lichterfelde-Steglitz_Nikolassee-Zehlendorf_Dahlem-Zehlendorf_Zehlendorf-Zehlendorf/2,50-/60,00-/EURO--800,00/-/-/ -a dest="Brandenburger Tor, Berlin" -a mode=transit -a dest2="Rathaus Steglitz, Berlin" -L INFO
