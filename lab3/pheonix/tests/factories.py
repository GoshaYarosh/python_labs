from django.test import TestCase
from django.core.urlresolvers import reverse
from pheonix import models, factories


class FactoryTestCase(TestCase):

    def test_channel_factory(self):
        channel = factories.ChannelFactory.create_instance()
        db_channel = models.Channel.objects.filter(id=channel.id)
        self.assertTrue(db_channel.exists())

        db_channel = db_channel.first()
        self.assertEquest(db_channel.title, channel.title)
        self.assertEqual(db_channel.description, channel.description)

    def test_member_factory(self):
        member = factories.MemberFactory.create_instance()
        db_member = models.Member.objects.filter(username=member.username)
        self.assertTrue(db_member.exists())

        db_member = db_member.first()
        self.assertEqual(db_member.first_name, member.first_name)
        self.assertEqual(db_member.last_name, member.last_name)
