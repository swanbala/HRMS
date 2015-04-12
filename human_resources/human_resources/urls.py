from django.conf.urls import patterns, include, url
from django.contrib import admin
from HRM import views
#from django.contrib.auth.views import login, logout



urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'human_resources.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/$', include(admin.site.urls)),
    (r'^login$',views.login),
    (r'^change_passwd$',views.change_passwd),
    (r'^basic_information$',views.basic_information),
    (r'^ability_work$',views.ability_work),
    (r'^success$',views.success),
    (r'^logout$', views.logout),
    (r'^sign_in$',views.sign_in),
    (r'^salary$',views.salary),
    (r'^former$',views.former),
    (r'^add$',views.add),
    (r'^sign_information$',views.sign_information),
    (r'^all_information$',views.all_information),
    (r'^salary_all$',views.salary_all),
    (r'^bonus$',views.bonus),
    (r'^time$',views.change_time),
    (r'^delete_staff/(\d{7})$',views.delete_staff),
    (r'^not_login',views.not_login),
    (r'^change_information/(\d{7})$',views.change_information),
    (r'^recorvery_former/(\d{7})$',views.recorvery_former),
    (r'^sure_former$',views.sure_former),
    
)
