from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import NotesList,NoteDetails,NoteCreate,NoteUpdate,NoteDelete,UserLogin,UserRegistration


urlpatterns = [
    path('',NotesList.as_view(),name='notes'),
    path('note/<int:pk>/',NoteDetails.as_view(),name='note-details'),
    path('note-create/', NoteCreate.as_view(), name='note-create'),
    path('note-update/<int:pk>/', NoteUpdate.as_view(), name='note-update'),
    path('note-delete/<int:pk>/', NoteDelete.as_view(), name='note-delete'),

    path('login/',UserLogin.as_view(),name='login'),
    path('logout/',LogoutView.as_view(next_page='login'),name='logout'),
    path('register/',UserRegistration.as_view(),name='register')

]