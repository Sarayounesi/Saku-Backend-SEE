from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from auction.models import Auction
from bid.models import Bid
from .functions import *


class HomepageView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, year):
        user = request.user
        all_user_auctions = Auction.objects.filter(user=user)
        all_user_bids = Bid.objects.filter(user=user)

        response = {
                    'status': 'success',
                    'code': status.HTTP_200_OK,
                    'data': {
                            'income' : get_income(user),
                            'seccussfull_auction_count' : get_seccussfull_auction_count(user),
                            'auctions_participants_num' : get_auctions_participants_num(all_user_auctions),
                            'auctions_count' : get_auctions_count(all_user_auctions),
                            'last_auctions_participated' : get_last_auctions_participated(user, all_user_bids),
                            'last_auctions_created' : get_last_auctions_created(all_user_auctions),
                            'income_list' : get_income_list(user),
                            'your_colaberation_list' : get_your_colaberation_list(all_user_bids, all_user_auctions),
                            'your_colaberation_count' : get_your_colaberation_count(all_user_bids, all_user_auctions),
                            'others_colaberation_list' : get_others_colaberation_list(user),
                            'others_colaberation_count' : get_others_colaberation_count(user),
                            'expense_list' : get_expense_list(user, all_user_bids),
                            'expense' : get_expense(user, all_user_bids),
                            'auction1_participate_count' : get_auction1_participate_count(user),
                            'auction1_create_count' : get_auction1_create_count(user),
                            'auction2_participate_count' : get_auction2_participate_count(user),
                            'auction2_create_count' : get_auction2_create_count(user),
                            # 'last_chats' : get_last_chats(user),
                            'income_list' : get_yearly_income_list(user, year),
                            'expense_list' : get_yearly_expense_list(user, year, all_user_bids),
                    }
            }
        return Response(response, status=status.HTTP_200_OK)
