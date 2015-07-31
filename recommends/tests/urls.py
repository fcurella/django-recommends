try:
    from django.conf.urls.defaults import patterns, include, url
except ImportError:
    from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from django.contrib import admin

from .views import RecProductView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'example_project.views.home', name='home'),
    # url(r'^example_project/',
    # include('example_project.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/',
    # include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/',
        'recommends.tests.views.login', name='login'),
    url(r'^product/(?P<pk>\d+)/$',
        RecProductView.as_view(), name='product_detail'),
    url(r'^$', TemplateView.as_view(
        template_name='home.html'), name='home'),
)
