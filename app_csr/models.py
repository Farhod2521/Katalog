from django.db import models

from global_vars import measures_csr, types_csr_resources

# Create your models here.
class CSRVolumes(models.Model):
    volume_name = models.CharField(max_length=255, verbose_name='Название книги', unique=True)
    volume_code = models.CharField(max_length=2, verbose_name='Код книги', unique=True)

    def __str__(self):
        return self.volume_code + '.\t' + self.volume_name

    class Meta:
        db_table = 'csr_volumes'
        ordering = ['volume_code', 'volume_name']


class CSRParts(models.Model):
    part_name = models.CharField(max_length=255, verbose_name='Название части', unique=True)
    part_code = models.CharField(max_length=4, verbose_name='Код части', unique=True)
    part_volume = models.ForeignKey(CSRVolumes, verbose_name='Книга части', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.part_name

    class Meta:
        db_table = 'csr_parts'
        ordering = ['part_code', 'part_name']


class CSRChapters(models.Model):
    chapter_name = models.CharField(max_length=255, verbose_name='Название раздела', unique=True)
    chapter_code = models.CharField(max_length=7, verbose_name='Код раздела', unique=True)
    chapter_part = models.ForeignKey(CSRParts, verbose_name='Часть раздела', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.chapter_name

    class Meta:
        db_table = 'csr_chapters'
        ordering = ['chapter_code', 'chapter_name']


class CSRGroups(models.Model):
    group_name = models.CharField(max_length=255, verbose_name='Название группы', unique=True)
    group_code = models.CharField(max_length=10, verbose_name='Код группы')
    group_chapter = models.ForeignKey(CSRChapters, verbose_name='Раздел группы', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.group_name

    class Meta:
        db_table = 'csr_groups'
        ordering = ['group_code', 'group_name']


class CSRResources(models.Model):
    resource_name = models.CharField(max_length=600, verbose_name='Название ресурса')
    resource_code = models.CharField(max_length=20, verbose_name='Код ресурса', unique=True)
    resource_measure = models.CharField(max_length=20, verbose_name='Ед. измерения', choices=measures_csr, blank=True, null=True)
    resource_type = models.CharField(max_length=2, verbose_name='Тип ресурса', choices=types_csr_resources, default='M')
    resource_average_price = models.FloatField(verbose_name='Средняя цена', null=True)
    resource_current_average_price = models.FloatField(verbose_name='Средняя текущая цена', null=True)
    resource_group = models.ForeignKey(CSRGroups, verbose_name='Группа ресурса', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.resource_code + '.\t' + self.resource_name

    class Meta:
        db_table = 'csr_resources'
        ordering = ['resource_code', 'resource_name']


class CSRResourcesAllInfos(models.Model):
    # resource = models.ForeignKey(CSRResources, on_delete=models.DO_NOTHING)
    resource_name = models.CharField(max_length=600)
    resource_code = models.CharField(max_length=20)
    resource_measure = models.CharField(max_length=20)
    resource_type = models.CharField(max_length=2)
    resource_average_price = models.FloatField(null=True)
    resource_current_average_price = models.FloatField(null=True)
    resource_volume = models.ForeignKey(CSRVolumes, on_delete=models.DO_NOTHING)
    resource_volume_name = models.CharField(max_length=255)
    resource_part = models.ForeignKey(CSRParts, on_delete=models.DO_NOTHING)
    resource_part_name = models.CharField(max_length=255)
    resource_chapter = models.ForeignKey(CSRChapters, on_delete=models.DO_NOTHING)
    resource_chapter_name = models.CharField(max_length=255)
    resource_group = models.ForeignKey(CSRGroups, on_delete=models.DO_NOTHING)
    resource_group_name = models.CharField(max_length=255)

    def __str__(self):
        return self.resource_name

    class Meta:
        managed = False
        db_table = 'resources_all_infos'
        ordering = ['resource_name', 'resource_code']