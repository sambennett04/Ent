# Ent

## Overview 

Ent is an intelligent watering system (Hardware + Software) that combines data from an in-ground water content sensor and hyperlocal weather forecast data from the DarkSky API to optimize  water and fertilizer distribution to your garden. 

Ent is deployed in production at Immanuel Presbyterian Church in McLean Virginia. Stop by if you want to see Ent in action!

## Limitations 

As of xxxx the DarkSky API was aquired by Apple, so to use this code you will need a payed subscritption that you can get from this [link](https://developer.apple.com/weatherkit/get-started/) or try one of these alternative [APIs](https://medium.com/@Ari_n/8-weather-api-alternatives-now-that-darksky-is-shutting-down-42a5ac395f93)

The MegaIO board consumes a lot of power which can cause problems if you have a garden that does not get direct sunlight most of the day( This happened to me in the early spring months). I recomend changing to a sense hat which consumes far less energy and simply requires a change of the MegaIO configuration to implement with this software. 

## Hardware 

### Materials
- Mega I/O Board (Sourced from Amazon at this [link](https://www.amazon.com/gp/product/B079N2V8F8/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1))
- Raspberry PI 1 W
- 2 12V Battery (Sourced from Amazon at this [link](https://www.amazon.com/gp/product/B00K8V2Y8W/ref=ppx_yo_dt_b_search_asin_image?ie=UTF8&psc=1))
- Water Content Sensor compatitable with Raspberry Pi (sourced from Amazon at this [link](https://www.amazon.com/Capacitive-Soil-Moisture-Sensor-Electronic/dp/B0B8N69LMX/ref=sr_1_1_sspa?keywords=raspberry+pi+moisture+sensor&qid=1689351716&sr=8-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1) )
- 20A Solar Panel (Sourced from Amazon at this [link](https://www.amazon.com/gp/product/B082XRCVZM/ref=ppx_yo_dt_b_search_asin_image?ie=UTF8&psc=1))
- 7 Gallon Bucket
- Venturi Fertelizer Valve (Sourced from Amazon at this [link](https://www.amazon.com/gp/product/B01M1NKJJ6/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1))
- 12v submersible pump (Sourced froom Amazon at this [link](https://www.amazon.com/gp/product/B06Y2T63PX/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1))
- 12v Brass Valve (Sourced from Amazon at this [link](https://www.amazon.com/gp/product/B07N6246YB/ref=ppx_yo_dt_b_search_asin_image?ie=UTF8&th=1))
- Water Proof Battery Box x2 (Sourced from Amazon at this [link](https://www.amazon.com/gp/product/B001GN6QTE/ref=ppx_yo_dt_b_search_asin_image?ie=UTF8&psc=1))
- Enclosure Junction Box (Sourced from Amazon at this [link](https://www.amazon.com/gp/product/B07J6S2CFH/ref=ppx_yo_dt_b_search_asin_image?ie=UTF8&psc=1))
- Garden Post (I purchased a mailbox post from homedepot)

### Configuration 


## Software
- Need an Azure Cosmos DB Account 
- Need a DarkSky Account 
- Download install.sh from Git Repo
- Run install.sh, which will install all python dependencies and clone repo from GitHub
- Edit configurations: DarkSkyConfiguration to add API key, SystemConfiguration to add a personalilized watering schedule and 

### Excecution 
- You can run this using the following python command or we recommend you set up a run schedule using Cron

```sh

python3 ./Groot.py

```

### Tests
- Run test.sh 

```sh

test.sh

```