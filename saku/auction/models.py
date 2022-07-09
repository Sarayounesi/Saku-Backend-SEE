from django.contrib.auth.models import User
from django.db import models
from .tasks import save_best_bid
from saku.celery import app

def photo_path(instance, filename):
    basefilename, file_extension= os.path.splitext(filename)
    randomstr = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))
    return 'images/auction_images/{randomstring}{ext}'.format(randomstring=randomstr, ext=file_extension)


class Category(models.Model):

    name = models.CharField(max_length=20, primary_key=True)

    def __str__(self):
        return self.name


class Tags(models.Model):

    name = models.CharField(max_length=20, primary_key=True)

    def __str__(self):
        return self.name


class Auction(models.Model):

    class Mode(models.IntegerChoices):
        INCREASING = 1
        DECREASING = 2

    name = models.CharField(max_length=20)
    token = models.CharField(max_length=8, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_created=True)
    finished_at = models.DateTimeField()
    mode = models.IntegerField(choices=Mode.choices, default=Mode.INCREASING)
    limit = models.IntegerField(default=0)
    location = models.CharField(max_length=50, blank=True)
    description = models.CharField(max_length=200, blank=True)
    is_private = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    tags = models.ManyToManyField(Tags, blank=True)
    participants_num = models.IntegerField(default=0)
    show_best_bid = models.BooleanField(default=False)
    celery_task_id = models.CharField(max_length=100)
    best_bid = models.ForeignKey(to='bid.Bid', related_name='best_bid', on_delete=models.DO_NOTHING, null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        try: 
            pre_finished_at = Auction.objects.get(pk=self.pk).finished_at
        except Auction.DoesNotExist:
            pre_finished_at = None
        super().save(*args, **kwargs)
        post_finished_at = self.finished_at
        if not self.celery_task_id:  # initial task creation
            task_object = save_best_bid.apply_async((self.pk,), eta=post_finished_at)
            Auction.objects.filter(pk=self.pk).update(celery_task_id=task_object.id)
        elif pre_finished_at != post_finished_at:
            # revoke the old task
            app.control.revoke(self.celery_task_id, terminate=True)
            task_object = save_best_bid.apply_async((self.pk,), eta=post_finished_at)
            Auction.objects.filter(pk=self.pk).update(celery_task_id=task_object.id)
