# Euro COVID: mapping rate of infection in european regions

This project displays the 14-day notification rate of newly reported COVID-19 cases per 100,000 population by subnational region.

Some regions are updated daily, others are updated weekly, on Wednesdays. Hovering on each region shows the numeric data, along with the name of the region, country and update date for the data.

![user interface](https://github.com/pepicello/eurocovid/blob/master/ui.png?raw=true)

## Data sources

The 14-day notification rate of new cases data is sourced from the European Centre for Disease Prevention and Control (ECDC). They, in turn, outsorce the data from various sources, more details [here](https://www.ecdc.europa.eu/en/covid-19/data-collection).

The map is created matching the [NUTS](https://en.wikipedia.org/wiki/Nomenclature_of_Territorial_Units_for_Statistics) codes for each region from ECDC to the geoJson from [Eurostat](https://ec.europa.eu/eurostat/web/gisco/geodata/reference-data/administrative-units-statistical-units/nuts).

## Caveats

### How to interpret the data
Data never represents the ground truth and its quality is based on how much effort is spent in creating and curating the dataset from the sources.

For COVID-19 data, it is good to keep in mind that it is heavily affected by the local testing strategy, laboratory capacity and the effectiveness of surveillance systems. This visualization aims to break country boundaries and show regional data at a glance. Yet, the data is best comparable within each country, in order to avoid comparing data collected with different testing and reporting strategies. Comparing the epidemiological situation between countries should not be based purely on this data.

Any change in the testing strategy over time will inevitably cause a change in the meaning of the data. More extensive testing will lead to more cases being detected, and vice-versa. Using different tests with different efficacies will also cause similar changes.

The 14-day notification rate of new COVID-19 cases should be used in combination with other factors including testing policies, number of tests performed, test positivity, excess mortality and rates of hospital and Intensive Care Unit (ICU) admissions, when analysing the epidemiological situation in a country. Most of these indicators are presented for EU/EEA Member States and the UK in the Country Overview report.

Even when using several indicators in combination, comparisons between countries should be done with caution and relevant epidemiological expertise.

**Note:** This paragraph contains extracts from the [ECDC variable dictionary and disclaimer](https://www.ecdc.europa.eu/sites/default/files/documents/2020-08-12_Variable_Dictionary_and_Disclaimer_subnational_weekly_data_0.pdf)

### NUTS codes

Not all countries and regions are represented in this map. This might be due to several reasons:
  - Data was not available in the ECDC database
  - The *NUTS* code for a region was not matched with the geoJson sourced from the Eurostat website

Among the list of regions which *NUTS* code could not be matched, there are various reasons for the mismatch.
This is the list of regions which could not be matched with the geoJson from the Eurostat website are were discarded:
  - Greenland (Denmark): GL
  - Höfuðborgarsvæði (Iceland): ISG31
  - Vesturland (Iceland): ISG32
  - Vestfirðir (Iceland): ISG33
  - Norðurland Vestra (Iceland): ISG34
  - Norðurland Eystra (Iceland): ISG35
  - Austurland (Iceland): ISG36
  - Suðurland (Iceland): ISG37
  - Suðurnes (Iceland): ISG39  
  - Isle Of Man (United Kingdom): IM
  - Ayrshire And Arran (United Kingdom): S08000015
  - Borders (United Kingdom): S08000016
  - Dumfries And Galloway (United Kingdom): S08000017
  - Forth Valley (United Kingdom): S08000019
  - Grampian (United Kingdom): S08000020
  - Highland (United Kingdom): S08000022
  - Lothian (United Kingdom): S08000024
  - Orkney (United Kingdom): S08000025
  - Shetland (United Kingdom): S08000026
  - Western Isles (United Kingdom): S08000028
  - Fife (United Kingdom): S08000029
  - Tayside (United Kingdom): S08000030
  - Greater Glasgow And Clyde (United Kingdom): S08000031
  - Lanarkshire (United Kingdom): S08000032
  - Betsi Cadwaladr (United Kingdom): W11000023
  - Powys (United Kingdom): W11000024
  - Hywel Dda (United Kingdom): W11000025
  - Abertawe Bro Morgannwg (United Kingdom): W11000026
  - Cwm Taf (United Kingdom): W11000027
  - Aneurin Bevan (United Kingdom): W11000028
  - Cardiff And Vale (United Kingdom): W11000029  

Some regions were manually matched, but other that have recently changed boundaries or name were mismatched with the version of the geoJson used from Eurostat, and were discarded. Ideally these need to be re-mapped with a different geoJson:
  - Viken (Norway): NOG330
  - Innlandet (Norway): NOG334
  - Vestfold Og Telemark (Norway): NOG338
  - Agder (Norway): NOG342
  - Vestland (Norway): NOG346
  - Troms Og Finnmark (Norway): NOG354

Some *NUTS* codes could not be matched and had a duplicated region name in the data. The matched *NUTS* codes were kept and the rest, listed below, were discarded:
  - Nordwestmecklenburg (Germany): DE80E

For the regions below, the *NUTS* code was modified as seen in `nuts_mapping.yml` to match it with the Eurostat website:
  - Sofia (Bulgaria): BG412X
  - Mazowiecki Regionalny (Poland): PL92X

The *NUTS* code for certain regions was duplicated at different levels of granularity. The highest level of granularity which could be matched with the Eurostat data was picked, while the rest were discarded:
  - Harju Maakond (Estonia): EEG11212
  - Hiiu Maakond (Estonia): EEG11213
  - Ida-Viru Maakond (Estonia): EEG11214
  - Järva Maakond (Estonia): EEG11215
  - Jõgeva Maakond (Estonia): EEG11216
  - Lääne-Viru Maakond (Estonia): EEG11217
  - Lääne Maakond (Estonia): EEG11218
  - Pärnu Maakond (Estonia): EEG11219
  - Põlva Maakond (Estonia): EEG11220
  - Rapla Maakond (Estonia): EEG11221
  - Saare Maakond (Estonia): EEG11222
  - Tartu Maakond (Estonia): EEG11223
  - Valga Maakond (Estonia): EEG11224
  - Viljandi Maakond (Estonia): EEG11225
  - Võru Maakond (Estonia): EEG11226
  - Ave (Portugal): PT113
  - Douro (Portugal): PT117
  - Médio Tejo (Portugal): PT16C
  - Alto Alentejo (Portugal): PT182
  - Alentejo Central (Portugal): PT183
  - Alentejo (Portugal): PTG301
  - Algarve (Portugal): PTG302
  - Regiao Autonoma Dos Acores (Portugal): PTG303
  - Centro (Portugal): PTG304
  - Area Metropolitana De Lisboa (Portugal): PTG305
  - Regiao Autonoma Da Madeira (Portugal): PTG306
  - Norte (Portugal): PTG307

## Contribute

PRs to improve any aspect of the repository are welcome. These include but are not limited to:
  - Expand countries and regions, even outside of the european continent
  - Merge with other sources of more granular data
  - Fix bugs or any of the issues in the caveats section above
  - Implement history (currently only most recent data is shown)
  - Improve UI
  - Improve documentation

The codebase was build over a day, with a focus to deliver a working app quickly, and it has a lot of areas where it can be improved.

## Development

### Dependencies

The following packages are required to run this web-app locally: pandas for data handling, geojson for loading region boundaries, dash/plotly for building the chart and app, and loguru for logging. A full list of dependencies is in `requirements.txt`.

### Web implementation

The app runs locally on localhost, but can also be implemented online.
