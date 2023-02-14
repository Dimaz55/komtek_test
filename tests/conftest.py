import pytest
import datetime as dt
from model_bakery import baker

from main.models import *
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
	return APIClient()


@pytest.fixture
def element_factory():
	def factory(**kwargs):
		return baker.make(RefbookElement, **kwargs)

	return factory


@pytest.fixture
def version_factory():
	def factory(**kwargs):
		return baker.make(RefbookVersion, **kwargs)

	return factory


@pytest.fixture
def refbook_factory():
	def factory(**kwargs):
		return baker.make(Refbook, **kwargs)

	return factory


version_dates = (
	'dates, correct_element_count',
	[
		(
			[
				dt.date.today() - dt.timedelta(days=1),
				dt.date.today(),
				dt.date.today() + dt.timedelta(days=1)
			],
			2
		),
		(
			[
				dt.date.today() - dt.timedelta(days=2),
				dt.date.today() - dt.timedelta(days=1),
				dt.date.today()
			],
			3
		),
		(
			[
				dt.date.today() - dt.timedelta(days=2),
				dt.date.today() - dt.timedelta(days=1),
				dt.date.today() + dt.timedelta(days=1)
			],
			2
		)
	]
)
