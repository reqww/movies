from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

from . import views, api


urlpatterns = [
#     path('movie/', views.MovieListView.as_view()),
#     path('movie/<int:pk>', views.MovieDetailView.as_view()),

    path('review/', views.ReviewCreateView.as_view()),
    path('review/<int:pk>', views.ReviewDestroyView.as_view()),

    path('rating/', views.AddStarRatingView.as_view()),

#     path('actors/', views.ActorsListView.as_view()),
#     path('actors/<int:pk>', views.ActorDetailView.as_view()),

#     path('actor-set/', api.ActorViewSet.as_view({'get': 'list'})),
#     path('actor-set/<int:pk>', api.ActorViewSet.as_view({'get': 'retrieve'})),
]

#######
movie_list = views.MovieViewSet.as_view({
    'get': 'list',
    # 'post': 'create'
})

movie_detail = views.MovieViewSet.as_view({
    'get': 'retrieve',
    # 'put': 'update',
    # 'patch': 'partial_update',
    # 'delete': 'destroy'
})

actor_list = api.ActorModelViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

actor_detail = api.ActorModelViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

actor_example = api.ActorModelViewSet.as_view({
    'get': 'example',
    'put': 'example'
})

# actor_my_list = api.ActorModelViewSet.as_view(
#     'get': 'my_list',
#     'post': 'create'
# )

urlpatterns += format_suffix_patterns([
    path('movie/', movie_list, name='movie-list'), 
    path('movie/<int:pk>', movie_detail, name='movie-detail'),

    path('actor/', actor_list, name='actor-list'),
    # path('actor-my/', actor_my_list, name = 'actor-my-list'),
    path('actor/<int:pk>/', actor_detail, name='actor-detail'),
    path('actor/<int:pk>/example/', actor_example, name='actor-example')  
])
#######

# router = DefaultRouter()
# router.register(r'actor-read', api.ActorReadOnly, basename = 'actor')
# router.register(r'actor-modelset', api.ActorModelViewSet, basename = 'actor')
# urlpatterns = router.urls
