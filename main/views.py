import datetime

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiExample, extend_schema_view, inline_serializer, OpenApiParameter
from rest_framework import viewsets, serializers, views, mixins
from rest_framework.decorators import action, api_view
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.response import Response

from main import models, schemas
from main.models import Refbook
from main.serializers import RefbookSerializer, RefbookElementSerializer


class RefbookListView(views.APIView):
	@extend_schema(**schemas.GET_REFBOOKS)
	def get(self, request):
		queryset = models.Refbook.objects.all()
		date_filter = request.query_params.get('date')
		if date_filter:
			try:
				datetime.datetime.strptime(date_filter, "%Y-%m-%d")
			except ValueError:
				raise ValidationError({'error': 'date doesn`t match format YYYY-MM-DD'})
			queryset = queryset.filter(
				versions__effective_date__lte=date_filter).distinct()
		serializer = RefbookSerializer(queryset, many=True)
		return Response({'refbooks': serializer.data})


class RefbookViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = models.Refbook.objects.all()
	serializer_class = RefbookSerializer

	@extend_schema(**schemas.GET_ELEMENTS)
	@action(
		methods=['GET'], detail=True, url_path='elements')
	def list_elements_in_version(self, request, pk=None):
		version = self.get_version()
		serializer = RefbookElementSerializer(version.elements.all(), many=True)
		return Response({'elements': serializer.data})

	@extend_schema(**schemas.CHECK_ELEMENTS)
	@action(
		methods=['GET'], detail=True, url_path='check_element')
	def check_element_in_version(self, request, pk=None):
		version = self.get_version()
		code_filter = request.query_params.get('code')
		value_filter = request.query_params.get('value')
		if code_filter is None or value_filter is None:
			raise ValidationError(
				{'error': 'both code and value parameters required'})
		result = version.elements.filter(
			code=code_filter, value=value_filter).exists()
		return Response({'result': result})

	def get_version(self) -> models.RefbookVersion:
		"""Получение текущей версии или версии из параметра запроса"""
		try:
			instance = Refbook.objects.get(pk=self.kwargs['pk'])
		except Refbook.DoesNotExist:
			raise NotFound({'error': 'refbook not found'})
		version = instance.current_version
		version_filter = self.request.query_params.get('version')
		if version_filter:
			versions = instance.versions.filter(version=version_filter)
			if versions:
				version = versions.first()
		return version
