Apartment-Price-By-Zip-Code
12/11/2020
Contact: Kane Hammond at 201306381@panthers.greenville.edu

# Basic Dependencies/Imports

This was written using python 2.7.16. Data for this script is downloaded/imported
from HUD and uszipcode (https://pypi.org/project/uszipcode/). Data download from 
HUD is done via urllib3. This alleviates the need for an account at any specific data repository for use. HUD data represents the 50th percentile of rent values for rental properties based upon number of bedrooms. The information from uszipcode is included for reference. Albeit, the data for rental properties may not match with the HUD data. 

# Purpose

My specific purpose was to utilize this script to aid in assessing rental 
properties by zip code and projected net income required to live in those 
locations. Gross income required to obtain housing at a specific price is based 
upon the concept of spending no more than 30 percent of one's gross income on 
housing. Gross income and net income are estimated via the 30 percent concept and a flat tax rate. The flat overall income tax rate provided in the script is 25 percent. There are links provided within the code to assess state and federal income tax rates if you wish to modify these.

Data returned from this script will provide basic information pertaining to the
50th percentile of property rental prices (HUD Data), as well as demographic 
data pertaining to education and reported salaries (uszipcode). Rental data provided by uszipcode references the number of properties on record per rental price range bracket. As prevously mentioned, this data may not accurately represent what is provided via HUD. It is simply provided for reference. For more information on the uszipcode data, visit the link provided: https://pypi.org/project/uszipcode/ 

# General Use

This is a single script which will pull all data required to conduct the 
analysis. There are no saved outputs. Once the data is downloaded and ready for 
reference, it takes very little time for the results to be provided within the 
command prompt (if that is where you choose to initialize it). Simply run the 
script and provide a five digit zip code for an assessment when asked to do so. 
If the analysis is running for the first time, data from HUD is relatively small 
in file size, taking little time to download. However, the search option chosen for the uszipcode search uses the full dataset they provide. Expect a download of around 450 mb for this. Afterwards, the uszipcode data will be used to reference the HUD data with the given zip code. This reference will be initially based upon county name, state, then city name if applicable. To update the HUD data, simply delete the CSV folder that is written when initiating the file. The script will automatically pull the most recent documentation from HUD for the current year.
