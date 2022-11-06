import requests
from datetime import datetime, timezone
from dateutil import parser

class SignInApp:
	def __init__(self, site_ids, base_url, connection_name, client_key, secret_key, api_timezone=timezone.utc, local_timezone=None, group_ids=[]):
		self.connection_name=connection_name
		self.base_url=base_url
		self.client_key=client_key
		self.secret_key=secret_key
		self.auth=(self.client_key, self.secret_key)
		self.site_ids=site_ids
		self.group_ids=group_ids
		self.api_timezone=api_timezone
		self.local_timezone=local_timezone
		self.create_site_objs()

	def create_site_objs(self):
		self.sites=[]
		for site_id in self.site_ids:
			s=Site(self, site_id)
			self.sites.append(s)

	def get_today(self):
		todays_visitors=[]
		for s in self.sites:
			site_visitors=s.get_today()
			todays_visitors+=site_visitors
		return todays_visitors


	def get_history(self, start_date, end_date):
		visitors=[]
		for s in self.sites:
			visitor_list=s.get_history(start_date, end_date)
			visitors+=visitor_list
		return visitors

class Site:
	data_type="JSON"
	headers={'Accept': 'application/json'}
	timeout=60
	def __init__(self, sign_in_app, site_id):
		self.sign_in_app=sign_in_app
		self.site_id=site_id

	def get(self, base_url):
		r=requests.get(base_url, timeout=self.timeout, headers=self.headers, auth=self.sign_in_app.auth)
		r.raise_for_status()
		data=r.json()
		return data

	def get_today(self):
		objs=[]
		base_url=f"{self.sign_in_app.base_url}client-api/v1/sites/{self.site_id}/today"
		data=self.get(base_url)
		for d in data:
			for visitor in d["visitors"]:
				if visitor["group_id"] in self.sign_in_app.group_ids:
					user_obj=User(self, visitor)
					objs.append(user_obj)
		return objs

	def convert_to_api_timezone(self, date):
		if not date:
			return
		return date.replace(tzinfo=None).astimezone(tz=self.sign_in_app.api_timezone).date()


	def get_history(self, start_date=None, end_date=None):
		objs=[]
		start_date=self.convert_to_api_timezone(start_date)
		end_date=self.convert_to_api_timezone(end_date)

		base_url=f"{self.sign_in_app.base_url}client-api/v1/sites/{self.site_id}/history?date_from={start_date}T00%3A00%3A00&date_to={end_date}T23%3A59%3A59&page=1"
		data=self.get(base_url)	
		for d in data["data"]:
			if d["group_id"] in self.sign_in_app.group_ids:
				user_obj=User(self, d)
				objs.append(user_obj)
		return objs

class User:
	def __init__(self, site, data_dict):
		self.site=site
		self.sign_in_app=self.site.sign_in_app
		self.__dict__.update(data_dict)
		

		if self.personal_fields:
			self.__dict__.update(self.personal_fields)
			del self.__dict__["personal_fields"]

		self.__dict__.update(self.metadata)


		del self.__dict__["metadata"]
		self.add_custom_fields()

	def add_custom_fields(self):
		self.add_localized_datetimes()
		self.sia_id=self.returning_visitor_id

	def inspect(self):
		print(f"Name: {self.name}")
		print(f"User ID: {self.returning_visitor_id}")
		print(f"Time in: {self.in_datetime_local}")
		print(f"Time out: {self.out_datetime_local}")
		print("\n"*2)

	def add_localized_datetimes(self):
		self.in_datetime_local=self.localize_datetime(self.in_datetime)
		self.out_datetime_local=self.localize_datetime(self.out_datetime)

	def localize_datetime(self, api_datetime):
		if not api_datetime:
			return
		d=parser.isoparse(api_datetime)
		return d.replace(tzinfo=self.sign_in_app.api_timezone).astimezone(tz=None)


def usage():
	from datetime import datetime, timezone
	from dateutil import parser
	
	#These options match up with the terminology of the Sign In App. Once you've created your client, it should be straight forward.
	base_url="your_base_url"
	client_key="your_client_key"
	connection_name="your_connection_name"
	secret_key="your_secret_key"
	
	#Instructs which sites to look at.
	site_ids=[]

	#Instructs which user groups to look at.
	group_ids=[]


	api=SignInApp(site_ids=site_ids, base_url=base_url, connection_name=connection_name, client_key=client_key, secret_key=secret_key, group_ids=group_ids)
	

	"""
	get_today iterates through the sites to retrieve all the visitors assigned to the group_ids specified above.
	A list of sign_in_app.user objects of all the users from the sites is retrieved.
	All datetime objects from the API come in UTC. The sign_in_app library will add localized datetimes to the user objects.
	"""
	# visitors=api.get_today()

	# print(visitors)
	


if __name__=="__main__":
	usage()