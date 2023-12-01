from rest_framework import serializers
from .models import Feed, RelationFeed


class ListFeedSerializer(serializers.ModelSerializer):
    rel_feed = serializers.SerializerMethodField()

    class Meta:
        model = Feed
        fields = ("pk", "title", "rel_feed", "created_at")

    def get_rel_feed(self, instance):
        result = [
            {
                "pk": feed.sim_pk,
                "title": feed.sim_title,
                "payload": feed.sim_payload,
                "created_at": feed.sim_created_at,
            }
            for feed in instance.rel_feeds
            if instance.pk != feed.sim_pk
        ]
        return result


class CreateFeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feed
        fields = ("title", "payload")
