import datetime
import pytz
from saku.celery import app
import bid.models, auction.models


@app.task(bind=True)
def save_best_bid(self, instance_pk):
    try:
        instance = auction.models.Auction.objects.get(pk=instance_pk)
        if instance.finished_at.replace(tzinfo=pytz.UTC) <= datetime.datetime.now(pytz.UTC):
            bids = bid.models.Bid.objects.filter(auction=instance_pk).order_by('price')
            best_bid = None
            if len(bids)>0:
                if instance.mode == 1:
                    best_bid = bids.last()
                else:
                    best_bid = bids.first()
            instance.best_bid = best_bid
            instance.save()
    except:
        print('Task failed due to an error!')
