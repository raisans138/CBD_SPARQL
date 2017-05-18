
from Sparql import views
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'SPARQL2.views.home', name='home'),
    # url(r'^SPARQL2/', include('SPARQL2.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^$', views.index),
    url(r'^index.html/$', views.index, name='home'),
    url(r'^moviesExample/$', views.go_movies),
    url(r'^mapsExample/$', views.goMap),
    url(r'^artistsExample/$', views.goArtists),

    url(r'^ajaxMap$', views.ajax_map),
    url(r'^ajaxMovie$', views.ajax_movie),
    url(r'^ajaxArtists$', views.ajax_artists),
    url(r'^ajaxAlbum$', views.ajax_album),

                       # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
