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
locations. Net income required to obtain housing at a specific price is based 
upon the concept of spending no more than 30 percent of one's net income on 
housing. Gross income is estimated from net income via a flat tax rate. The flat 
overall income tax rate provided in the script is 25 percent. There are links 
provided within the code to assess state and federal income tax rates if you 
wish to modify these.

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

# Example Output:


Type in 5 digit zip code: 80202

LOCATION: Denver County, CO

Rental Data and required income:

  Rental_Size  Price   Gross_Income  Net_Income  Hourly_Rate
0      Studio   1210   64533.333333     48400.0    33.611111
1        1 BR   1367   72906.666667     54680.0    37.972222
2        2 BR   1700   90666.666667     68000.0    47.222222
3        3 BR   2348  125226.666667     93920.0    65.222222
4        4 BR   2701  144053.333333    108040.0    75.027778
*Data Source: HUD (2020)
*Rental prices represent the 50th percentile.


Educational Data:

Total Educational Data Recorded: 8790
Total Higher Educational Data Recorded: 6588
Percent of Records Above High School: 74.948805

                       Education  Total_Records   %_All_Ed %_Higher_Ed
0  Less Than High School Diploma            233   2.650739         nan
1           High School Graduate           1969  22.400455         nan
2             Associate's Degree            513   5.836177     7.78689
3              Bachelor's Degree           3678  41.843003     55.8288
4                Master's Degree           1582  17.997725     24.0134
5     Professional School Degree            664   7.554039     10.0789
6               Doctorate Degree            151   1.717861     2.29205
*Data Source: uszipcode


Salary Data:

       Pay_Bracket  Total_Records  %_Of_Records
0        < $10,000            966     11.618956
1  $10,000-$19,999            783      9.417849
2  $20,000-$29,999            443      5.328362
3  $30,000-$39,999            690      8.299254
4  $40,000-$49,999            855     10.283859
5  $50,000-$64,999           1469     17.668992
6  $65,000-$74,999            426      5.123887
7  $75,000-$99,999           1086     13.062305
8        $100,000+           1596     19.196536
*Data Source: uszipcode


Rental Data:

  Rental_Bracket  Total_Records  %_Of_Records
0         < $200             26      3.886398
1      $200-$299            100     14.947683
2      $300-$499             14      2.092676
3      $500-$749             31      4.633782
4      $750-$999             90     13.452915
5        $1,000+            408     60.986547
*Data Source: uszipcode

