import requests
import json

def getData(url):
		req = requests.get(url)						
		return req.json()

class AttorneysRequest():		
	@classmethod		
	def getAttorneys(self):			
		attorneys = getData('https://www.lawyercentral.com/utils/maps.cfc?method=getAttorneysFromLatLng&lat=39.828185&lng=-98.57954&lawyerName=&stateAbb=&practiceareaID=89')

		for attorney in attorneys['markers']:
			print(attorney['name'])
			practice_areas = getData('https://www.lawyercentral.com/utils/lawyer.cfc?method=returnPracticeAreaJSON&lawyer_id=%s' % attorney['id'])			
			for area in practice_areas['data']:
				if(area['name'] == 'Divorce'):
					print(area['y'])