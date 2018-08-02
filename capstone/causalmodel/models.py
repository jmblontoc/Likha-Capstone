from datetime import datetime

from django.db import models

# Create your models here.
from datapreprocessing.models import Metric


class RootCause(models.Model):

    name = models.CharField(max_length=128, null=True)
    date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.name

    @staticmethod
    def show_root_causes():

        # we will show a root cause if all of its metrics are critical
        return [root_cause for root_cause in RootCause.objects.all() if root_cause.is_critical]

    @property
    def is_critical(self):

        for metric in self.datamap_set.all():
            if not DataMap.get_metric(metric).is_alarming:
                return False

        return True


class DataMap(models.Model):

    root_cause = models.ForeignKey(RootCause, on_delete=models.CASCADE)
    metric = models.CharField(max_length=255)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    threshold = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return '%s - %s' % (self.root_cause.name, self.metric)

    def is_correlation(self):
        return " vs " in self.metric

    def get_metric(self):
        return Metric.objects.get(metric__contains=self.metric)

    @property
    def display(self):

        if self.is_correlation():
            return "Correlation(%s) | Score - (%s)" % (self.metric, self.value)

        return '%s | %s - %s' % (self.get_metric().get_document, self.metric, int(self.value))


class Box(models.Model):

    root_cause = models.ForeignKey(RootCause, on_delete=models.CASCADE)
    causal_model = models.ForeignKey('CausalModel', on_delete=models.CASCADE)

    def __str__(self):
        return self.root_cause.name


class Son(models.Model):

    box = models.ForeignKey('Box', on_delete=models.CASCADE)
    father = models.ForeignKey('Box', on_delete=models.CASCADE, related_name='Father')

    def __str__(self):
        return 'I am %s, my father is %s' % (self.box.root_cause.name, self.father.root_cause.name)

    @property
    def to_dict(self):
        return {
            "name": self.box.root_cause.name,
            "parent": self.father.root_cause.name,
            "key": self.box.root_cause.name,
            "quantifiable_data": self.get_quantifiable_data()
        }

    def get_quantifiable_data(self):

        # if self.box.root_cause is None:
        #     data = []
        #
        #     for x in self.block.root_causes_content.all():
        #         for y in x.datamap_set.all():
        #             data.append(y.display)
        #
        #     return data
        #
        # return [x.display for x in self.block.root_cause.datamap_set.all()]

        return [x.display for x in self.box.root_cause.datamap_set.all()]


class Block(models.Model):

    root_cause = models.ForeignKey(RootCause, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=128)
    root_causes_content = models.ManyToManyField(RootCause, related_name='block_root_causes')
    causal_model = models.ForeignKey('CausalModel', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Child(models.Model):

    block = models.ForeignKey(Block, on_delete=models.CASCADE)
    parent = models.ForeignKey(Block, on_delete=models.CASCADE, related_name='Dad')

    def __str__(self):
        return 'I am %s .My parent is %s' % (self.block.name, self.parent.name)

    # TODO
    def to_tree_dict(self):

        return {
            'key': self.block.id,
            'name': self.block.name,
            'parent': self.parent.id,
            'quantifiable_data': self.get_quantifiable_data()
        }

    def get_quantifiable_data(self):

        if self.block.root_cause is None:
            data = []

            for x in self.block.root_causes_content.all():
                for y in x.datamap_set.all():
                    data.append(y.display)

            return data

        return [x.display for x in self.block.root_cause.datamap_set.all()]

    @property
    def is_root_cause(self):
        return self.block.root_cause is not None


class CausalModel(models.Model):

    date = models.DateTimeField(default=datetime.now)
    is_approved = models.BooleanField(default=False)
    uploaded_by = models.ForeignKey('core.Profile', on_delete=models.CASCADE)


class CausalModelComment(models.Model):

    causal_model = models.ForeignKey(CausalModel, on_delete=models.CASCADE)
    profile = models.ForeignKey('core.Profile', on_delete=models.CASCADE)
    comment = models.TextField()
    date = models.DateTimeField(default=datetime.now)

    def to_dict(self):

        return {
            "id": self.causal_model.id,
            "profile": self.profile.get_name,
            "comment": self.comment,
            "date": self.date.strftime('%B %d, %Y'),
            "user_type": self.profile.user_type
        }


class Memo(models.Model):

    subject = models.CharField(max_length=128)
    date = models.DateTimeField(default=datetime.now)
    metric = models.ForeignKey(Metric, on_delete=models.CASCADE)
    comments = models.TextField()
    uploaded_by = models.ForeignKey('core.Profile', on_delete=models.CASCADE)

    def __str__(self):
        return self.subject


