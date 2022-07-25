from .views import *
from django.urls import path

urlpatterns = [
    path('', SmartContractViewSet.as_view(), name='contracts'),
    path('<int:id>/', SmartContractView.as_view(), name='contract'),
    path('<int:id>/input/', BankInputView.as_view(), name='input'),
    path('<int:contract_id>/invite/', InviteModeratorView.as_view(), name='invite_random_moderator'),
    path('<int:contract_id>/invite/<int:user_id>/', InviteModeratorView.as_view(), name='invite_moderator'),
    path('invites/', InviteModeratorViewSet.as_view(), name='invites'),
    path('message/<int:id>/', AgreeRequest.as_view(), name='agree_or_disagree'),
    path('<int:contract_id>/withdrawal/', WithdrawalFundsRequestView.as_view(), name='withdrawal'),
]
