from django.urls import path, include
from . import views

urlpatterns = [
    path('', include('users.urls')),
    path('', views.HomePage.as_view(), name='home'),
    path('tarif', views.tarifPage, name='tarif'),
    path('course/<slug>', views.CoursePage.as_view(), name='course-page'),
    path('course/<slug>/<les_slug>', views.LessonPage.as_view(), name='les-page'),

]

