# Intro
Finding a good flat which is near to your work place and is also near to e.g. the kindergarden/school of your kids, your
 favorite park etc. can be very difficult. Unfortunately the existing search engines in Germany for apartments like 
 Immoscout, Immowelt, Immonet don't support computing the travel time for an apartment to some destinations. Here I 
 want to show you how to use Immospider to do that.
## Immospider
Immospider is a python program that crawls the Immoscout24 website. It is based on ideas from 
http://mfcabrera.com/data_science/2015/01/17/ichbineinberliner.html and https://github.com/balzer82/immoscraper . But 
it is faster and more flexible. 

### Installation

Immospider is using the popular python framework https://scrapy.org/ . To install you need Python 3. Then you can 
clone this repository and install the requirements via

    pip3 install -r requirements.txt
   
This should install scrapy and the googlemaps package for you. To use it you also need an API key for the googlemaps 
API. You should follow the instructions at https://github.com/googlemaps/google-maps-services-python#api-keys to get 
your API key.

### Usage

Let's assume you want to move to Berlin. You will work at some fancy startup near Alexanderplatz but your partner likes 
to go shopping at the KaDeWe. And you are searching for a flat with 2-3 rooms bigger than 60m^2 flat which should not be 
more expensive than 1000 Euro. You must enter these requirements in Immoscout24 website and search. If you search for 
whole Berlin you probably will find more than 500 results. As next step copy the url of your Immoscout search, because 
Immospider will use it. For the example given here the url is 
https://www.immobilienscout24.de/Suche/S-T/Wohnung-Miete/Berlin/Berlin/-/2,50-/60,00-/EURO--1000,00 . 
With this information you can now start Immospider like

    scrapy crawl immoscout -o apartments.csv -s GM_KEY=<Google Maps API Key> -a url=https://www.immobilienscout24.de/Suche/S-T/Wohnung-Miete/Berlin/Berlin/-/2,50-/60,00-/EURO--1000,00 -a dest="Alexanderplatz, Berlin" -a mode=transit -a dest2="KaDeWe, Berlin" -L INFO
    
The option `-o apartments.csv` specifies the output file. The parameter `-s GM_KEY=<Google Maps API Key>` sets your 
Google maps API key. The argument `dest="Alexanderplatz, Berlin" -a mode=transit` tells Immospider that you want to 
calculate the travel time for each apartment to Alexanderplatz using public transportation mode. The 
argument `dest2="KaDeWe, Berlin"` will additionaly compute the travel time via car (the default mode) to KaDeWe. You 
can have up to three destinations `dest1,dest2,dest3` and specify the mode for each destination `mode1,mode2,mode3`. 
The argument `-a url=...` must hold the search url from Immoscout. The optional parameter `-L INFO` can be added to 
generate more log output.

If you start Immospider with the given parameters here it might run up to 20 minutes, not because the crawler is slow, 
but because the Google Maps API takes some time to compute the travel time for each of the more than 500 apartments. 
If that is too slow for you, you should modify your search on Immoscout (and again copy the new url), so that the 
amount of search results is lower. If your result set is about 50 apartments, Immospider will only need 1-2 minutes 
to compute all the travel times. 
  
# Data Science
How one can analyze the search results and also show them on a map you can see at the jupyter 
notebook [ImmoAnalyze.ipynb](https://nbviewer.jupyter.org/github/asmaier/ImmoSpider/blob/master/ImmoAnalyze.ipynb) .
