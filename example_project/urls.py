from django.conf.urls.defaults import patterns, include, url
from django.views.generic import TemplateView, DetailView
from example_app.models import Product


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'example_project.views.home', name='home'),
    # url(r'^example_project/', include('example_project.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/', 'example_app.views.login', name='login'),
    url(r'^product/(?P<pk>\d+)/$', DetailView.as_view(model=Product), name='product_detail'),
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
)
