from django.db.models import Sum, Count, F
from auction.models import Auction
from bid.models import Bid

# - daramad
def get_income(user):
    income = Auction.objects.filter(user=user, best_bid__isnull=False).aggregate(
        Sum("best_bid__price")
    )["best_bid__price__sum"]
    return 0 if income == None else income


# - tedad auction movafagh (best_bid.user=user and finished_at > datetime.now)
def get_seccussfull_auction_count(user):
    return Auction.objects.filter(best_bid__user=user).count()


# - participant num on my auctions
def get_auctions_participants_num(all_user_auctions):
    return all_user_auctions.aggregate(Sum("participants_num"))["participants_num__sum"]


# - tedad my auctions
def get_auctions_count(all_user_auctions):
    return all_user_auctions.count()


# - 5 ta az akharin mozayede sherkat karde :
#   - mode
#   - name
#   - started_at
#   - finished_at
#   - vaziat (barande, bazande)
def get_last_auctions_participated(user, all_user_bids):
    all_user_bids = all_user_bids.order_by("-time")
    success_choices = ["successfull", "failed", "unknown"]
    last_auctions = []
    auctions = set()
    for user_bid in all_user_bids:
        if len(auctions) == 5:
            break
        if user_bid.auction.pk not in auctions:
            auction = user_bid.auction
            auctions.add(auction.pk)
            best_bid = auction.best_bid
            if best_bid == None:
                success = success_choices[2]
            else:
                best_bid_user = best_bid.user
                if best_bid_user == user:
                    success = success_choices[0]
                else:
                    success = success_choices[1]
            auction_info = {
                "mode": auction.mode,
                "name": auction.name,
                "created_at": auction.created_at,
                "finished_at": auction.finished_at,
                "success": success,
            }
            last_auctions.append(auction_info)
    return last_auctions


# - 5 ta az akharin mozayede ijad karde :
#   - mode
#   - name
#   - participant num
#   - started_at
#   - finished_at
#   - best_bid
#   - cathegory
def get_last_auctions_created(all_user_auctions):
    return all_user_auctions.order_by("-created_at").values(
        "mode",
        "name",
        "participants_num",
        "created_at",
        "finished_at",
        "best_bid",
        "category",
    )[:5]


# - list daramad ha
def get_income_list(user):
    income_list = []
    auctions = Auction.objects.filter(user=user, best_bid__isnull=False)
    for auction in auctions:
        income_list.append(auction.best_bid.price)
    return income_list


# - mizane mosharekate shoma
def get_your_colaberation_list(all_user_bids, all_user_auctions):
    colaberation_count = (
        all_user_auctions.values("created_at__date")
        .annotate(count=Count("id"))
        .order_by("created_at__date")
        .union(
            all_user_bids.values_list("time__date")
            .annotate(count=Count("id"))
            .order_by("time__date")
        )
    )
    ### does union works?
    ### how to convert to list better ?
    colaberation_list = []
    for colaberation in colaberation_count:
        colaberation_list.append(colaberation["count"])
    return colaberation_list


def get_your_colaberation_count(all_user_bids, all_user_auctions):
    return all_user_auctions.count() + all_user_bids.count()


# - list moshahede afrad az my auction
def get_others_colaberation_list(user):
    colaberation_count = (
        Bid.objects.filter(auction__user=user)
        .values("time__date")
        .annotate(count=Count("id"))
        .order_by("time__date")
    )
    ### how to convert to list better ?
    colaberation_list = []
    for colaberation in colaberation_count:
        colaberation_list.append(colaberation["count"])
    return colaberation_list


def get_others_colaberation_count(user):
    return Bid.objects.filter(auction__user=user).count()


# - list hazine ha
def get_expense_list(user, all_user_bids):
    expense_list = []
    for user_bid in all_user_bids:
        if Auction.objects.filter(best_bid=user_bid).exists():
            expense_list.append(user_bid.price)
    return expense_list


def get_expense(user, all_user_bids):
    expense = 0
    for user_bid in all_user_bids:
        if Auction.objects.filter(best_bid=user_bid).exists():
            expense += user_bid.price
    return expense


# - tedad auction mode 1 sherkat karde
def get_auction1_participate_count(user):
    auction1_participate = set()
    all_user_bids = Bid.objects.filter(user=user, auction__mode=1)
    for user_bid in all_user_bids:
        auction1_participate.add(user_bid.auction)
    return len(auction1_participate)


# - tedad auction mode 1 ijad karde
def get_auction1_create_count(user):
    return Auction.objects.filter(user=user, mode=1).count()


# - tedad auction mode 2 sherkat karde
def get_auction2_participate_count(user):
    auction2_participate = set()
    all_user_bids = Bid.objects.filter(user=user, auction__mode=2)
    ### make better
    for user_bid in all_user_bids:
        auction2_participate.add(user_bid.auction.pk)
    return len(auction2_participate)


# - tedad auction mode 2 ijad karde
def get_auction2_create_count(user):
    return Auction.objects.filter(user=user, mode=2).count()


# - payam haye akhir
def get_last_chats(user):
    # username = user.username
    pass


# - list az:
#   - hazine, daramad -> entekhabe sal
def get_yearly_income_list(user, year):
    income_list = []
    auctions = Auction.objects.filter(
        user=user, finished_at__year=year, best_bid__isnull=False
    )
    for auction in auctions:
        income_list.append(auction.best_bid.price)
    return income_list


def get_yearly_expense_list(user, year, all_user_bids):
    expense_list = []
    for user_bid in all_user_bids:
        if Auction.objects.filter(best_bid=user_bid, finished_at__year=year).exists():
            expense_list.append(user_bid.price)
    return expense_list
