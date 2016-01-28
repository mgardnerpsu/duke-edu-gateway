"""edugway URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
# do not use django admin 
#from django.contrib import admin
from django.conf.urls import url, include
from rest_framework import routers
from edugway.forms import views as forms_views
from edugway.videos import views as videos_views
from edugway.authors import views as authors_views
from edugway.content import views as content_views

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'forms', forms_views.FormViewSet)
router.register(r'fields', forms_views.FieldViewSet, base_name='form-fields')
router.register(r'choices', forms_views.ChoiceViewSet, base_name='field-choices')
router.register(r'videos', videos_views.VideoViewSet)
router.register(r'authors', authors_views.AuthorViewSet)
router.register(r'categories', content_views.CategoryViewSet)
router.register(r'credits', content_views.CreditViewSet)
router.register(r'courses', content_views.CourseViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    # do not use django admin
	#url(r'^admin/', admin.site.urls),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
