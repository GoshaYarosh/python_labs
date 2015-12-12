from random import randint
from pheonix import models


class Factory(object):

    @staticmethod
    def get_random_int(min_value=-100, max_value=100):
        return randint(min_value, max_value)

    @staticmethod
    def get_random_char(min_char='a', max_char='z'):
        return chr(randint(ord(min_char), ord(max_char)))

    @staticmethod
    def get_random_string(length=100):
        return  "".join(Factory.get_random_char() for _ in xrange(length))

    @staticmethod
    def get_random_email(email_length=50, host_length=20, domain_length=5):
        return "{email}@{host}.{domain}".format(
            email=Factory.get_random_string(length=email_length),
            host=Factory.get_random_string(length=host_length),
            domain=Factory.get_random_string(length=domain_length),
        )

    @classmethod
    def _extract_attrs(cls, **kwargs):
        fields = cls.Meta.fields
        attrs = dict([
            (attr, value)
            for attr, value in cls.__dict__.iteritems()
                if attr in fields
        ])
        attrs.update(dict([
            (attr, value)
            for attr, value in kwargs.iteritems()
                if attr in fields
        ]))
        return attrs

    @classmethod
    def create_instance(cls, **kwargs):
        instance = cls.Meta.model.objects.create(**cls._extract_attrs(**kwargs))
        return instance

    @classmethod
    def create_batch(cls, count=3):
        return [cls.create_instance() for _ in xrange(count)]


class ChannelFactory(Factory):

    class Meta:
        model = models.Channel
        fields = ('title', 'description', )

    title = Factory.get_random_string(length=20)
    descrition = Factory.get_random_string(length=200)


class MemberFactory(Factory):

    class Meta:
        model = models.Channel
        fields = (
            'username',
            'password',
            'email',
            'first_name',
            'last_name'
        )

    username = Factory.get_random_string(length=20)
    password = Factory.get_random_string(length=50)
    email = Factory.get_random_email(20, 10, 3)
    first_name = Factory.get_random_string(length=20)
    last_name = Factory.get_random_string(length=20)

    @classmethod
    def create_instance(cls, **kwargs):
        instance = models.Member.objects.create_user(**cls._extract_attrs())
        return instance


class MessageFactory(Factory):

    class Meta:
        model = models.Message
        fields = ('content', 'member', 'user')
