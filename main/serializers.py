from drf_spectacular.utils import extend_schema_serializer, OpenApiExample
from rest_framework import serializers

from main import models


class RefbookElementSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.RefbookElement
		fields = ['code', 'value']


# @extend_schema_serializer(
# 	many=False,
# 	examples=[
# 		OpenApiExample(
# 			name='Success',
# 			value={
# 				'refbooks': [
# 					{
# 						'id': 0,
# 						'code': 'string',
# 						'name': 'string'
# 					}
# 				]
# 			},
# 			response_only=True,
# 			status_codes=[200]
# 		)
# 	]
# )
class RefbookSerializer(serializers.ModelSerializer):
	class Meta:
		model = models.Refbook
		fields = ['id', 'code', 'name']


# @extend_schema_serializer(many=False)
class RefbookListSerializer(serializers.Serializer):
	refbooks = serializers.ListSerializer(child=RefbookSerializer())


class ErrorSerializer(serializers.Serializer):
	error = serializers.CharField()
