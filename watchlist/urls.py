from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views
router = DefaultRouter()

router.register('list',views.WatchListViewset)
router.register('category',views.CategoryViewset)
router.register('release',views.ReleaseViewset)

urlpatterns = [
    path('', include(router.urls)),
    path('list/<int:pk>/review/',views.ReviewList.as_view(),name='watchlist-review'),
    path('list/<int:pk>/review/create/',views.ReviewCreate.as_view(),name='watchlist-review-create'),
    path('review/<int:pk>/',views.ReviewDetails.as_view(),name='review-details'),
]