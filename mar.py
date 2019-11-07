import requests
import pandas as pd

def query(addr):
	r = requests.post(
			'http://citizenatlas.dc.gov/newwebservices/locationverifier.asmx/findLocation2',
			data={'f': 'json', 'str': addr})
	r.raise_for_status()
	return r.json()


def query_schools(x,y):
	url = 'http://geospatial.dcgis.dc.gov/SchoolsWebService/sy19-20/getSchools.asmx/findSchoolsNew?x={}&y={}&f=json'.format(x,y)
	r = requests.get(url)
	r.raise_for_status()
	return r.json()


def add_schools(row):
	schools = query_schools(row['XCOORD'],row['YCOORD'])
	row['elementary_school'] = schools['newBoundarySchools']['inBoundaryElementarySchool']
	row['middle_school'] = schools['newBoundarySchools']['inBoundaryMiddleSchool']
	row['high_school'] = schools['newBoundarySchools']['inBoundaryHighSchool']
	return row

if __name__ == "__main__":
	df = pd.read_csv('Address_Points.csv')
	df.apply(add_schools, axis=1)
	df.to_csv(r'Address_Points_With_Schools.csv')
