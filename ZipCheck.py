################# Imports
import subprocess
import sys
import os
import os.path
from os import listdir
from os.path import exists
import urllib3
import pandas as pd
import datetime
from datetime import datetime
# import csv

# The HUD data comes in as a xlsx file.
try:
	import xlrd
except:
	subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'xlrd'])
import xlrd

################## uszipcode
# THIS CAN LIVE HERE 
# This import can be used to pull county names based upon input 
# zip code. This can then be related to the HUD data for specific 
# rent approximations in the 50th percentile. The uszipcode import
# also contains rental data. Albeit, less precise. The main purpose of 
# uszipcode in this script is to reference the county names in the HUD
# dataset to the associated zip codes. Some of the data from 
# uszipcode is displayed in the end since it was available.

# Supporting Docs for this import:
# https://pypi.org/project/uszipcode/
# https://uszipcode.readthedocs.io/index.html

try:
	import uszipcode
except:
	subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'uszipcode'])
import uszipcode

from uszipcode import SearchEngine, SimpleZipcode, Zipcode

################## Data Download Link Examples for HUD data 
# 2021
# Projected or current years have a different file name. Keep in mind
# for data download.
# https://www.huduser.gov/portal/datasets/50thper/FY2021_50_County.xlsx
# 2020
# https://www.huduser.gov/portal/datasets/50thper/FY2020_50_County_rev.xlsx
# 2019
# https://www.huduser.gov/portal/datasets/50thper/FY2019_50_County_rev.xlsx

################## Define year for data download
# Will pull data for current year
YearOfInterest = datetime.now().year
################## Download data for current year

# Set to no, if the folder is missing, the data pull will take place.
PullInData = 'No'

# Define the folder path for download
dir = 'CSV_DATA'
if not os.path.exists(dir):
	# If the directory is not found, we need
	# to pull the HUD data.
	PullInData = 'Yes'
	os.makedirs(dir)
CSVOut = 'CSV_DATA/'

if PullInData == 'Yes':
	# Define the base file name
	BF = 'https://www.huduser.gov/portal/datasets/50thper/FY%s_50_County' % str(YearOfInterest)
	# We are using a document link on the HUC website. Since there were
	# several API options that required an account and/or the user to pay for data,
	# I felt this was a pretty cool alternative. However, this will only contain
	# rent estimates at the 50th percentil for studio apartments up to four
	# bedroom units. Not actual current rent ranges or number of available units.
	# Zillow had a good platfor for that, but I just wanted simple data for the
	# purpose of this script.

	# NOTE: The fiscal year will automatically update when the year changes.
	# As long as the link stays the same, this will work between years.

	# Will try both formats. As there are two potential file names.
	try:
		print 'Base Data Download...'
		# Attempt first file name
		urllib3.disable_warnings()
		url = BF+'_rev.xlsx'
		fileName = "50th_Perc_%s.xlsx" % str(YearOfInterest)
		with urllib3.PoolManager() as http:
			r = http.request('GET', url)
			with open(CSVOut+fileName, 'wb') as fout:
				fout.write(r.data)
	except:
		print 'Base Data Download Fail...\nAlternative File Name Download...'
		# Attempt other file name
		urllib3.disable_warnings()
		url = BF+'.xlsx'
		fileName = "50th_Perc_%s.xlsx" % str(YearOfInterest)
		with urllib3.PoolManager() as http:
			r = http.request('GET', url)
			with open(CSVOut+fileName, 'wb') as fout:
				fout.write(r.data)

################### Prep current year data for CSV

def csv_from_excel(excelFile, BaseOutputLoc):
	Data = pd.read_excel(excelFile)
	Columns = Data.columns.values
	LVar = Data.values.tolist()
	# Convert the data to avoid character error
	ModData = []
	for ListItem in LVar:
		try:
			# Format: ['fips2010' 'rent50_0' 'rent50_1' 'rent50_2' 'rent50_3' 'rent50_4' 'state'
						 # 'cbsasub20' 'areaname20' 'county' 'cousub' 'cntyname' 'name' 'pop2017'
						 # 'hu2017' 'state_alpha']
			# We only want rent and loc name data
			# New format: [Rent 0 BR-4, City State, County Name, Secondary Name, State]
			DataToKeep = [int(ListItem[1]), int(ListItem[2]), int(ListItem[3]), int(ListItem[4]),
				int(ListItem[5]), str(ListItem[8]), str(ListItem[11]), str(ListItem[12]), str(ListItem[-1])]
			ModData.append(DataToKeep)
		except:
			# We will pass those with special characters that are not
			# able to be converted. These seem to be out of the 50 states.
			pass

	# Write to a csv file
	NewDF = pd.DataFrame(ModData, columns = ['R_0', 'R_1', 'R_2', 'R_3', 'R_4', 'City_State', 'County_Name', 'Secondary_Name', 'State'])
	# This will contain up to date data from HUD for census areas, counties, etc.
	NewDF.to_csv(BaseOutputLoc)

# runs the csv_from_excel function:
excelFile = 'CSV_DATA/50th_Perc_%s.xlsx' % str(YearOfInterest)
BaseOutputLoc = 'CSV_DATA/50th_Perc_%s.csv' % str(YearOfInterest)
csv_from_excel(excelFile, BaseOutputLoc)

############### Open the CSV file for reference

HUD_Data = []
with open(BaseOutputLoc, 'r') as Doc:
	# Counting index to skip the first rec
	i = 0
	for aItem in Doc:
		if i > 0:
			# Clean up the data
			# Define the City/State
			Sp1 = aItem.split('"')
			try:
				# Works for standard city state combinations
				CityState = Sp1[1]
				# First part of Sp1 is our rent prices
				# Final part is the remaining text data
				# I'm sure there is a better way to do this part, but
				# I like it this way.
				# Parse the rent data. This will be our 50th percentile.
				# The first part of the parse is a counting index. Will drop it.
				# The final comma also leads to a blank item. Thus we don't want
				# that either.
				Sp2 = Sp1[0].split(',')
				# This will parse our text data for state and county names.
				# Drop first record of this split, it is blank. Then mod
				# the final part as it includes a new line deliminator.
				Sp3 = Sp1[-1].split(',')
			except:
				# Works for the census areas or combinations without commas
				SpMod = Sp1[0].split(',')
				CityState = SpMod[6]
				Sp2 = SpMod[0:6]
				Sp3 = SpMod[7::]
			# Correct this data and add it to an insert item for
			# our overall HUD_Data. This data will be referenced to
			# the uszipcode import by county name.
			InsertItem = []

			SelectSp2 = Sp2[1:-1]
			SelectSp3 = Sp3[1::]
			# Remove the \n from the end of the state deliminator.
			SelectSp3[-1] = SelectSp3[-1].replace('\n', '')

			for aValue in SelectSp2:
				InsertItem.append(int(aValue))

			InsertItem.append(CityState)

			for aString in SelectSp3:
				InsertItem.append(aString)
			# Add this to the HUD_Data list item
			HUD_Data.append(InsertItem)
		# Counting index for skipping first record (That is the header)
		i = i+1

# Close the file
Doc.close()
# Format of out HUD_Data
# Format: [Rent 0 Bed, Rent 1 Bed, Rent 2 Bed, Rent 3 Bed, Rent 4 Bed, City/State/Census Area, County, City or County, State]

################## Base Zipcode entry
search = SearchEngine(simple_zipcode=False)

# This will query the data and put it directly into the search
zipcode = search.by_zipcode(raw_input('\nType in 5 digit zip code: '))
################# Zip general stats from uszipcode import

#### PULL RENTAL STATS
RentStatsZip = zipcode.monthly_rent_including_utilities_studio_apt[0]['values']

MonthlyRentData = []
for aItem in RentStatsZip:
	MonthlyRentData.append([int(aItem['y']), str(aItem['x'])])

#### PULL EDUCATIONAL STATS
EdStatsZip = zipcode.educational_attainment_for_population_25_and_over[0]['values']

EducationalData = []
for aItem in EdStatsZip:
	EducationalData.append([int(aItem['y']), str(aItem['x'])])

#### PULL EARNINGS DATA
EarnStatsZip = zipcode.annual_individual_earnings[0]['values']

EarningsData = []
for aItem in EarnStatsZip:
	EarningsData.append([int(aItem['y']), str(aItem['x'])])

#### Define Zip County and State
ZipCounty = str(zipcode.county)
ZipState = str(zipcode.state)

#### Link this to the HUD_Data by county and state
# There are multiple records for each county in some locations.
# In the case of multiple records per county, the secondary name will be 
# referenced for city/town name.

SelectHUD = []
for aItem in HUD_Data:
	CNTY = aItem[6]
	ST = aItem[-1]
	if CNTY==ZipCounty:
		if ST==ZipState:
			SelectHUD.append(aItem)

FilterHUD = []
# Test for multiple HUD recs for the given county
if len(SelectHUD)>1:
	# There are multiple recs for the county associated with the zipcode.
	CommonCities = zipcode.common_city_list
	# Filter the HUD data by the common cities if possible
	for City in CommonCities:
		for HUD_Rec in SelectHUD:
			# Parse by spaces if present
			# This may allow for the city/town name to be extracted
			PS = HUD_Rec[-2].split(' ')
			for Parse in PS:
				if Parse==City:
					FilterHUD.append(HUD_Rec)

# If FilterHUD is empty, we matched only one record. To keep the same
# syntax below, we will define SelectHUD as FilterHUD
if len(FilterHUD)==0:
	FilterHUD = SelectHUD

###################### OUTPUTS FROM THE ANALYSIS #############################
# For now we will just write a print output in the command prompt. No figures
# or anything will be made.

#********************************
# Future Tax data option. Currently I just use a flat income tax of 25 percent.
# Keeps it simple, but should be improved.

# https://taxfoundation.org/publications/state-individual-income-tax-rates-and-brackets/
# https://www.taxadmin.org/tax-rates
# Above sources are from the web page below
# https://wallethub.com/edu/best-worst-states-to-be-a-taxpayer/2416
#********************************

print '\nLOCATION: %s, %s' % (ZipCounty, ZipState)

# Calculate the required net annual income per rental 50th percentile.
# This is based on spending approximatly 30 percent of net income on
# housing. After net income is calculated, the gross
# income will be estimated based upon a flat income tax of 25 percent.
# This is not accurate for all regions. Hourly rate based on a 40 hour 
# work week is also given. This was written to aid in my personal job 
# applications. Particulalry when requesting a salary or hourly 
# wage range.

######### Rental Data
NetIncomeBrackets = []
Rents = FilterHUD[0][0:5]
Labels = ['Studio', '1 BR', '2 BR', '3 BR', '4 BR']
NetIncomeReq = []
GrossReq = []
HourlyRate = []
for aValue in Rents:
	# **RENT AS 30 PERCENT OF INCOME**
	NetIncomeReq.append((aValue/0.3)*12)
	# **ASSUME A FLAT 25 PERCENT INCOME TAX**
	# Assume 25 perc state and fed tax combined
	GrossReq.append(((aValue/0.3)*12)/0.75)
	# Estimated hourly rate required (Based from Gross Req)
	HR = (((aValue/0.3)*12/0.75)/52)/40
	HourlyRate.append(HR)

# Combine in a dataframe to illustrate the data in the prompt
CombList = []
i = 0
while i < len(GrossReq):
	CombList.append([Labels[i], Rents[i], GrossReq[i], NetIncomeReq[i], HourlyRate[i]])
	i = i+1

RentalData = pd.DataFrame(CombList, columns = ['Rental_Size', 'Price', 'Gross_Income', 'Net_Income', 'Hourly_Rate'])

##########################################################################
######## Print out rental data
print '\nRental Data and required income:\n'
print RentalData
print '*Data Source: HUD (%i)' % YearOfInterest
print '*Rental prices represent the 50th percentile.'
print '\n'
###########################################################################

######## Education Data
# print EducationalData
TotalRecs = 0
HigherEd = 0
PercentOfAll = []
PercOfDegrees = []
Labels2 = []
# Count total educational recs
i = 0
for aItem in EducationalData:
	TotalRecs = TotalRecs+aItem[0]
	if i>1:
		HigherEd = HigherEd+aItem[0]
	i = i+1
if TotalRecs>0:
	CombList2 = []
	i = 0
	for aItem in EducationalData:
		PercOfEd = (float(aItem[0])/TotalRecs)*100
		if i>1:
			HigherEdPerc = (float(aItem[0])/HigherEd)*100
		if i<=1:
			HigherEdPerc = 'nan'
		# Add data to new list
		CombList2.append([aItem[1], aItem[0], PercOfEd, HigherEdPerc])
		# Index data
		i = i+1

	EducationalData = pd.DataFrame(CombList2, columns = ['Education', 'Total_Records', '%_All_Ed', '%_Higher_Ed'])
	# Define the per of total records which is above HS
	Ratio = (float(HigherEd)/float(TotalRecs))*100

if TotalRecs==0:
	EducationalData = 'No Data Found.'
	HigherEd = 0
	Ratio = 0.0

################################################################################
###### Print out the educational data
print 'Educational Data:\n'
print 'Total Educational Data Recorded: %i' % TotalRecs
print 'Total Higher Educational Data Recorded: %i' % HigherEd
print 'Percent of Records Above High School: %f\n' % Ratio
print EducationalData
print '*Data Source: uszipcode'
print '\n'
#################################################################################

####### Earnings Data
# print EarningsData

TotalRecs = 0
for aItem in EarningsData:
	TotalRecs = TotalRecs+aItem[0]

if TotalRecs>0:
	CombList3 = []
	for aItem in EarningsData:
		PercOfRecs = (float(aItem[0])/TotalRecs)*100
		CombList3.append([aItem[-1], aItem[0], PercOfRecs])

	EarningsData = pd.DataFrame(CombList3, columns = ['Pay_Bracket', 'Total_Records', '%_Of_Records'])

if TotalRecs==0:
	EarningsData = 'No Data Found.'
################################################################################
###### Print out the earnings data
print 'Salary Data:\n'
print EarningsData
print '*Data Source: uszipcode'
print '\n'
#################################################################################

######## Rental 
TotalRecs = 0
for aItem in MonthlyRentData:
	TotalRecs = TotalRecs+aItem[0]

if TotalRecs>0:
	CombList4 = []
	for aItem in MonthlyRentData:
		PercOfRecs = (float(aItem[0])/TotalRecs)*100
		CombList4.append([aItem[-1], aItem[0], PercOfRecs])

	RentalData = pd.DataFrame(CombList4, columns = ['Rental_Bracket', 'Total_Records', '%_Of_Records'])

if TotalRecs==0:
	RentalData = 'No Data Found.'
################################################################################
###### Print out the rental data
print 'Rental Data:\n'
print RentalData
print '*Data Source: uszipcode'
print '\n'
#################################################################################
