from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect

from .forms import GroupForm
from ..userprofile.models import UserProfile
from ..document.models import Document, Pubtator
from ..document.tasks import get_pubmed_document
from ..common.models import Task, UserQuestRelationship, Group
from ..common.bioc import *

import pandas as pd
import uuid
import csv


@login_required
@user_passes_test(lambda u: u.is_staff)
def users_training(request):
    response = HttpResponse(content_type='text/html')
    writer = csv.writer(response)

    training = Task.objects.filter(kind=Task.TRAINING).all()
    writer.writerow(['user_pk', 'T1', 'T2', 'T3', 'E1_Q1', 'E2_Q2'])

    for user in User.objects.all():
        row = [user.pk]
        for t in training:
            row.append(UserQuestRelationship.objects.filter(task=t, user=user, completed=True).exists())

        row.append(UserQuestRelationship.objects.filter(task__pk=4, user=user, completed=True).exists())
        row.append(UserQuestRelationship.objects.filter(task__pk=11, user=user, completed=True).exists())
        writer.writerow(row)
    return response


@login_required
@user_passes_test(lambda u: u.is_staff)
@require_http_methods(['GET', 'POST'])
def group_list(request):

    if request.method == 'POST':
        group_form = GroupForm(instance=None, data=request.POST or None)
        group_uuid = str(uuid.uuid1())

        if group_form.is_valid():
            group = group_form.save()
            pmids = group_form.cleaned_data.get('pmids', [])
            get_pubmed_document.delay(pmids, source=group_uuid, group_pk=group.pk)
            return redirect(reverse('dashboard:groups_home'))

        ctx = {
            'groups': Group.objects.all(),
            'form': group_form
        }
        return TemplateResponse(request, 'dashboard/group_list.jade', ctx)

    if request.method == 'GET':
        group_form = GroupForm(instance=None, data=request.POST or None)
        ctx = {
            'groups': Group.objects.all().order_by('-pk'),
            'form': group_form
        }
        return TemplateResponse(request, 'dashboard/group_list.jade', ctx)


@login_required
@user_passes_test(lambda u: u.is_staff)
def group_read(request, pk):
    group = get_object_or_404(Group, pk=pk)
    ctx = {
        'group': group
    }
    return TemplateResponse(request, 'dashboard/group.jade', ctx)


@login_required
@require_http_methods(['POST'])
@user_passes_test(lambda u: u.is_staff)
def pubtator_actions(request, pk):
    pubtator = get_object_or_404(Pubtator, pk=pk)
    doc = pubtator.document

    if request.method == 'POST':
        pubtator.delete()
        doc.init_pubtator()

    return redirect(reverse('dashboard:document', doc.pk))


@login_required
@require_http_methods(['POST'])
@user_passes_test(lambda u: u.is_staff)
def document_pubtator_actions(request, pk):
    doc = get_object_or_404(Document, pk=pk)

    if request.method == 'POST':
        print '> Reset doc pubtators'
        doc.pubtator_set.all().delete()
        doc.init_pubtator()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
@user_passes_test(lambda u: u.is_staff)
def document_read(request, pk):
    doc = get_object_or_404(Document, pk=pk)
    ctx = {
        'doc': doc
    }
    return TemplateResponse(request, 'dashboard/doc.jade', ctx)


@login_required
@user_passes_test(lambda u: u.is_staff)
def home(request):

    arr = []
    users = User.objects.exclude(userprofile__isnull=True).all()
    for u in users.values('pk', 'username'):
        try:
            profile = UserProfile.objects.get(pk=u['pk'])
            arr.append((u['username'], profile.quests_count(), profile.available_quests()))
        except Exception as e:
            pass

    df = pd.DataFrame(arr, columns=['Username', 'Quest Count', 'Available Quests'])

    ctx = {
        'dataframe': df.to_html(classes='table table-striped table-condensed')
    }
    return TemplateResponse(request, 'dashboard/home.jade', ctx)

