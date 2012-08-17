from django import forms
from crispy_forms.layout import Field

from caminae.mapentity.forms import MapEntityForm
from caminae.core.fields import PointLineTopologyField

from .models import Intervention, InterventionStatus, Project


class InterventionForm(MapEntityForm):
    """ An intervention can be a Point or a Line """
    topology = PointLineTopologyField()

    modelfields = (
            'name',
            'structure',
            'date',
            'status',
            'type',
            'disorders',
            Field('comments', css_class='input-xlarge'),
            'in_maintenance',
            'length',
            'height',
            'width',
            'area',
            'slope',
            'material_cost',
            'heliport_cost',
            'subcontract_cost',
            'stake',
            'project',)
    geomfields = ('topology',)

    class Meta:
        model = Intervention
        exclude = ('deleted', 'geom', 'jobs')  # TODO: inline formset for jobs


class InterventionCreateForm(InterventionForm):
    def __init__(self, *args, **kwargs):
        super(InterventionCreateForm, self).__init__(*args, **kwargs)
        # Limit status choices to first one only ("requested")
        first = InterventionStatus.objects.all()[0]
        self.fields['status'] = forms.ModelChoiceField(queryset=InterventionStatus.objects.filter(pk=first.pk))

    class Meta(InterventionForm.Meta):
        exclude = InterventionForm.Meta.exclude + (
            'length',
            'height',
            'width',
            'area',
            'slope',
            'material_cost',
            'heliport_cost',
            'subcontract_cost',
            'stake',
            'project', )


class ProjectForm(MapEntityForm):
    modelfields = (
            'name',
            'structure',
            'begin_year',
            'end_year',
            'constraint',
            'cost',
            Field('comments', css_class='input-xlarge'),
            'contractors',
            'project_owner',
            'project_manager',
            'founders',)
    geomfields = tuple()  # no geom field in project

    class Meta:
        model = Project
        exclude = ('deleted', 'founders',)  #TODO founders (inline form)
