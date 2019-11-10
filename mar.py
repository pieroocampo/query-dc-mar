import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import pandas as pd

def query(addr):
	r = requests.post(
			'http://citizenatlas.dc.gov/newwebservices/locationverifier.asmx/findLocation2',
			data={'f': 'json', 'str': addr})
	r.raise_for_status()
	return r.json()


def query_schools(x,y):
	max_attempts = 10
	attempts = 0
	s = requests.Session()
	url = 'http://geospatial.dcgis.dc.gov/SchoolsWebService/sy19-20/getSchools.asmx/findSchoolsNew?x={}&y={}&f=json'.format(x,y)
	retries = Retry(total=5, backoff_factor = 1, status_forcelist=[500, 502, 503, 504])
	s.mount('http://', HTTPAdapter(max_retries=retries))
	r = s.get(url)
	return r.json()


def add_schools(row):
	schools = query_schools(row['XCOORD'],row['YCOORD'])
	return pd.Series([schools['newBoundarySchools']['inBoundaryElementarySchool'], 
					schools['newBoundarySchools']['inBoundaryMiddleSchool'], 
					schools['newBoundarySchools']['inBoundaryHighSchool']])

if __name__ == "__main__":
	df = pd.read_csv('Address_Points.csv')	
	df[['elementary_school', 'middle_school', 'high_school']] = df.apply(add_schools, axis=1)
	df.to_csv(r'Address_Points_With_Schools.csv')
