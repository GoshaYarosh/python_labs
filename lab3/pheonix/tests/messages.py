from django.test import TestCase
from django.core.urlresolvers import reverse
from pheonix import models, factories


class ChannelsViewTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.member = factories.MemberFactory.create_instance()
        factories.ChannelFactory.create_batc    h(count=5)

    def test_get_all_channels(self):
        self.client.force_login(self.member)
        response = self.client.get(reverse('channels_view'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('channels', response.context)

        channels = response.context['channels']
        db_channels = models.Channel.objects.all()
        self.assertEqual(len(db_channels), len(response.context['channels']))

        for channel, db_channel in zip(channels, db_channels):
            self.assertEqual(db_channel.id, channel.id)
            self.assertEqual(db_channel.title, channel.title)
            self.assertEqual(db_channel.description, channel.description)

    def test_create_new_channel(self):
        title = factories.Factory.get_random_string(length=40)
        description = factories.Factory.get_random_string(length=60)
        data = {'title': title, 'description': description}

        self.client.force_login(self.member)
        response = self.client.post(reverse('channels_view'), data)
        self.assertEqual(response.status_code, 200)

        channel = models.Channel.objects.filter(title=title)
        self.assertTrue(channel.exists())
        self.assertEqual(channel.first().description, description)
