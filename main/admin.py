from django.contrib import admin

from main import models


class VersionsInline(admin.TabularInline):
	model = models.RefbookVersion
	extra = 0
	can_delete = False
	readonly_fields = ['version', 'effective_date']

	def has_add_permission(self, request, obj=None):
		return False


@admin.register(models.Refbook)
class RefbookAdmin(admin.ModelAdmin):
	list_display = ['id', 'code', 'name', 'current_version', 'get_version_date']
	list_display_links = ['id', 'code', 'name']
	inlines = [VersionsInline]

	@admin.display(description='Дата версии')
	def get_version_date(self, obj):
		if obj.current_version:
			return obj.current_version.effective_date
		return '-'


class ElementInline(admin.TabularInline):
	model = models.RefbookElement
	extra = 1


@admin.register(models.RefbookVersion)
class RefbookVersionAdmin(admin.ModelAdmin):
	list_display = [
		'get_refbook_code', 'get_refbook_name', 'version', 'effective_date'
	]
	list_select_related = ['refbook']
	inlines = [ElementInline]

	@admin.display(description='Код справочника')
	def get_refbook_code(self, obj):
		return obj.refbook.code

	@admin.display(description='Наименование справочника')
	def get_refbook_name(self, obj):
		return obj.refbook.name


@admin.register(models.RefbookElement)
class RefbookElementAdmin(admin.ModelAdmin):
	list_display = ['code', 'value']
	list_select_related = ['refbook_version']
