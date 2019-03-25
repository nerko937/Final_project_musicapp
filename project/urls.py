from django.contrib import admin
from django.urls import path
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from .settings import MEDIA_ROOT, MEDIA_URL
from main_page.views import MainPageView
from articles.views import (
    ArticlesView,
    ArticleView,
    AddArticles,
    CreateArticleView,
    ModifyArticleView,
    DeleteArticleView
)
from users.views import (
    SignUpView,
    LoginView,
    LogoutView,
    ModifyUserView,
    SendCommentView,
    ModifyCommentView,
    DeleteCommentView,
    AddFakeUsers
)
from music.views import (
    SearchView,
    AddFakeMusicView,
    BandView,
    CreateBandView,
    ModifyBandView,
    DeleteBandView,
    AlbumView,
    CreateAlbumView,
    ModifyAlbumView,
    DeleteAlbumView,
    SongView,
    CreateSongView,
    ModifySongView,
    DeleteSongView,
    CreateMusicianView,
    DeleteMusicianView
)


urlpatterns = [
    # main page
    path('', MainPageView.as_view(), name='main-page'),
    # users
    path('admin/', admin.site.urls),
    path('sign-up/', SignUpView.as_view(), name='sign-up'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('modify-user/', ModifyUserView.as_view(), name='modify-user'),
    # comments
    path('send-comment/', SendCommentView.as_view(), name='send-comment'),
    path('modify-comment/<int:comment_id>/', ModifyCommentView.as_view(), name='modify-comment'),
    path('delete-comment/<int:comment_id>/', DeleteCommentView.as_view(), name='delete-comment'),
    # articles
    path('articles/', ArticlesView.as_view(), name='articles'),
    path('article/<int:article_id>/', ArticleView.as_view(), name='article'),
    path('add-article/', CreateArticleView.as_view(), name='add-article'),
    path('modify-article/<int:article_id>/', ModifyArticleView.as_view(), name='modify-article'),
    path('delete-article/<int:article_id>/', DeleteArticleView.as_view(), name='delete-article'),
    # music
    path('search/', SearchView.as_view(), name='search'),
    # bands
    path('band/<int:band_id>/', BandView.as_view(), name='band'),
    path('add-band/', CreateBandView.as_view(), name='add-band'),
    path('modify-band/<int:band_id>/', ModifyBandView.as_view(), name='modify-band'),
    path('delete-band/<int:band_id>/', DeleteBandView.as_view(), name='delete-band'),
    # musicians
    path('add-musician/<int:band_id>/', CreateMusicianView.as_view(), name='add-musician'),
    path('delete-musician/<int:musician_id>', DeleteMusicianView.as_view(), name='delete-musician'),
    # albums
    path('album/<int:album_id>/', AlbumView.as_view(), name='album'),
    path('add-album/<int:band_id>/', CreateAlbumView.as_view(), name='add-album'),
    path('modify-album/<int:album_id>/', ModifyAlbumView.as_view(), name='modify-album'),
    path('delete-album/<int:album_id>/', DeleteAlbumView.as_view(), name='delete-album'),
    # songs
    path('song/<int:song_id>/', SongView.as_view(), name='song'),
    path('add-song/<int:album_id>/', CreateSongView.as_view(), name='add-song'),
    path('modify-song/<int:song_id>/', ModifySongView.as_view(), name='modify-song'),
    path('delete-song/<int:song_id>/', DeleteSongView.as_view(), name='delete-song'),
    # fake data
    path('add-fake-users/', AddFakeUsers.as_view()),
	# those need users
    path('add-fake-articles/', AddArticles.as_view()),
    path('add-fake-music/', AddFakeMusicView.as_view())
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
