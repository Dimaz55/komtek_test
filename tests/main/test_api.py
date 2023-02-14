import datetime as dt

import pytest
from django.urls import reverse
from django.utils.http import urlencode
from model_bakery import seq

from tests.conftest import version_dates


@pytest.mark.django_db
class TestApi:

	def test_get_all_refbooks(self, refbook_factory, api_client):
		refbooks = refbook_factory(_quantity=5)
		url = reverse('refbooks-list')
		response = api_client.get(url)
		assert response.status_code == 200
		assert len(refbooks) == len(response.json()['refbooks'])

	def test_get_refbook_by_version_date(
			self, refbook_factory, api_client, version_factory):
		refbooks = refbook_factory(_quantity=3)
		for day in range(-2, 1):  # позавчера, вчера, сегодня = 1
			version_factory(
				refbook=refbooks[0],
				effective_date=dt.date.today() + dt.timedelta(days=day)
			)
		for day in range(-1, 2):  # вчера, сегодня, завтра = 1
			version_factory(
				refbook=refbooks[1],
				effective_date=dt.date.today() + dt.timedelta(days=day)
			)
		for day in range(1, 2):  # завтра, послезавтра = 0
			version_factory(
				refbook=refbooks[2],
				effective_date=dt.date.today() + dt.timedelta(days=day)
			)
		query_params = {'date': dt.date.today()}
		url = reverse('refbooks-list') + '?' + urlencode(query_params)
		response = api_client.get(url)
		assert response.status_code == 200
		assert len(response.json()['refbooks']) == 2

	@pytest.mark.parametrize(*version_dates)
	def test_get_all_elements_in_current_version(
			self, version_factory, element_factory, refbook_factory, api_client,
			dates, correct_element_count):

		refbook = refbook_factory()
		for element_count, date in enumerate(dates, 1):
			version = version_factory(effective_date=date, refbook=refbook)
			# Кол-во элементов в версии от 1 до 3 по порядку создания
			element_factory(
				_quantity=element_count,
				code=seq('c' + str(element_count)),
				value=seq('v' + str(element_count)),
				refbook_version=version
			)
		url = reverse('elements', kwargs={'pk': refbook.pk})
		response = api_client.get(url)
		assert response.status_code == 200
		assert len(response.json()['elements']) == correct_element_count

	def test_get_all_elements_in_specified_version(
			self, version_factory, element_factory, refbook_factory, api_client):
		refbook = refbook_factory()
		versions = version_factory(
			_quantity=2, refbook=refbook, effective_date=seq('2023-02-1'))
		elements = element_factory(_quantity=5, refbook_version=versions[0])
		url = reverse('elements', kwargs={'pk': refbook.pk})
		query_params = {'version': versions[0].version}
		response = api_client.get(url + '?' + urlencode(query_params))
		assert response.status_code == 200
		assert len(elements) == len(response.json()['elements'])

		query_params = {'version': versions[1].version}
		response = api_client.get(url + '?' + urlencode(query_params))
		assert response.status_code == 200
		assert len(response.json()['elements']) == 0

	def test_check_element_in_current_version(
			self, version_factory, element_factory, refbook_factory, api_client):
		refbook = refbook_factory()
		version = version_factory(refbook=refbook)
		element_factory(refbook_version=version, code='c', value='v')
		url = reverse('check_element', kwargs={'pk': refbook.pk})
		query_params = {'code': 'c', 'value': 'v'}
		response = api_client.get(url + '?' + urlencode(query_params))
		assert response.status_code == 200
		assert response.json()['result'] is True

		query_params = {'code': 'c1', 'value': 'v1'}
		response = api_client.get(url + '?' + urlencode(query_params))
		assert response.status_code == 200
		assert response.json()['result'] is False

	def test_check_element_in_specified_version(
			self, version_factory, element_factory, refbook_factory, api_client):
		refbook = refbook_factory()
		versions = version_factory(
			_quantity=2,
			refbook=refbook,
			version=seq('v'),
			effective_date=seq('2023-02-1')  # версия [1] всегда будет текущей
		)
		element_factory(refbook_version=versions[0], code='c1', value='v1')
		element_factory(refbook_version=versions[1], code='c2', value='v2')
		url = reverse('check_element', kwargs={'pk': refbook.pk})
		query_params = {
			'code': 'c1', 'value': 'v1', 'version': versions[0].version
		}
		response = api_client.get(url + '?' + urlencode(query_params))
		assert response.status_code == 200
		assert response.json()['result'] is True

		query_params = {
			'code': 'c2', 'value': 'v2', 'version': versions[0].version
		}
		response = api_client.get(url + '?' + urlencode(query_params))
		assert response.status_code == 200
		assert response.json()['result'] is False

	def test_refbook_not_found_error(self, refbook_factory, api_client):
		refbook = refbook_factory()
		url = reverse('elements', kwargs={'pk': refbook.pk+1})
		response = api_client.get(url)
		assert response.status_code == 404
