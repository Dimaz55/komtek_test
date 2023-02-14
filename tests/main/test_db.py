import pytest
import datetime as dt
from django.db import IntegrityError

from main.models import *


@pytest.mark.django_db
class TestRefbookModel:
	@pytest.mark.parametrize(
		'start_day_offset, date_qty, current_version_offset',
		[
			(-1, 3, 1), (-1, 2, 1), (-2, 2, 1), (-2, 1, 0)
		]
	)
	def test_current_version(self, version_factory, refbook_factory,
	                         start_day_offset, date_qty,
	                         current_version_offset):
		# Если сегодня 2022-02-10:
		# [2022-02-09, 2022-02-10, 2022-02-11] индекс текущей версии = 1
		# [2022-02-09, 2022-02-10] = 1
		# [2022-02-08, 2022-02-09] = 0
		# [2022-02-08] = 0
		refbook = refbook_factory()
		start_date = dt.date.today() + dt.timedelta(days=start_day_offset)
		date_range = [start_date + dt.timedelta(days=x) for x in range(date_qty)]
		for date in date_range:
			version_factory(refbook=refbook, effective_date=date)
			date -= dt.timedelta(days=1)
		assert refbook.current_version == RefbookVersion.objects.get(
			effective_date=date_range[current_version_offset])

	def test_code_unique_constraint(self):
		Refbook.objects.create(code='A')
		with pytest.raises(
				IntegrityError, match='UNIQUE constraint failed: main_refbook.code'):
			Refbook.objects.create(code='A')


@pytest.mark.django_db
class TestRefbookVersionModel:
	def test_refbook_version_unique_constraint(self, refbook_factory, version_factory):
		refbook = refbook_factory()
		version_factory(refbook=refbook, version='v1', effective_date='2023-01-10')
		with pytest.raises(
				IntegrityError,
				match='UNIQUE constraint failed: main_refbookversion.refbook_id, '
				      'main_refbookversion.version'):
			version_factory(refbook=refbook, version='v1', effective_date='2023-01-11')

	def test_refbook_effective_date_unique_constraint(self, refbook_factory,
	                                                  version_factory):
		refbook = refbook_factory()
		today = dt.date.today()
		version_factory(refbook=refbook, version='v1', effective_date=today)
		with pytest.raises(
				IntegrityError,
				match='UNIQUE constraint failed: main_refbookversion.refbook_id, '
				      'main_refbookversion.effective_date'):
			version_factory(refbook=refbook, version='v2', effective_date=today)


@pytest.mark.django_db
class TestRefbookElementModel:
	def test_refbook_version_code_unique_constraint(self, version_factory,
	                                                element_factory):
		today = dt.date.today()
		version = version_factory(version='v1', effective_date=today)
		element_factory(refbook_version=version, code='c')
		with pytest.raises(
				IntegrityError,
				match='UNIQUE constraint failed: '
				      'main_refbookelement.refbook_version_id, '
				      'main_refbookelement.code'):
			element_factory(refbook_version=version, code='c')