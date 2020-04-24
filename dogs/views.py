
from django.shortcuts import render, redirect, get_object_or_404
import requests



def index(request):
	url = 'https://dog.ceo/api/breeds/image/random'

	r = requests.get(url).json()
	context = {
		'image_url': r['message'],
	}
	return render(request, 'dogs/index.html', context)



def books(request):
	url = 'https://openlibrary.org/api/books?bibkeys=ISBN:9780980200447&jscmd=data&format=json'

	r = requests.get(url).json()
	res = r['ISBN:9780980200447']
	print(res['cover']['small'])
	books = []
	for i in range(5):
		books.append(res['table_of_contents'][i])

	context = {
		'publishers':res['publishers'][0]['name'],
		'books':books,
		'img_url':res['cover'],

	}
	return render(request, 'dogs/books.html', context)