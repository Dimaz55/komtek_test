from django.urls import path
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView

from main.views import RefbookListView, RefbookViewSet

urlpatterns = [
	path('refbooks/', RefbookListView.as_view(), name='refbooks-list'),
	path(
		'refbooks/<pk>/elements',
		RefbookViewSet.as_view({'get': 'list_elements_in_version'}),
		name='elements'),
	path(
		'refbooks/<pk>/check_element',
		RefbookViewSet.as_view({'get': 'check_element_in_version'}),
		name='check_element'),
	path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
	path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui')
]
