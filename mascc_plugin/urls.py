from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^mascc/(?P<graph>(.|\n)+)$', 'mascc_plugin.views.parse'),
    # url(r'^$', 'mascc_plugin.views.home', name='home'),
    # url(r'^mascc_plugin/', include('mascc_plugin.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
