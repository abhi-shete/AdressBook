from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'testproject.views.home', name='home'),
    # url(r'^testproject/', include('testproject.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),
    url(r'^$','testapp.views.loginpage'),
    url(r'^login/$','testapp.views.login_user'),
    url(r'^temp/$','testapp.views.index'),
    url(r'^temp/addpage$','testapp.views.addpage'),
    url(r'^temp/add/$','testapp.views.addEntry'),
    url(r'^temp/display/$','testapp.views.display'),
    url(r'^temp/display/(?P<contact>.*)$','testapp.views.update'),
    url(r'^temp/show/$','testapp.views.show'),
    url(r'^temp/deletepage/$','testapp.views.deletepage'),
    url(r'^temp/delete/(?P<contact>.*)$','testapp.views.delete'),
    url(r'^temp/searchpage/$','testapp.views.searchpage'),
    url(r'^temp/search/$','testapp.views.search'),
    url(r'^temp/editpage/(?P<contact>.*)$','testapp.views.editpage'),
    url(r'^temp/edit/(?P<contact>.*)$','testapp.views.edit'),
    url(r'^loginpage/$','testapp.views.loginpage'),
    url(r'^temp/logout/$','testapp.views.logoutpage'),
    url(r'^staff/$','testapp.views.staff_auth'),
    url(r'^temp/pwdpage/(?P<contact>.*)$','testapp.views.changePwdPage'),
    url(r'^temp/pwd/$','testapp.views.changePassword'),
    url(r'^temp/adduserpage/$','testapp.views.adduserpage'),
    url(r'^temp/adduser/$','testapp.views.adduser'),
)
