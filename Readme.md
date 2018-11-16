# Immospider
Immospider is a python program that crawls the Immoscout24 website. You can also use it to 
immediately receive an email when new apartments are available at the Immoscout24 website. 
It is based on ideas from <http://mfcabrera.com/data_science/2015/01/17/ichbineinberliner.html> 
and <https://github.com/balzer82/immoscraper> .

## Installation

Immospider is using the popular python framework <https://scrapy.org/> . For installation you need Python 3. Then you can 
clone this repository and install the requirements via

    pipenv install
   
This should install all necessary packages for you. 

## Simple scraping
Let's assume you want to move to Berlin. You are searching for a flat with 2-3 rooms bigger than 60m^2 flat which should not be 
more expensive than 1000 Euro. You must enter these requirements in Immoscout24 website and search. If you search for 
whole Berlin you probably will find more than 500 results. As next step copy the url of your Immoscout search, because 
Immospider will use it. For the example given here the url is 
<https://www.immobilienscout24.de/Suche/S-T/Wohnung-Miete/Berlin/Berlin/-/2,50-/60,00-/EURO--1000,00> . 
With this information you can now start Immospider like

    scrapy crawl immoscout -o apartments.csv -a url=https://www.immobilienscout24.de/Suche/S-T/Wohnung-Miete/Berlin/Berlin/-/2,50-/60,00-/EURO--1000,00  -L INFO

You should be able to scrape all results within 30 seconds. The results will be stored as CSV file
`apartments.csv`.

## Scraping at regular intervals with email alarm

### Prerequisites

- Docker
- Account at SendGrid (for sending out email)

### Configuration
Make a copy of `config.tmpl` and rename it to `config`. Edit `config` and 
file out the following environment variables: 

    URL=<your immoscout search url>
    FROM=<from email address>
    TO=<to email address>
    SENDGRID_API_KEY=<your sendgrid API key>

By default Immospider is configured to run every 10 minutes. To change it edit the
file `yacrontab.yaml` and edit the line

    schedule: "*/10 * * * *"
    
### Usage
To create the docker container and run it with your configuration do

    $ sh run_docker.sh
    
This will create a docker container from the `Dockerfile`, install the dependencies
and Immospider into the container and run it with your configuration. It will scrape
the Immoscout24 in regular intervals, store the results and will send out an email
when it detects new results it hasn't seen before. Neat, isn't it?         

## Computing travel times
Finding a good flat which is near to your work place and is also near to e.g. the kindergarden/school of your kids, your
 favorite park etc. can be very difficult. Unfortunately the existing search engines in Germany for apartments like 
 Immoscout, Immowelt, Immonet don't support computing the travel time for an apartment to several destinations. Here I 
 want to show you how to use Immospider to do that.

You need an API key for the googlemaps API, if you want to compute travel times to several destinations.
You should follow the instructions at <https://github.com/googlemaps/google-maps-services-python#api-keys> to get 
your API key.

Let's assume you want to move to Berlin. You will work at some fancy startup near Alexanderplatz but your partner likes 
to go shopping at the KaDeWe. And you are searching for a flat with 2-3 rooms bigger than 60m^2 flat which should not be 
more expensive than 1000 Euro. You must enter these requirements in Immoscout24 website and search. If you search for 
whole Berlin you probably will find more than 500 results. As next step copy the url of your Immoscout search, because 
Immospider will use it. For the example given here the url is 
<https://www.immobilienscout24.de/Suche/S-T/Wohnung-Miete/Berlin/Berlin/-/2,50-/60,00-/EURO--1000,00> . 
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


## Data Science
How one can analyze the search results you can see in several jupyter 
notebooks 
- [ImmoAnalyze.ipynb](https://nbviewer.jupyter.org/github/asmaier/ImmoSpider/blob/master/immoscience/ImmoAnalyze.ipynb) .
- [ImmoPredict.ipynb](https://nbviewer.jupyter.org/github/asmaier/ImmoSpider/blob/master/immoscience/ImmoPredict.ipynb) .
- [ApartmentsPredict.ipynb](https://nbviewer.jupyter.org/github/asmaier/ImmoSpider/blob/master/immoscience/ApartmentsPredict.ipynb) .
- [ImmoPredictHouses.ipynb](https://nbviewer.jupyter.org/github/asmaier/ImmoSpider/blob/master/immoscience/ImmoPredictHouses.ipynb) .



