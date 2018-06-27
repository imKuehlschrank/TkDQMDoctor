import django_tables2 as tables

from .models import RunInfo, ReferenceRun


# TODO remove redundancy from RunInfoTable and READONLYRunInfoTable
class RunInfoTable(tables.Table):
    edit_run = tables.TemplateColumn(
        '<div align="center"><a href="{% url \'certhelper:update\' record.id%}">'
        '<span class="glyphicon glyphicon-pencil"></a></div>',
        orderable=False)

    class Meta:
        model = RunInfo
        fields = ('userid',
                  'run_number',
                  'type',
                  'reference_run.reference_run',
                  'trackermap',
                  'number_of_ls',
                  'int_luminosity',
                  'pixel',
                  'sistrip',
                  'tracking',
                  'comment',
                  'date')
        attrs = {'class': 'table table-hover table-bordered'}


class READONLYRunInfoTable(tables.Table):
    class Meta:
        model = RunInfo
        fields = ('userid',
                  'run_number',
                  'type',
                  'reference_run.reference_run',
                  'trackermap',
                  'number_of_ls',
                  'int_luminosity',
                  'pixel',
                  'sistrip',
                  'tracking',
                  'comment',
                  'date')
        attrs = {'class': 'table table-hover table-bordered'}


class ReferenceRunTable(tables.Table):
    class Meta:
        model = ReferenceRun
        fields = ['id', 'reference_run', 'reco', 'runtype', 'bfield', 'beamtype', 'beamenergy', 'dataset', ]
        attrs = {'class': 'table table-hover table-bordered'}


class ShiftleaderRunInfoTable(RunInfoTable):
    delete_run = tables.TemplateColumn(
        '<div align="center"><a href="{% url \'certhelper:delete\' record.id%}">'
        '<span class="glyphicon glyphicon-trash"></a></div>',
        orderable=False)

    class Meta:
        attrs = {'class': 'table table-hover table-bordered'}


class DeletedRunInfoTable(tables.Table):
    restore_run = tables.TemplateColumn(
        '<div align="center"><a href="{% url \'certhelper:restore_run\' record.id%}">'
        '<span class="glyphicon glyphicon-repeat"></a></div>',
        orderable=False)
    delete_forever = tables.TemplateColumn(
        '<div align="center"><a href="{% url \'certhelper:hard_delete_run\' record.id%}">'
        '<span class="glyphicon glyphicon-trash " style="color:red"></a></div>',
        orderable=False)

    class Meta:
        model = RunInfo
        fields = ('id',
                  'deleted_at',
                  'userid',
                  'run_number',
                  'type',
                  'reference_run.reference_run',
                  'date')
        attrs = {'class': 'table table-hover table-bordered'}
