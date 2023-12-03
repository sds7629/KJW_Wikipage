from django.shortcuts import render
from rest_framework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
)
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ParseError
from . import serializers
from .models import Feed, PayloadWord, RelationFeed
from django.db.models import QuerySet, Prefetch, F
from .feed_utils import update_percent, create_relword, create_relfeed


class FeedViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    GenericViewSet,
):
    # 쿼리를 불러올 때 연관 게시글의 중복 hit를 없애기 위해 prefetch를 통해 미리 가져오는 코드르 작성했습니다.
    queryset = Feed.objects.all().prefetch_related(
        Prefetch(
            "rel_from_feed",
            queryset=RelationFeed.objects.annotate(
                sim_pk=F("sim_feed__pk"),
                sim_title=F("sim_feed__title"),
                sim_payload=F("sim_feed__payload"),
                sim_created_at=F("sim_feed__created_at"),
            ).order_by("-similar"),
            to_attr="rel_feeds",
        )
    )
    serializer_class = serializers.ListFeedSerializer

    # 시리얼 라이저를 http method에 따라 변경되도록 설정했습니다.
    def get_serializer_class(self) -> QuerySet:
        if self.action in ["list", "retrieve"]:
            return serializers.ListFeedSerializer
        else:
            return serializers.CreateFeedSerializer

    # GET METHOD
    def list(self, request, *args, **kwargs) -> QuerySet:
        return super().list(request, *args, **kwargs)

    # Detail GET METHOD
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    # POST METHOD
    def create(self, request, *args, **kwargs) -> QuerySet:
        serializer = serializers.CreateFeedSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            pay_data = set(
                [data for data in serializer.validated_data["payload"].split(" ")]
            )
            pay_data = list(pay_data)
        except:
            raise ParseError("없는 데이터")
        all_data = PayloadWord.objects.all()
        new_feed = serializer.save(sim_word=create_relword(pay_data))
        create_relfeed(pay_data, new_feed)
        update_percent(pay_data, all_data)
        return Response(serializer.data, status=status.HTTP_200_OK)
