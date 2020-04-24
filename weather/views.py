from django.shortcuts import render, redirect, get_object_or_404
import requests
from .models import City
from .forms import CityForm


def index(request):
	url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=fc107ef800e442d30bf55875a2387183&lang=en&units=metric'
	err = ''
	message = ''
	message_class = ''

	if request.method == 'POST':
		form = CityForm(request.POST)
		if form.is_valid():
			new_city = form.cleaned_data['name']
			existing = City.objects.filter(name=new_city).count()
			if existing == 0:
				r = requests.get(url.format(new_city)).json()
				if r['cod'] == 200:
					form.save()
					return redirect('index')


				else:
					err = 'NOT A VALID CITY NAME !'
			else:
				err = 'City Already exists !'

		if err:
			message = err
			message_class = 'is-danger'

		else:
			message = 'Added Successfully'
			message_class = 'is-success'


	form = CityForm()
	cities = City.objects.order_by('-id')

	weather_data = []

	for city in cities:

		r = requests.get(url.format(city)).json()


		city_weather = {
			'city': city,
			'temperature': r['main']['temp'] ,
			'description':r['weather'][0]['description'] ,
			'icon':r['weather'][0]['icon'],

		}
		weather_data.append(city_weather)
	context = {
		'weather_data':weather_data,
		'form':form,
		'message':message,
		'message_class':message_class,
	}
	return render(request, 'weather/weather.html', context)

def delete_city(request, city_id):
	city = get_object_or_404(City, id=city_id)
	city.delete()
	return redirect('index')
