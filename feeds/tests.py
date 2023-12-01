from django.test import TestCase
from .models import PayloadWord, Feed


class CompareWordTest(TestCase):
    @classmethod
    def setUpTestData(self) -> None:
        feed1 = Feed.objects.create(title="가나다라마", payload="안녕하세요 잘지내시나요?")
        feed2 = Feed.objects.create(title="가나라마", payload="안녕하세요 잘지내시나요? 저는")
        feed3 = Feed.objects.create(title="가다라마", payload="잘지내시나요? 잘지내요")
        feed4 = Feed.objects.create(title="가나다라", payload="안녕하세요!")

    def test_40퍼센트_단어_찾기(self):
        queryset = Feed.objects.all()
