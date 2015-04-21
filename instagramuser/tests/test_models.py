from django.test import TestCase
from django.utils.text import slugify
from django.test.client import RequestFactory

from attributes.models import Attribute
from categories.models import Category

from instagramuser.models import (InspiringUser, Follower, Following, InspiringUserBelongsToCategory,
                                  InspiringUserBelongsToAttribute)


# Create your tests here.
from libs.instagram.tools import InstagramUserAdminUtils, InstagramSession


class InspiringUserModelTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

        InspiringUser.objects.get_or_create(instagram_user_id='ABCD123',
                                            instagram_user_name='pera'
                                            )
        InspiringUser.objects.get_or_create(instagram_user_id='ABCD456',
                                            instagram_user_name='mika'
                                            )
        InspiringUser.objects.get_or_create(instagram_user_id='ABCD789',
                                            instagram_user_name='laza'
                                            )
        InspiringUser.objects.get_or_create(
                                            instagram_user_name='nnenads'
                                            )
        Category.objects.get_or_create(title=u'Category One',
                                       description=u'Description1',
                                       slug=slugify(u'Category1')
                                       )
        Category.objects.get_or_create(title=u'Category Two',
                                       description=u'Description1',
                                       slug=slugify(u'Category1')
                                       )
        Attribute.objects.get_or_create(title=u'Attribute One',
                                       description=u'Description1',
                                       slug=slugify(u'Attribute1')
                                       )
        Attribute.objects.get_or_create(title=u'Attribute Two',
                                       description=u'Description1',
                                       slug=slugify(u'Attribute2')
                                       )

    def test_change_instagram_user_name(self):
        obj = InspiringUser.objects.get(instagram_user_id='ABCD123')
        obj.instagram_user_name = 'pera2'
        obj.save()
        obj = InspiringUser.objects.get(instagram_user_id='ABCD123')
        self.assertEqual(obj.instagram_user_name == 'pera2', True)

    def test_change_instagram_user_id(self):
        obj = InspiringUser.objects.get(instagram_user_id='ABCD456')
        obj.instagram_user_id = 'ABCD456789'
        obj.save()
        obj = InspiringUser.objects.get(instagram_user_id='ABCD456789')
        self.assertEqual(obj.instagram_user_id == 'ABCD456789', True)

    def test_add_category_to_inspiring_user(self):
        obj = InspiringUser.objects.get(instagram_user_id='ABCD123')
        cat = Category.objects.get(title='Category One')
        InspiringUserBelongsToCategory.objects.create(instagram_user=obj,
                                                      category=cat,
                                                      frequency=1,
                                                      weight=0.3
        )
        l_cnt = obj.categories.all().count()
        self.assertGreaterEqual(l_cnt, 1)

    def test_add_attribute_to_inspiring_user(self):
        obj = InspiringUser.objects.get(instagram_user_id='ABCD123')
        atr = Attribute.objects.get(title='Attribute One')
        InspiringUserBelongsToAttribute.objects.create(instagram_user=obj,
                                                      attribute=atr,
                                                      frequency=1,
                                                      weight=0.3
        )
        l_cnt = obj.attributes.all().count()
        self.assertGreaterEqual(l_cnt, 1)

    def test_processing_for_basic_info(self):
        obj = InspiringUser.objects.get(instagram_user_name='nnenads')
        obj.to_be_processed_for_basic_info = True
        obj.instagram_user_id = 'WrongID'
        obj.save()
        instagram_utils = InstagramUserAdminUtils()

        self.assertNotEqual(instagram_utils, None)

        #request = self.factory.get('/members/dashboard')
        #queryset = InspiringUser.objects.filter(instagram_user_name='nnenads')
        ig_session = InstagramSession(
            p_is_admin=True, p_token=''
        )
        ig_session.init_instagram_API()

        instagram_utils.analyze_instagram_user(ig_session, obj)
        # print 'Instagram user ID: %s ' % (obj.instagram_user_id)
        self.assertNotEqual(obj.instagram_user_id, 'WrongID')


