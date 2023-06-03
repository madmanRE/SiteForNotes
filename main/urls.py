from django.urls import path, include
from .views import index, RegisterView, UpdateProfile, ListNotes, CreateNote, UpdateNote, DeleteNote, NoteViewSet
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'note', NoteViewSet)
print(router.urls)

app_name = 'main'

urlpatterns = (
        [
            path('api/', include(router.urls)),
            path('login/', LoginView.as_view(template_name='main/login.html'), name='login'),
            path('logout/', LogoutView.as_view(next_page='main:index'), name='logout'),
            path('register/', RegisterView.as_view(), name='register'),
            path('note/<int:pk>/update/', UpdateNote.as_view(), name='update_note'),
            path('note/<int:pk>/delete/', DeleteNote.as_view(), name='delete_note'),
            path('profile/<int:pk>/create_note/', CreateNote.as_view(), name='create_note'),
            path('profile/<int:pk>/', UpdateProfile.as_view(), name='update_profile'),
            path('profile/<int:pk>/notes/', ListNotes.as_view(), name='list_notes'),
            path('', index, name='index'),

        ]
        + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
        + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

)
