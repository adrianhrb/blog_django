from django.urls import path

from blog import views

app_name = 'blog'
# In case of using post_list by using class, the path will be:"
# path('', views.PostListView.as_view(), name='post_list')

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>', views.post_detail, name='post_detail'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('<int:post_id>/comment/', views.post_comment, name='post_comment'),
]
