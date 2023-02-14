from django.contrib import admin
from django.db import models
from django.utils.timezone import now


class Refbook(models.Model):
	code = models.CharField('Код', max_length=100, unique=True)
	name = models.TextField('Наименование', max_length=300)
	description = models.TextField('Описание', blank=True)

	class Meta:
		verbose_name = 'Справочник'
		verbose_name_plural = 'Справочники'
		ordering = ['code']

	@property
	@admin.display(description='Текущая версия')
	def current_version(self):
		if self.versions:
			return self.versions.filter(
				effective_date__lte=now().date()).order_by('effective_date').last()
		return ''

	def __str__(self):
		return f'Справочник ({self.code}) {self.name}'


class RefbookVersion(models.Model):
	refbook = models.ForeignKey(
		Refbook,
		on_delete=models.CASCADE,
		related_name='versions',
		verbose_name='Справочник')
	version = models.CharField('Версия', max_length=50)
	effective_date = models.DateField('Дата начала действия')

	class Meta:
		ordering = ['effective_date']
		unique_together = [['refbook', 'version'], ['refbook', 'effective_date']]
		verbose_name = 'Версия справочника'
		verbose_name_plural = 'Версии справочника'

	def __str__(self):
		return f'{str(self.refbook)} (вер. {self.version} от {self.effective_date})'


class RefbookElement(models.Model):
	refbook_version = models.ForeignKey(
		RefbookVersion,
		on_delete=models.CASCADE,
		related_name='elements',
		verbose_name='Версия справочника')
	code = models.CharField('Код элемента', max_length=100, unique=True)
	value = models.TextField('Значение элемента', max_length=300)

	class Meta:
		ordering = ['code']
		unique_together = ['refbook_version', 'code']
		verbose_name = 'Элемент справочника'
		verbose_name_plural = 'Элементы справочника'
