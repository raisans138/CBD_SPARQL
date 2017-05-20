from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from SPARQLWrapper import SPARQLWrapper, JSON

import json
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


def goArtists(request):
    return render(request, "artistsExample.html")


def ajax_artists(request):

    artist = request.GET.get("artist")

    s = ""
    re = ""
    for x in artist:
        s = x
        if x == " ":
            s = "_"
        re += s

    artist = re

    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery("""
        SELECT distinct ?album, ?name WHERE {
        
         ?album a dbo:Album ; dbo:releaseDate ?releaseDate ; foaf:name ?name; dbo:artist ?artist FILTER( regex(str(?artist), '"""+artist+"""' ))
         OPTIONAL { ?artist dbo:bandMember ?miembros }
         OPTIONAL { ?artist dbo:genre ?gen}
         ?album dbo:abstract ?abs  filter(langMatches(lang(?abs),'en'))
        } ORDER BY ?releaseDate
        """)

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    data = {'album':[], 'name':[]}

    for result in results["results"]["bindings"]:
        data['album'].append(result['album']['value'])
        data['name'].append(result['name']['value'])

    return HttpResponse(json.dumps(data), content_type="application/json")


def ajax_album(request):


    album = request.GET.get("album")
    artist = request.GET.get("artist")

    s = ""
    re = ""
    for x in artist:
        s = x
        if x == " ":
            s = "_"
        re += s

    artist = re
    print artist



    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery("""
            SELECT distinct ?album, ?name, ?genre, ?releaseDate, ?abstract, ?artist WHERE {

             ?album a dbo:Album ; dbo:releaseDate ?releaseDate ; foaf:name ?name ; dbo:abstract ?abstract;dbo:artist ?artist FILTER( regex(str(?artist), '"""+artist+"""' )) 
             FILTER (regex(str(?name), '"""+album+"""')) filter(langMatches(lang(?abstract),'en'))
             OPTIONAL { ?album dbo:genre ?genre}
             OPTIONAL { ?album dbo:producer ?producer}
             OPTIONAL { ?artist dbo:bandMember ?miembros }
             OPTIONAL { ?artist dbo:genre ?gen}
            }
            """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    data = {'album':[], 'genre':[], 'name':[], 'releaseDate':[], 'abstract':[], 'artist':[]}

    a = ""
    g = ""
    n = ""
    r = ""
    ab = ""
    ar = ""

    for result in results["results"]["bindings"]:
        a = result['album']['value']
        g = result['genre']['value']
        n = result['name']['value']
        r = result['releaseDate']['value']
        ab = result['abstract']['value']
        ar = result['artist']['value']

    data['album'].append(a)
    data['genre'].append(g)
    data['name'].append(n)
    data['releaseDate'].append(r)
    data['abstract'].append(ab)
    data['artist'].append(ar)

    return HttpResponse(json.dumps(data), content_type="application/json")


def ajax_genre(request):
    genre = request.GET.get("genre")

    s = ""
    re = ""
    for x in genre:
        s = x
        if x == " ":
            s = "_"
        re += s

    genre = re

    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery("""
       SELECT DISTINCT ?name, ?derivatives, ?instruments, ?abstract WHERE {

        ?genre a dbo:MusicGenre ; dbo:abstract ?abstract FILTER( regex(str(?genre), '"""+genre+"""' )) filter(langMatches(lang(?abstract),'en'))
        ?genre dbo:derivative ?derivatives .
        ?genre foaf:name ?name .
         ?genre dbo:instrument ?instruments
         
        } 
        """)

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    data = {'name': [], 'derivatives': [], 'instruments':[], 'abstract':[], 'groups':[], 'gname':[]}

    for result in results["results"]["bindings"]:
        data['name'].append(result['name']['value'])
        if result['derivatives']['value'] not in data['derivatives']:
            data['derivatives'].append(result['derivatives']['value'])
        if result['instruments']['value'] not in data['instruments']:
            data['instruments'].append(result['instruments']['value'])
        data['abstract'].append(result['abstract']['value'])

    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery("""
          SELECT DISTINCT ?grupo, ?name WHERE {

         ?grupo a dbo:Group ; foaf:name ?name ; dbo:genre ?genre FILTER( regex(str(?genre), '"""+genre+"""' ))
        } LIMIT 20
            """)

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    for result in results["results"]["bindings"]:
        if result['grupo']['value'] not in data['groups']:
            data['groups'].append(result['grupo']['value'])
        data['gname'].append(result['name']['value'])


    return HttpResponse(json.dumps(data), content_type="application/json")



