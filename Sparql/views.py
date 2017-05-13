from django.shortcuts import render
from django.http import HttpResponseRedirect
from SPARQLWrapper import SPARQLWrapper, JSON
import time

def index(request):
    actor = "Johnny Depp"
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery("""
        SELECT DISTINCT ?pelicula WHERE {
 
  ?pelicula rdf:type <http://dbpedia.org/ontology/Film> .
  ?pelicula rdfs:label ?titulo FILTER(lang(?titulo) = "es") .
  ?pelicula dbo:starring ?reparto .
  ?reparto rdfs:label ?actor FILTER (?actor = '"""+actor+"""'@en)
  ?pelicula dct:subject ?sub FILTER( regex(str(?sub), "Disney" ))

}""")
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    list = []

    for result in results["results"]["bindings"]:
        list.append(result['pelicula']['value'])

    return render(request, "index.html", {"actor":actor, "resultados":list})