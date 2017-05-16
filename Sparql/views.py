from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from SPARQLWrapper import SPARQLWrapper, JSON

import json
import googlemaps
from datetime import datetime
import time

def index(request):
      return render(request, "index.html")

def go_movies(request):
    return render(request, "moviesExample.html")

def ajax_movie(request):

    actor = request.GET.get("actor")
    related = request.GET.get("related")

    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery("""
            SELECT DISTINCT ?pelicula WHERE {

      ?pelicula rdf:type <http://dbpedia.org/ontology/Film> .
      ?pelicula rdfs:label ?titulo FILTER(lang(?titulo) = "es") .
      ?pelicula dbo:starring ?reparto .
      ?reparto rdfs:label ?actor FILTER (?actor = '""" + actor + """'@en)
      ?pelicula dct:subject ?sub FILTER( regex(str(?sub), '"""+related+"""' ))

    }""")
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    list = []

    for result in results["results"]["bindings"]:
        list.append(result['pelicula']['value'])

    print list
    return HttpResponse(json.dumps(list), content_type="application/json")

def goMap(request):
    return render(request, "mapsExample.html")


def ajax_map(request):
    popu = request.GET.get("popu")
    ciOrCoun = request.GET.get("ciOrCoun")
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery("""

        SELECT distinct ?country, ?lat, ?long WHERE{ 
         ?country a dbo:"""+ciOrCoun+"""; dbo:populationTotal ?population ; rdf:type ?tipo .
         #FILTER (regex (?tipo, "WikicatCountriesInEurope")).
         FILTER (?population > """+popu+""").
         ?country geo:lat ?lat .
         ?country geo:long ?long .
    }""")

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    paises = []
    coord = []
    data = {'countries': [], 'lat': [], 'long':[]}
    for result in results["results"]["bindings"]:
        if result['country']['value'] not in data['countries']:
            data['countries'].append(result['country']['value'])
            data['lat'].append(result['lat']['value'])
            data['long'].append(result['long']['value'])

    return HttpResponse(json.dumps(data), content_type="application/json")




