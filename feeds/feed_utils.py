from django.db.models import QuerySet
from .models import Feed, PayloadWord, FeedRelWord, RelationFeed
from thefuzz import fuzz


def update_percent(pay_data: list, all_queryset: QuerySet) -> None:
    for data in pay_data:
        all_data = PayloadWord.objects.all()
        word_set, word_is_created = PayloadWord.objects.get_or_create(
            word=data, defaults={"count": 1}
        )
        if not word_is_created:
            word_set.count += 1
            word_set.save(update_fields=["count"])
    datas = [obj for obj in all_queryset]
    for data in datas:
        data.percent = round((data.count / Feed.objects.all().count()) * 100, 2)
    all_queryset.bulk_update(datas, ["percent"])


def create_relword(pay_data: list) -> object:
    up_data = PayloadWord.percent_objects.up()
    up_word = [obj.word for obj in up_data]
    result_word = list(set(pay_data) - set(up_word))
    rel_word = FeedRelWord(word_list=result_word)
    rel_word.save()
    return rel_word


def create_relfeed(pay_data: list, query: QuerySet):
    tags = FeedRelWord.objects.all()
    up_data = PayloadWord.percent_objects.up()
    up_word = [obj.word for obj in up_data]
    reduce_payload = set(pay_data) - set(up_word)  # 60퍼 제외한 payload
    tag = [list(set(tag.word_list) & reduce_payload) for tag in tags]
    rel = []
    for i in range(1, len(tag) + 1):
        if len(tag[i - 1]) >= 2:
            sim_percent = fuzz.token_sort_ratio(
                " ".join(reduce_payload), " ".join(tag[i - 1])
            )
            rel.append(
                RelationFeed(
                    from_feed=query,
                    sim_feed=Feed.objects.get(pk=i),
                    similar=sim_percent,
                )
            )
    RelationFeed.objects.bulk_create(rel)
