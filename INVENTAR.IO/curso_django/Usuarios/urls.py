from django.urls import path
from Usuarios import views

urlpatterns = [
    path('<int:pag>',views.users),
    path('registration/',views.registration, name='registration'),
    path('edit/<int:user_id>',views.edit, name ='edit_user'),
    path('delete/<int:user_id>',views.delete, name='delete_user'),
    path('login/',views.login_request, name='login'),
    path('logout/',views.logout_request, name='logout')
]