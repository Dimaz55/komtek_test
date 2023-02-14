from drf_spectacular.utils import inline_serializer, OpenApiParameter, OpenApiExample
from rest_framework import serializers

from main.serializers import RefbookElementSerializer, RefbookSerializer, ErrorSerializer

GET_REFBOOKS = {
	'description': 'Получение списка справочников (+ актуальных на указанную дату)',
	'parameters': [
		OpenApiParameter(
			name='date',
			type={'type': 'date', 'format': 'YYYY-MM-DD'},
			description='Получение справочников, в которых имеются версии с '
			            'датой начала действия раннее или равной указанной.'
		)
	],
	'responses': {
		200: inline_serializer(
			name='refbooks',
			fields={
				'refbooks': RefbookSerializer(many=True)
			}
		),
		400: ErrorSerializer()
	},
	'examples': [
		OpenApiExample(
			name='Неверный формат даты',
			value={'error': 'date doesn`t match format YYYY-MM-DD'},
			status_codes=[400]
		),
	]
}

GET_ELEMENTS = {
	'description': 'Получение элементов текущей версии заданного справочника',
	'parameters': [
		OpenApiParameter(
			name='id',
			location='path',
			type=int,
			description='Идентификатор справочника',
			required=True
		),
		OpenApiParameter(
			name='version',
			location='query',
			type=str,
			description='Получение элементов указанной версии'
		)
	],
	'responses': {
		200: inline_serializer(
			name='elements',
			fields={
				'elements': RefbookElementSerializer(many=True)
			}
		),
		404: ErrorSerializer()
	},
	'examples': [
		OpenApiExample(
			name='Справочник не существует',
			value={'error': 'refbook not found'},
			status_codes=[404]
		)
	]

}

CHECK_ELEMENTS = {
	'description': 'Валидация элемента справочника - проверка на то, что '
	               'элемент с данным кодом и значением присутствует в текущей '
	               'версии справочника.',
	'parameters': [
		OpenApiParameter(
			name='id',
			location='path',
			type=int,
			description='Идентификатор справочника',
			required=True
		),
		OpenApiParameter(
			name='code',
			type=str,
			description='Код элемента',
			required=True
		),
		OpenApiParameter(
			name='value',
			type=str,
			description='Значение элемента',
			required=True
		),
		OpenApiParameter(
			name='version',
			type=str,
			description='Проверка на включение в указанную версию справочника'
		)
	],
	'responses': {
		200: inline_serializer(name='result', fields={'result': serializers.BooleanField()}),
		400: ErrorSerializer(),
		404: ErrorSerializer()
	},
	'examples': [
		OpenApiExample(
			name='Элемент присутствует в версии',
			value={'result': True},
			status_codes=[200]
		),
		OpenApiExample(
			name='Элемент отсутствует в версии',
			value={'result': False},
			status_codes=[200]
		),
		OpenApiExample(
			name='Не указаны обязательные параметры: код и значение',
			value={'error': 'both code and value parameters required'},
			status_codes=[400]
		),
		OpenApiExample(
			name='Справочник не существует',
			value={'error': 'refbook not found'},
			status_codes=[404]
		)
	]
}
