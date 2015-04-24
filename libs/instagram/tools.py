from __future__ import division
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseNotFound
from django.utils import timezone
from emoji.models import Emoji
#from members.models import Membership
from photos.models import Photo
from smartfeed.models import SquareFollowing, SquareFollowingMember

from squaresensor.settings.base import TEST_APP, TEST_APP_FRIENDS_TR_ANALYZE_N_FRIENDS, FRIENDS_TR_MIN_MEDIA_COUNT, \
    FRIENDS_TR_MAX_MEDIA_COUNT, FRIENDS_TR_MIN_FOLLOWINGS, FRIENDS_TR_MAX_FOLLOWINGS, FRIENDS_TR_MIN_FOLLOWERS, \
    FRIENDS_TR_MAX_FOLLOWERS, FRIENDS_TR_MIN_FF_RATIO, FRIENDS_TR_MAX_FF_RATIO, FRIENDS_TR_LAST_POST_BEFORE_DAYS, \
    FOLLOWINGS_TR_MAX_MEDIA_COUNT, FOLLOWINGS_TR_MIN_FOLLOWINGS, FOLLOWINGS_TR_MAX_FOLLOWINGS, \
    FOLLOWINGS_TR_MIN_FOLLOWERS, FOLLOWINGS_TR_MAX_FOLLOWERS, FOLLOWINGS_TR_MIN_MEDIA_COUNT, FOLLOWINGS_TR_MIN_FF_RATIO, \
    FOLLOWINGS_TR_MAX_FF_RATIO, FOLLOWINGS_TR_LAST_POST_BEFORE_DAYS, FRIENDS_TR_ANALYZE_N_FRIENDS, \
    FOLLOWINGS_TR_ANALYZE_N_FOLLOWINGS, TEST_APP_FRIENDS_TR_ANALYZE_N_FOLLOWINGS, INSPIRING_USERS_FIND_TOP_N_PHOTOS, \
    INSPIRING_USERS_SEARCH_N_PHOTOS, FRIENDS_FIND_TOP_N_PHOTOS, FRIENDS_SEARCH_N_PHOTOS, MEMBERS_FIND_TOP_N_PHOTOS, \
    MEMBERS_SEARCH_N_PHOTOS, FOLLOWINGS_FIND_TOP_N_PHOTOS, FOLLOWINGS_SEARCH_N_PHOTOS, INSTAGRAM_API_THRESHOLD, \
    INSTAGRAM_CLIENT_SECRET, INSTAGRAM_LIMIT_PERIOD_RESET_TIME_HOURS, FIND_FRIENDS_LIMIT_PERIOD_RESET_TIME_DAYS

__author__ = 'n.nikolic'
from sys import exc_info
from datetime import (
    datetime, timedelta
)

import numpy as np
import logging

from instagram import InstagramAPI
from instagram.bind import InstagramAPIError, InstagramClientError

from django.conf import settings
from django.shortcuts import get_object_or_404

from squaresensor.settings.base import INSTAGRAM_SECRET_KEY, IMPORT_MAX_INSTAGRAM_FOLLOWINGS

from instagramuser.models import Follower, Following, InspiringUser, InspiringUserBelongsToCategory, \
    InspiringUserBelongsToAttribute, FollowerBelongsToCategory, FollowerBelongsToAttribute


class InstagramAPIParametersInvalid(Exception):
    """ Easy to understand naming conventions work best! """
    pass


class InstagramSession():
    """Set of tools regarding Instagram API"""

    api = None

    def __init__(self,
                 p_is_admin,
                 p_token,
                 ):

        init_params_ok = False

        if p_is_admin:
            self.access_token = INSTAGRAM_SECRET_KEY
        else:
            self.access_token = p_token

    def init_instagram_API(self):
        """Initializes Instagram API session

        Parameters: -
        Returns: Instagram API session
        """

        try:
            self.api = InstagramAPI(access_token=self.access_token)
            if self.api:
                temp = self.api.user_search(q='instagram', count=1)  # @UnusedVariable
        except InstagramAPIError as e:
            if (e.status_code == 400):
                l_user_private = True  # @UnusedVariable
            else:
                if (e.status_code == 429):
                    l_limits_exceeded = True  # @UnusedVariable
                else:
                    logging.exception("init_instagram_API: ERR-00001 Instagram API Error %s : %s" % (e.status_code, e.error_message))
        except InstagramClientError as e:
            logging.exception("init_instagram_API: ERR-00002 Instagram Client Error %s : %s" % (e.status_code, e.error_message))
        except:
            logging.exception("init_instagram_API: ERR-00003 Unexpected error: ")
            raise


    def is_instagram_user_valid(self, p_gooduser_name):
        '''Check if you can find Instagram user'''

        user_search = None
        if self.api:
            try:
                user_search = self.api.user_search(q=p_gooduser_name, count=1)

            except InstagramAPIError as e:
                if (e.status_code == 400):
                    l_user_private = True  # @UnusedVariable
                else:
                    if (e.status_code == 429):
                        l_limits_exceeded = True  # @UnusedVariable
                    else:
                        logging.exception("is_instagram_user_valid: ERR-00004 Instagram API Error %s : %s" % (e.status_code, e.error_message))

            except InstagramClientError as e:
                logging.exception("is_instagram_user_valid: ERR-00005 Instagram Client Error %s : %s" % (e.status_code, e.error_message))
                return None
            except:
                logging.exception("is_instagram_user_valid: ERR-00006 Unexpected error: ")
                raise

        return user_search

    def is_instagram_photo_valid(self, p_photo_id):
        '''Checks if Instagram photo exists'''
        l_photo = None

        try:
            l_photo = self.api.media(media_id = p_photo_id)
        except InstagramAPIError as e:
            if (e.status_code == 400):
                l_user_private = True  # @UnusedVariable
            else:
                logging.exception("is_instagram_photo_valid: ERR-00018 Instagram API Error %s : %s" % (e.status_code, e.error_message))

        except InstagramClientError as e:
            logging.exception("is_instagram_photo_valid: ERR-00019 Instagram Client Error %s : %s" % (e.status_code, e.error_message))
            return None
        except:
            logging.exception("is_instagram_photo_valid: ERR-00020 Unexpected error: ")
            raise

        if l_photo:
            return True
        else:
            return False

    def get_instagram_photo_info(self, p_photo_id):
        '''returns Instagram photo information'''

        try:
            l_photo = self.api.media(media_id=p_photo_id)
        except InstagramAPIError as e:
            logging.exception("get_instagram_photo_info: ERR-00021 Instagram API Error %s : %s" % (e.status_code, e.error_message))

        except InstagramClientError as e:
            logging.exception("get_instagram_photo_info: ERR-00022 Instagram Client Error %s : %s" % (e.status_code, e.error_message))
            return None
        except:
            logging.exception("get_instagram_photo_info: ERR-00023 Unexpected error: ")
            raise

        return l_photo

    def get_instagram_user(self, user_search_result):
        '''Get Instagram user

        Parameters:
        p_gooduser - GoodUser object

        Returns
        Instagram user object
        '''

        instagram_user = None
        l_user_private = False  # @UnusedVariable

        if self.api:
            try:
                instagram_user = self.api.user(user_search_result)
            except InstagramAPIError as e:

                if (e.status_code == 400):
                    l_user_private = True  # @UnusedVariable
                else:
                    logging.exception("get_instagram_user: ERR-00014 Instagram API Error %s : %s" % (e.status_code, e.error_message))
            except InstagramClientError as e:
                logging.exception("get_instagram_user: ERR-00015 Instagram Client Error %s : %s" % (e.status_code, e.error_message))
            except IndexError:
                logging.exception("get_instagram_user: ERR-00016 Instagram search unsuccessful: %s" % (exc_info()[0]))
            except:
                logging.exception("get_instagram_user: ERR-00017 Unexpected error: %s" % (exc_info()[0]))
                raise


        return instagram_user

    def get_api_limits(self):
        '''Returns a tuple of (Instagram AOI limit remaining, Instagram API limit)'''

        return self.api.x_ratelimit_remaining, self.api.x_ratelimit


class MyLikes:

    def __init__(self, p_instgram_user, p_photo_id, p_instagram_api):
        """Initialize class object
           Parameters:
           p_instagram_api - opened instagram session
           p_max_like_id - photo ID
        """

        self.liked_media = None
        self.instagram_session = p_instagram_api
        self.photo_id = p_photo_id # ID of media to check
        self.my_instgram_username = p_instgram_user

    def get_number_of_media_likes(self):
        """Returns number of likes on a media object for Instagram ID self.photo_id"""
        pass


    def has_user_liked_media(self):
        """returns if user liked the media self.max_like_id """

        self.liked_media = self.instagram_session.get_instagram_photo_info(self.photo_id)
        no_of_likes = self.liked_media.like_count


        if self.liked_media.user_has_liked :
            return True, no_of_likes
        else:
            return False, no_of_likes

    def like_instagram_media(self):
        """Procedure that likes instagram media with ID  self.photo_id"""

        result = 'error'
        l_user_private = False  # @UnusedVariable

        l_client_secret = INSTAGRAM_CLIENT_SECRET
        # Check if media is already liked
        has_user_liked_media, no_of_likes = self.has_user_liked_media()  # @UnusedVariable
        if has_user_liked_media:
            # If already liked - unlike

            try:
                self.instagram_session.api.client_secret = l_client_secret
                self.instagram_session.api.client_ips = '127.0.0.1'
                self.instagram_session.api.unlike_media(
                    media_id=self.photo_id,
                    include_secret=True,
                    )
                result = 'unlike'
            except  InstagramAPIError as e:
                if (e.status_code == 400):
                    l_user_private = True                  # @UnusedVariable
                    if (e.status_code == 403):
                        raise InstagramAPIError                 # @UnusedVariable
                    else:
                        logging.exception("get_instagram_user: ERR-00032 Instagram API Error %s : %s" % (e.status_code, e.error_message))
            except InstagramClientError as e:
                logging.exception("get_instagram_user: ERR-00033 Instagram Client Error %s : %s" % (e.status_code, e.error_message))
            except IndexError:
                logging.exception("get_instagram_user: ERR-00034 Instagram search unsuccessful: %s" % (exc_info()[0]))
            except:
                logging.exception("get_instagram_user: ERR-00035 Unexpected error: %s" % (exc_info()[0]))
                raise
        else:
            '''if not already liked - like'''
            try:
                self.instagram_session.api.client_secret = l_client_secret
                self.instagram_session.api.client_ips = '127.0.0.1'

                self.instagram_session.api.like_media(
                    media_id=self.photo_id,
                    include_secret=True,
                    )
                result = 'like'
            except InstagramAPIError as e:
                if (e.status_code == 400):
                    l_user_private = True                # @UnusedVariable
                    if (e.status_code == 403):
                        raise InstagramAPIError                 # @UnusedVariable
                    else:
                        logging.exception("get_instagram_user: ERR-00036 Instagram API Error %s : %s" % (e.status_code, e.error_message))
            except InstagramClientError as e:
                logging.exception("get_instagram_user: ERR-00037 Instagram Client Error %s : %s" % (e.status_code, e.error_message))
            except IndexError:
                logging.exception("get_instagram_user: ERR-00038 Instagram search unsuccessful: %s" % (exc_info()[0]))
            except:
                logging.exception("get_instagram_user: ERR-00039 Unexpected error: %s" % (exc_info()[0]))
                raise

        return result

    def comment_instagram_media(self, p_comment_text):
        '''Procedure that likes instagram media with ID  self.photo_id'''

        result = 'error'
        l_user_private = False  # @UnusedVariable

        try:
            self.instagram_session.api.create_media_comment (media_id=self.photo_id,
                                                             text=p_comment_text
            )
            result = 'comment'
        except InstagramAPIError as e:
            if (e.status_code == 400):
                l_user_private = True            # @UnusedVariable
            else:
                logging.exception("get_instagram_user: ERR-00040 Instagram API Error %s : %s" % (e.status_code, e.error_message))
        except InstagramClientError as e:
            logging.exception("get_instagram_user: ERR-00041 Instagram Client Error %s : %s" % (e.status_code, e.error_message))
        except IndexError:
            logging.exception("get_instagram_user: ERR-00042 Instagram search unsuccessful: %s" % (exc_info()[0]))
        except:
            logging.exception("get_instagram_user: ERR-00043 Unexpected error: %s" % (exc_info()[0]))
            raise


        return result


class BestPhotos:
    '''Find best photos of instgaram user'''
    l_user_has_photos = True

    def __init__(self, instgram_user_id, top_n_photos, search_photos_amount, instagram_api):
        '''Initialize class object'''

        self.l_instgram_user_id = instgram_user_id
        self.l_top_n_photos = top_n_photos
        self.l_search_photos_amount = search_photos_amount
        self.l_instagram_user_id = instgram_user_id
        self.l_latest_photos = None
        self.instagram_session = instagram_api
        '''Resulting list of Instagram photo id's, length of max top_n_photos'''
        self.top_photos_list = []

    def linreg(self, x, y):
        '''Does linear regression parameter calculation'''

        regression = np.polyfit(x, y, 2)
        return regression

    def prediction(self, regression, point):
        '''Returns prediction for given argument(number of likes)'''

        y = regression[0]*point + regression[1]
        return y

    def get_instagram_photos(self):
        '''Retreive l_search_photos_amount photos of given Instagram user
        l_instgram_user_id

        Returns:
        Nothing
        '''
        recent_media = None
        media_feed = None
        x_next = None
        l_user_private = False

        try:
            recent_media, x_next = self.instagram_session.api.user_recent_media(user_id=self.l_instgram_user_id)
        except InstagramAPIError as e:
            if e.status_code == 400:
                l_user_private = True
            else:
                logging.exception("get_instagram_photos: ERR-00008 Instagram API Error %s : %s" % (e.status_code, e.error_message))
        except InstagramClientError as e:
            logging.exception("get_instagram_photos: ERR-00009 Instagram Client Error %s : %s" % (e.status_code, e.error_message))
            raise
        except IndexError:
            logging.exception("get_instagram_photos: ERR-00010 Instagram search unsuccessful: %s" % (exc_info()[0]))
            raise
        except:
            logging.exception("get_instagram_photos: ERR-00011 Unexpected error: %s" % (exc_info()[0]))
            raise

        if not l_user_private:
            if not recent_media:
                self.l_user_has_photos = False

            if len (recent_media) < self.l_search_photos_amount:
                if recent_media and x_next:
                    while x_next:
                        try:
                            media_feed, x_next = self.instagram_session.api.user_recent_media(with_next_url=x_next)
                        except InstagramAPIError as e:
                            logging.exception("get_instagram_photos: ERR-00012 Instagram API Error %s : %s" % (e.status_code, e.error_message))

                        except InstagramClientError as e:
                            logging.exception("get_instagram_photos: ERR-00013 Instagram Client Error %s : %s" % (e.status_code, e.error_message))
                        except IndexError:
                            logging.exception("get_instagram_photos: ERR-000114 Instagram search unsuccessful: %s" % (exc_info()[0]))
                        except:
                            logging.exception("get_instagram_photos: ERR-00015 Unexpected error: %s" % (exc_info()[0]))
                            raise("get_instagram_user: ERR-00015 Unexpected error: %s" % (exc_info()[0]))


                        recent_media.extend(media_feed)
                        if len (recent_media) >= self.l_search_photos_amount:
                            break


        if self.l_user_has_photos:
            self.l_latest_photos = recent_media
        else:
            self.l_user_has_photos = None

    def get_top_photos(self):
        '''Using linear regression find top photos in media pool of Instagram UserWarning

        Parameters:
        p_number_of_photos - top X photos to find
        p_media - Instagram API media object - list of Instagram photos of the user
        '''
        l_polynomial_result = None
        l_max_days = None
        l_min_days = None
        l_max_likes = None
        l_min_likes = None

        if self.l_user_has_photos and self.l_latest_photos:
            '''Convert Instagram media object to list'''
            l_media_list = []
            for x_media in self.l_latest_photos:
                if x_media.type == 'image':
                    l_time_delta = datetime.today() - x_media.created_time
                    l_media_list.append([x_media.id, x_media.like_count,
                                         x_media.comment_count,
                                         l_time_delta.days,
                                         0 # Error - to be calculated
                    ]
                    )
            #media_cnt = len(l_media_list)
            '''Normalize the number of likes and days'''
            l_max_likes = max(l[1] for l in l_media_list)
            l_min_likes = min(l[1] for l in l_media_list)
            l_max_days = max(l[3] for l in l_media_list)
            l_min_days = min(l[3] for l in l_media_list)

            l_normalized_media_list = []
            for val in l_media_list:
                if (l_max_likes - l_min_likes) != 0:
                    val[1] = (val[1] - l_min_likes) / (l_max_likes - l_min_likes)
                else:
                    val[1] = 0

                if (l_max_days - l_min_days) != 0:
                    val[3] = (val[3] - l_min_days) / (l_max_days - l_min_days)
                else:
                    val[3] = 0
                l_normalized_media_list.append(val)

            '''Sort media by date'''
            l_normalized_media_list = sorted(l_normalized_media_list, key=lambda x: x[3], reverse = True)

            '''Extract feature Date and label Likes to calculate linear regression parameters'''
            l_linreg_params = []
            l_linreg_results = []
            for val in l_normalized_media_list:
                l_linreg_params.extend([val[3]]) # days
                l_linreg_results.extend([val[1]]) # likes

            '''Calculate linear regression quadratic function based on actual likes'''
            l_regression = np.polyfit(l_linreg_params, l_linreg_results, 2)
            l_polynomial = np.poly1d(l_regression)
            l_polynomial_result = l_polynomial
            l_predictions = l_polynomial(l_linreg_params)

            '''Find errors, and write them in l_normalized_media_list'''
            l_cnt = 0
            for val in l_predictions:
                l_error = l_linreg_results[l_cnt] - val
                l_normalized_media_list[l_cnt][4] = l_error
                l_cnt += 1

            '''Sort by error value - descending'''
            l_normalized_media_list = sorted(l_normalized_media_list, key=lambda x: x[4], reverse=True)

            l_cnt = 1
            l_media_cnt = len(l_normalized_media_list)
            for val in l_normalized_media_list:
                self.top_photos_list.append([val[0], val[4]])
                if (l_cnt >= self.l_top_n_photos) or (l_cnt >= l_media_cnt):
                    break
                l_cnt += 1

        return l_polynomial_result, l_max_days, l_min_days, l_max_likes, l_min_likes

    def get_unanswered_author_comments(self, p_author_instagram_user_id):
        """

        :param p_author_instagram_user_id:
        :type p_author_instagram_user_id:
        :param p_instagram_photo_id:
        :type p_instagram_photo_id:
        :return:
        :rtype:
        """
        pass


class BestFollowers():
    """Class for finding the best Instagram followers - Friends

        Configuration for searching new friends:
        FRIENDS_TR_ANALYZE_N_FRIENDS
        FRIENDS_TR_LAST_POST_BEFORE_DAYS
        FRIENDS_TR_MIN_MEDIA_COUNT
        FRIENDS_TR_MAX_MEDIA_COUNT
        FRIENDS_TR_MIN_FOLLOWINGS
        FRIENDS_TR_MAX_FOLLOWINGS
        FRIENDS_TR_MIN_FOLLOWERS
        FRIENDS_TR_MAX_FOLLOWERS
        FRIENDS_TR_MIN_FF_RATIO
        FRIENDS_TR_MAX_FF_RATIO
    """
    l_instgram_user_id = None
    l_analyze_n_photos = None
    l_instagram_api = None

    l_analyzed_followers = 0
    l_private_followers = 0

    def __init__(self, p_instgram_user_id, p_analyze_n_photos, p_instagram_api):
        """Initialize class"""

        self.l_instgram_user_id = p_instgram_user_id
        self.l_analyze_n_photos = p_analyze_n_photos
        self.l_instagram_api = p_instagram_api

    def is_user_active_in_last_n_days(self, p_instagram_follower_id, n):
        """Returns activity of user
        Parameters:
        n - number of days in the pas when user had to post on Instagram

        Returns
        Boolean - True if user was active in last n days
        """
        l_is_user_active = False

        l_best_photos = BestPhotos(p_instagram_follower_id, 1, 1, self.l_instagram_api)
        if l_best_photos:
            l_best_photos.get_instagram_photos()

            if l_best_photos.l_latest_photos:
                l_photo = l_best_photos.l_latest_photos[0] # get the last photo
                l_time_delta = datetime.today() - l_photo.created_time

                if l_time_delta <= timedelta(days=n):
                    l_is_user_active = True

        return l_is_user_active

    def get_all_instagram_followers(self, request, logged_member):
        """
        Get all Instagram followers for instagram user self.l_instgram_user_id
        """
        l_instagram_followers = None
        l_user_private = None

        try:
            l_instagram_followers, x_next = self.l_instagram_api.api.user_followed_by(
                self.l_instgram_user_id
            )
        except InstagramAPIError as e:
            if (e.status_code == 400):
                l_user_private = True
            else:
                logging.exception("get_best_instagram_followers: ERR-00050 Instagram API Error %s : %s" % (e.status_code, e.error_message))
        except InstagramClientError as e:
            logging.exception("get_best_instagram_followers: ERR-00051 Instagram Client Error %s : %s" % (e.status_code, e.error_message))
        except IndexError:
            logging.exception("get_best_instagram_followers: ERR-00052 Instagram search unsuccessful: %s" % (exc_info()[0]))
        except:
            logging.exception("get_best_instagram_followers: ERR-00053 Unexpected error: %s" % (exc_info()[0]))
            raise

        if (len(l_instagram_followers) < self.l_analyze_n_photos) and (not l_user_private):
            if l_instagram_followers:
                while x_next:
                    try:
                        l_next_followers, x_next = self.l_instagram_api.api.user_followed_by(with_next_url = x_next)
                    except InstagramAPIError as e:
                        if (e.status_code == 400):
                            l_user_private = True
                        else:
                            logging.exception("get_best_instagram_followers: ERR-00050 Instagram API Error %s : %s" % (e.status_code, e.error_message))
                    except InstagramClientError as e:
                        logging.exception("get_best_instagram_followers: ERR-00055 Instagram Client Error %s : %s" % (e.status_code, e.error_message))
                    except IndexError:
                        logging.exception("get_best_instagram_followers: ERR-00056 Instagram search unsuccessful: %s" % (exc_info()[0]))
                    except:
                        logging.exception("get_best_instagram_followers: ERR-00057 Unexpected error: %s" % (exc_info()[0]))
                        raise


                    l_instagram_followers.extend(l_next_followers)
                    if len (l_instagram_followers) >= self.l_analyze_n_photos:
                        break

        return l_instagram_followers


    def get_best_instagram_followers(self):
        '''Analyze followers and find the best ones'''

        l_instagram_followers = []
        l_best_instagram_followers = []
        l_existing_instagram_friends = []
        l_user_private = False
        self.l_analyzed_followers = 0
        self.l_private_followers = 0
        self.l_already_friends = 0

        try:
            l_instagram_followers, x_next = self.l_instagram_api.api.user_followed_by(
                self.l_instgram_user_id
            )
        except InstagramAPIError as e:
            if (e.status_code == 400):
                l_user_private = True
            else:
                logging.exception("get_best_instagram_followers: ERR-00050 Instagram API Error %s : %s" % (e.status_code, e.error_message))
        except InstagramClientError as e:
            logging.exception("get_best_instagram_followers: ERR-00051 Instagram Client Error %s : %s" % (e.status_code, e.error_message))
        except IndexError:
            logging.exception("get_best_instagram_followers: ERR-00052 Instagram search unsuccessful: %s" % (exc_info()[0]))
        except:
            logging.exception("get_best_instagram_followers: ERR-00053 Unexpected error: %s" % (exc_info()[0]))
            raise

        if (len(l_instagram_followers) < self.l_analyze_n_photos) and (not l_user_private):
            if l_instagram_followers:
                while x_next:
                    try:
                        l_next_followers, x_next = self.l_instagram_api.api.user_followed_by(with_next_url = x_next)
                    except InstagramAPIError as e:
                        logging.exception("get_best_instagram_followers: ERR-00054 Instagram API Error %s : %s" % (e.status_code, e.error_message))
                    except InstagramClientError as e:
                        logging.exception("get_best_instagram_followers: ERR-00055 Instagram Client Error %s : %s" % (e.status_code, e.error_message))
                    except IndexError:
                        logging.exception("get_best_instagram_followers: ERR-00056 Instagram search unsuccessful: %s" % (exc_info()[0]))
                    except:
                        logging.exception("get_best_instagram_followers: ERR-00057 Unexpected error: %s" % (exc_info()[0]))
                        raise

                    l_instagram_followers.extend(l_next_followers)
                    if len (l_instagram_followers) >= self.l_analyze_n_photos:
                        break

        for follower in l_instagram_followers:
            '''Filter only the best followers'''
            l_exists = Follower.objects.filter(instagram_user_id=follower.id)
            l_user_private = False
            self.l_analyzed_followers += 1

            if l_exists.count() == 0:
                try:
                    l_user_data = self.l_instagram_api.api.user(follower.id)
                except InstagramAPIError as e:

                    if (e.status_code == 400):
                        l_user_private = True
                        self.l_private_followers += 1
                    else:
                        logging.debug("get_best_instagram_followers: ERR-00058 Instagram API Error %s : %s" % (e.status_code, e.error_message))
                except InstagramClientError as e:
                    logging.exception("get_best_instagram_followers: ERR-00059 Instagram Client Error %s : %s" % (e.status_code, e.error_message))
                except IndexError:
                    logging.exception("get_best_instagram_followers: ERR-00060 Instagram search unsuccessful: %s" % (exc_info()[0]))
                except:
                    logging.debug("get_best_instagram_followers: ERR-00061 Unexpected error: %s" % (exc_info()[0]))
                    raise

                if not l_user_private:
                    l_friends_media_count = l_user_data.counts[u'media']
                    l_friends_followings = l_user_data.counts[u'follows']
                    l_friends_followers = l_user_data.counts[u'followed_by']
                    if l_friends_followers != 0:
                        l_friends_ff_ratio = l_friends_followings / l_friends_followers
                    else:
                        l_friends_ff_ratio = 0

                    if (FRIENDS_TR_MIN_MEDIA_COUNT <= l_friends_media_count <= FRIENDS_TR_MAX_MEDIA_COUNT) and \
                            (FRIENDS_TR_MIN_FOLLOWINGS <= l_friends_followings <= FRIENDS_TR_MAX_FOLLOWINGS) and \
                            (FRIENDS_TR_MIN_FOLLOWERS <= l_friends_followers <= FRIENDS_TR_MAX_FOLLOWERS) and \
                            (FRIENDS_TR_MIN_FF_RATIO <= l_friends_ff_ratio <= FRIENDS_TR_MAX_FF_RATIO):

                        if self.is_user_active_in_last_n_days(follower.id, FRIENDS_TR_LAST_POST_BEFORE_DAYS):
                            '''User is active in last N days, passed all requirements
                               Add it to friends
                            '''

                            l_best_instagram_followers.extend([l_user_data])
            else:
                '''Friend already in database'''
                self.l_already_friends += 1
                l_existing_instagram_friends.extend([follower.id])
                pass

        return l_best_instagram_followers, l_existing_instagram_friends


class BestFollowings():
    '''Class for finding the best Instagram followers - Friends

        Configuration for searching new friends:
        FOLLOWINGS_TR_ANALYZE_N_FOLLOWINGS
        FOLLOWINGS_TR_LAST_POST_BEFORE_DAYS
        FOLLOWINGS_TR_MIN_MEDIA_COUNT
        FOLLOWINGS_TR_MAX_MEDIA_COUNT
        FOLLOWINGS_TR_MIN_FOLLOWINGS
        FOLLOWINGS_TR_MAX_FOLLOWINGS
        FOLLOWINGS_TR_MIN_FOLLOWERS
        FOLLOWINGS_TR_MAX_FOLLOWERS
        FOLLOWINGS_TR_MIN_FF_RATIO
        FOLLOWINGS_TR_MAX_FF_RATIO
    '''
    l_instgram_user_id = None
    l_analyze_n_photos = None
    l_instagram_api = None
    l_user_type = None

    l_analyzed_followings = 0
    l_private_followings = 0

    def __init__(self, p_instgram_user_id, p_user_type, p_analyze_n_photos, p_instagram_api):
        '''Initialize class'''

        self.l_instgram_user_id = p_instgram_user_id
        self.l_analyze_n_photos = p_analyze_n_photos
        self.l_instagram_api = p_instagram_api
        self.l_user_type = p_user_type

    def is_user_active_in_last_n_days(self, p_instagram_following_id, n):
        '''Returnts activity of user
        Parameters:
        n - number of days in the pas when user had to post on Instagram

        Returns
        Boolean - True if user was active in last n days
        '''
        l_is_user_active = False

        l_best_photos = BestPhotos(p_instagram_following_id, 1, 1, self.l_instagram_api)
        if l_best_photos:
            l_best_photos.get_instagram_photos()

            if l_best_photos.l_latest_photos:
                l_photo = l_best_photos.l_latest_photos[0] # get the last photo
                l_time_delta = datetime.today() - l_photo.created_time

                if l_time_delta <= timedelta(days=n):
                    l_is_user_active = True

        return l_is_user_active

    def get_instagram_followings(self):
        """
        Returns instagram followings for instagram user l_instgram_user_id
        """
        l_instagram_followings = None
        l_next_followings = None
        l_user_private = False

        try:
            l_instagram_followings, x_next = self.l_instagram_api.api.user_follows(
                self.l_instgram_user_id
            )
        except InstagramAPIError as e:
            if (e.status_code == 400):
                l_user_private = True
            else:
                logging.exception("get_instagram_followings: ERR-00060 Instagram API Error %s : %s" % (e.status_code, e.error_message))
        except InstagramClientError as e:
            logging.exception("get_instagram_followings: ERR-00061 Instagram Client Error %s : %s" % (e.status_code, e.error_message))
        except IndexError:
            logging.exception("get_instagram_followings: ERR-00062 Instagram search unsuccessful: %s" % (exc_info()[0]))
        except:
            logging.exception("get_instagram_followings: ERR-00063 Unexpected error: %s" % (exc_info()[0]))
            raise HttpResponseNotFound

        if (len(l_instagram_followings) < self.l_analyze_n_photos) and (not l_user_private):
            if l_instagram_followings:
                while x_next:
                    try:
                        l_next_followings, x_next = self.l_instagram_api.api.user_follows(with_next_url = x_next)
                    except InstagramAPIError as e:
                        logging.exception("get_instagram_followings: ERR-00064 Instagram API Error %s : %s" % (e.status_code, e.error_message))
                    except InstagramClientError as e:
                        logging.exception("get_instagram_followings: ERR-00065 Instagram Client Error %s : %s" % (e.status_code, e.error_message))
                    except IndexError:
                        logging.exception("get_instagram_followings: ERR-00066 Instagram search unsuccessful: %s" % (exc_info()[0]))
                    except:
                        logging.exception("get_best_instagram_followings: ERR-00067 Unexpected error: %s" % (exc_info()[0]))
                        raise HttpResponseNotFound


                    l_instagram_followings.extend(l_next_followings)
                    if len (l_instagram_followings) >= self.l_analyze_n_photos:
                        break

        return l_instagram_followings

    def get_best_instagram_followings(self):
        """Analyze followers and find the best ones"""

        l_instagram_followings = []
        l_best_instagram_followings = []
        l_existing_instagram_followings = []
        l_user_private = False
        self.l_analyzed_followings = 0
        self.l_private_followings = 0
        self.l_already_followings = 0

        try:
            l_instagram_followings, x_next = self.l_instagram_api.api.user_follows(
                self.l_instgram_user_id
            )
        except InstagramAPIError as e:
            if (e.status_code == 400):
                l_user_private = True
            else:
                logging.exception("get_best_instagram_followings: ERR-00060 Instagram API Error %s : %s" % (e.status_code, e.error_message))
        except InstagramClientError as e:
            logging.exception("get_best_instagram_followings: ERR-00061 Instagram Client Error %s : %s" % (e.status_code, e.error_message))
        except IndexError:
            logging.exception("get_best_instagram_followings: ERR-00062 Instagram search unsuccessful: %s" % (exc_info()[0]))
        except:
            logging.exception("get_best_instagram_followings: ERR-00063 Unexpected error: %s" % (exc_info()[0]))
            raise

        if (len(l_instagram_followings) < self.l_analyze_n_photos) and (not l_user_private):
            if l_instagram_followings:
                while x_next:
                    try:
                        l_next_followings, x_next = self.l_instagram_api.api.user_follows(with_next_url = x_next)
                    except InstagramAPIError as e:
                        logging.exception("get_best_instagram_followings: ERR-00064 Instagram API Error %s : %s" % (e.status_code, e.error_message))
                    except InstagramClientError as e:
                        logging.exception("get_best_instagram_followings: ERR-00065 Instagram Client Error %s : %s" % (e.status_code, e.error_message))
                    except IndexError:
                        logging.exception("get_best_instagram_followings: ERR-00066 Instagram search unsuccessful: %s" % (exc_info()[0]))
                    except:
                        logging.exception("get_best_instagram_followings: ERR-00067 Unexpected error: %s" % (exc_info()[0]))
                        raise


                    l_instagram_followings.extend(l_next_followings)
                    if len (l_instagram_followings) >= self.l_analyze_n_photos:
                        break

        for following in l_instagram_followings:
            '''Filter only the best followers'''
            l_exists = Following.objects.filter(instagram_user_id=following.id)
            l_user_private = False
            self.l_analyzed_followings += 1

            if l_exists.count() == 0:
                try:
                    l_user_data = self.l_instagram_api.api.user(following.id)
                except InstagramAPIError as e:

                    if (e.status_code == 400):
                        l_user_private = True
                        self.l_private_followings += 1
                    else:
                        logging.exception("get_best_instagram_followings: ERR-00068 Instagram API Error %s : %s" % (e.status_code, e.error_message))
                except InstagramClientError as e:
                    logging.exception("get_best_instagram_followings: ERR-00069 Instagram Client Error %s : %s" % (e.status_code, e.error_message))
                except IndexError:
                    logging.exception("get_best_instagram_followings: ERR-00070 Instagram search unsuccessful: %s" % (exc_info()[0]))
                except:
                    logging.exception("get_best_instagram_followings: ERR-00071 Unexpected error: %s" % (exc_info()[0]))
                    raise

                if (not l_user_private):
                    l_followings_media_count = l_user_data.counts[u'media']
                    l_followings_followings = l_user_data.counts[u'follows']
                    l_followings_followers = l_user_data.counts[u'followed_by']
                    if l_followings_followers != 0:
                        l_friends_ff_ratio = l_followings_followings / l_followings_followers
                    else:
                        l_friends_ff_ratio = 0

                    if (FOLLOWINGS_TR_MIN_MEDIA_COUNT <= l_followings_media_count <= FOLLOWINGS_TR_MAX_MEDIA_COUNT) and \
                            (FOLLOWINGS_TR_MIN_FOLLOWINGS <= l_followings_followings <= FOLLOWINGS_TR_MAX_FOLLOWINGS) and \
                            (FOLLOWINGS_TR_MIN_FOLLOWERS <= l_followings_followers <= FOLLOWINGS_TR_MAX_FOLLOWERS) and \
                            (FOLLOWINGS_TR_MIN_FF_RATIO <= l_friends_ff_ratio <= FOLLOWINGS_TR_MAX_FF_RATIO):

                        if self.is_user_active_in_last_n_days(following.id, FOLLOWINGS_TR_LAST_POST_BEFORE_DAYS):
                            '''User is active in last N days, passed all requirements
                               Add it to friends
                            '''

                            l_best_instagram_followings.extend([l_user_data])
            else:
                '''Following already in database'''
                self.l_already_followings += 1
                l_existing_instagram_followings.extend([following.id])
                '''Add new source'''
                #l_existing_following = get_object_or_404(Following(instagram_user_id=following.id))

                #if self.l_user_type == 'gooduser':
                #    l_gooduser = get_object_or_404(GoodUser(instagram_user_id=self.l_instgram_user_id))
                #    l_existing_following.gooduser.add(l_gooduser)
                #
                #if self.l_user_type == 'member':
                #    l_member = get_object_or_404(Member(instagram_user_id=self.l_instgram_user_id))
                #    l_existing_following.member.add(l_member)


                #pass

        return l_best_instagram_followings, l_existing_instagram_followings


class InstagramUserAdminUtils():
    '''Helper functions for Instagram users administrations'''

    l_find_top_n_photos = None
    l_search_last_photos = None

    l_analyzed_followers = 0
    l_found_friends = 0
    l_analyzed_goodusers = 0
    l_private_followers = 0

    l_instagram_api_limit = 0
    l_instagram_api_limit_start = 0
    l_instagram_api_limit_end = 0

    def analyze_instagram_user_find_friends(self, request, obj):
        ''' Analyze Instagram Users followers and find potential
           Friends.
        '''

        self.l_analyzed_followers = 0
        self.l_found_friends = 0
        self.l_analyzed_goodusers = 0
        self.l_private_followers = 0
        self.l_already_friends = 0
        buf = None

        #queryset = queryset.filter(to_be_processed_for_friends=True)

        if obj.to_be_processed_for_friends == True:
            ig_session = InstagramSession(p_is_admin=True, p_token='')
            ig_session.init_instagram_API()

            #self.l_instagram_api_limit_start, self.l_instagram_api_limit = \
            #    ig_session.get_api_limits()

            #for obj in queryset:
            obj.to_be_processed_for_friends = False
            obj.last_processed_friends_date = timezone.datetime.now()
            obj.times_processed_for_friends = obj.times_processed_for_friends + 1
            '''get Instagram user data'''
            self.l_instagram_api_limit_start, self.l_instagram_api_limit = \
                ig_session.get_api_limits()

            if (ig_session):
                '''We have Instagram session'''
                user_search = ig_session.is_instagram_user_valid(obj.instagram_user_name)

                if (len(user_search) > 0) and (user_search[0].username == obj.instagram_user_name):
                    instagram_user = ig_session.get_instagram_user(user_search[0].id)

                    if instagram_user:
                        l_instagram_user_id = instagram_user.id
                        l_number_of_followers = instagram_user.counts[u'followed_by']
                        if l_number_of_followers < FRIENDS_TR_ANALYZE_N_FRIENDS:
                            l_analyze_n_followers = l_number_of_followers
                        else:
                            l_analyze_n_followers = FRIENDS_TR_ANALYZE_N_FRIENDS

                        if (self.l_instagram_api_limit_start > (l_analyze_n_followers + 50)):
                            '''Do we have enough API requests available? Yes'''
                            if TEST_APP == '1':
                                '''Override for testing, analyze less followers'''
                                l_analyze_n_followers = TEST_APP_FRIENDS_TR_ANALYZE_N_FRIENDS

                            l_best_instagram_followers = \
                                BestFollowers(l_instagram_user_id, l_analyze_n_followers, ig_session)

                            l_instagram_friends, l_existing_instagram_friends = \
                                l_best_instagram_followers.get_best_instagram_followers()
                            self.l_analyzed_goodusers += 1
                            self.l_analyzed_followers += l_best_instagram_followers.l_analyzed_followers
                            self.l_private_followers += l_best_instagram_followers.l_private_followers
                            self.l_already_friends += l_best_instagram_followers.l_already_friends
                            if l_instagram_friends:
                                '''Found followers - save them to our database'''
                                for follower in l_instagram_friends:
                                    l_exists = Follower.objects.filter(instagram_user_id=follower.id)

                                    instagram_utils = InstagramUserAdminUtils()
                                    if l_exists.count() == 0:
                                        l_new_friend = \
                                            Follower(instagram_user_id=follower.id,
                                                     instagram_user_name=follower.username, instagram_user_name_valid=True,
                                                     instagram_user_full_name=follower.full_name,
                                                     instagram_profile_picture_URL=follower.profile_picture,
                                                     instagram_user_bio=follower.bio,
                                                     instagram_user_website_URL=follower.website,
                                                     is_user_active=True,
                                                     number_of_followers=follower.counts[u'followed_by'],
                                                     number_of_followings=follower.counts[u'follows'],
                                                     number_of_media=follower.counts[u'media'],
                                                     instagram_user_profile_page_URL=instagram_utils.generate_instagram_profile_page_URL(follower.username),
                                                     iconosquare_user_profile_page_URL=instagram_utils.generate_iconosquare_profile_page_URL(follower.id),
                                                     is_potential_friend=True
                                            )

                                        l_new_friend.save()
                                        l_new_friend.inspiringuser.add(obj)
                                    else:
                                        try:
                                            l_existing_follower = Follower.objects.get(instagram_user_id=follower.id)
                                            l_existing_follower.inspiringuser.add(obj)
                                            l_new_friend = l_existing_follower
                                        except ObjectDoesNotExist:
                                            l_existing_follower = None
                                            l_new_friend = None

                                        #add categories
                                    if obj.user_type == 'inspiring':
                                        l_categories = InspiringUserBelongsToCategory.objects.filter(
                                            instagram_user=obj,
                                        )
                                        l_attributes = InspiringUserBelongsToAttribute.objects.filter(
                                            instagram_user=obj,
                                        )

                                        for category in l_categories:
                                            try:
                                                l_follower_belongs_to_category_exists = \
                                                    FollowerBelongsToCategory.objects.get(
                                                        instagram_user=l_new_friend,
                                                        category=category.category,
                                                        frequency=1
                                                    )
                                            except ObjectDoesNotExist:
                                                l_follower_belongs_to_category_exists = None
                                            except:
                                                raise

                                            if not l_follower_belongs_to_category_exists:
                                                l_follower_belongs_to_category = FollowerBelongsToCategory(
                                                    instagram_user=l_new_friend,
                                                    category=category.category,
                                                    frequency=1
                                                )
                                                l_follower_belongs_to_category.save()
                                            else:
                                                l_follower_belongs_to_category_exists.frequency += 1
                                                l_follower_belongs_to_category_exists.save()

                                        for attribute in l_attributes:
                                            try:
                                                l_follower_belongs_to_attribute_exists = \
                                                    FollowerBelongsToAttribute.objects.get(
                                                        instagram_user=l_new_friend,
                                                        attribute=attribute.attribute
                                                    )
                                            except ObjectDoesNotExist:
                                                l_follower_belongs_to_attribute_exists = None
                                            except:
                                                raise

                                            if not l_follower_belongs_to_attribute_exists:
                                                l_follower_belongs_to_attribute = FollowerBelongsToAttribute(
                                                    instagram_user=l_new_friend,
                                                    attribute=attribute.attribute,
                                                    frequency=1
                                                )
                                                l_follower_belongs_to_attribute.save()
                                            else:
                                                l_follower_belongs_to_attribute_exists.frequency += 1
                                                l_follower_belongs_to_attribute_exists.save()


                                    self.l_found_friends += 1

                            if l_existing_instagram_friends:
                                for follower in l_existing_instagram_friends:
                                    l_existing = Follower.objects.filter(instagram_user_id=follower)

                                    if l_existing.count() != 0:
                                        l_existing = get_object_or_404(Follower, instagram_user_id=follower)
                                        if obj.user_type == 'inspiring':
                                            l_existing.inspiringuser.add(obj)
                                            l_existing.is_potential_friend = True
                                            l_existing.save()
                                        if obj.user_type == 'member':
                                            l_existing.member.add(obj)
                                            l_existing.save()
                        else:
                            buf = "Not enough Instagram API requests available (available %s, needed %s)" % \
                                  (self.l_instagram_api_limit_start, (l_analyze_n_followers + 50))
                            pass
            obj.save()

        self.l_instagram_api_limit_end, self.l_instagram_api_limit = \
            ig_session.get_api_limits()

        if not buf:
            buf = 'Analyzed %s Inspiring Users. Analyzed %s folowers. Found %s private followers.' \
                  ' Found %s new Friends (%s existing friends). Instagram API (%s - %s/%s / diff: %s)' \
                  % (self.l_analyzed_goodusers, self.l_analyzed_followers,
                     self.l_private_followers, self.l_found_friends, self.l_already_friends,
                     self.l_instagram_api_limit_start, self.l_instagram_api_limit_end,
                     self.l_instagram_api_limit,
                     (int(self.l_instagram_api_limit_start) - int(self.l_instagram_api_limit_end))
            )
        return buf
    analyze_instagram_user_find_friends.short_description = 'Find new friends from Instagram user'

    def analyze_instagram_user_find_followings(self, request, obj):
        """ Analyze Instagram Users followings and find potential
           Friends.
        """

        self.l_analyzed_followings = 0
        self.l_found_followings = 0
        self.l_analyzed_goodusers = 0
        self.l_private_followings = 0
        self.l_already_followings = 0
        buf = None
        ig_session = None

        #queryset = queryset.filter(to_be_processed_for_friends=True)

        if obj.to_be_processed_for_followings == True:
            ig_session = InstagramSession(
                p_is_admin=True, p_token=''
            )
            ig_session.init_instagram_API()

            self.l_instagram_api_limit_start, self.l_instagram_api_limit = \
                ig_session.get_api_limits()

            # for obj in queryset:
            obj.to_be_processed_for_followings = False
            obj.last_processed_for_followings_date = timezone.datetime.now()
            obj.times_processed_for_followings = obj.times_processed_for_followings + 1
            # get Instagram user data
            self.l_instagram_api_limit_start, self.l_instagram_api_limit = \
                ig_session.get_api_limits()

            if (ig_session):
                # We have Instagram session and enough API call remaining
                user_search = ig_session.is_instagram_user_valid(obj.instagram_user_name)

                if (len (user_search) > 0) and (user_search[0].username == obj.instagram_user_name):
                    instagram_user = ig_session.get_instagram_user(user_search[0].id)

                    if instagram_user:
                        l_instagram_user_id = instagram_user.id
                        l_number_of_followers = instagram_user.counts[u'followed_by']
                        if l_number_of_followers < FOLLOWINGS_TR_ANALYZE_N_FOLLOWINGS:
                            l_analyze_n_followers = l_number_of_followers
                        else:
                            l_analyze_n_followers = FOLLOWINGS_TR_ANALYZE_N_FOLLOWINGS

                        if (self.l_instagram_api_limit_start > (l_analyze_n_followers + 50)):

                            if TEST_APP == '1':
                                # Override for testing, analyze less followers
                                l_analyze_n_followers = TEST_APP_FRIENDS_TR_ANALYZE_N_FOLLOWINGS

                            l_best_instagram_followings = \
                                BestFollowings(l_instagram_user_id, obj.user_type,
                                               l_analyze_n_followers, ig_session
                                )

                            l_instagram_followings, l_existing_followings = \
                                l_best_instagram_followings.get_best_instagram_followings()
                            self.l_analyzed_goodusers += 1
                            self.l_analyzed_followings += l_best_instagram_followings.l_analyzed_followings
                            self.l_private_followings += l_best_instagram_followings.l_private_followings
                            self.l_already_followings += l_best_instagram_followings.l_already_followings
                            if l_instagram_followings:
                                # Found followers - save them to our database
                                for following in l_instagram_followings:
                                    # Friend does not exist - add new
                                    instagram_utils = InstagramUserAdminUtils()
                                    l_new_following = \
                                        Following(instagram_user_id=following.id,
                                                  instagram_user_name=following.username, instagram_user_name_valid=True,
                                                  instagram_user_full_name=following.full_name,
                                                  instagram_profile_picture_URL=following.profile_picture,
                                                  instagram_user_bio=following.bio,
                                                  instagram_user_website_URL=following.website,
                                                  is_user_active=True,
                                                  number_of_followers=following.counts[u'followed_by'],
                                                  number_of_followings=following.counts[u'follows'],
                                                  number_of_media=following.counts[u'media'],
                                                  instagram_user_profile_page_URL=instagram_utils.generate_instagram_profile_page_URL(following.username),
                                                  iconosquare_user_profile_page_URL=instagram_utils.generate_iconosquare_profile_page_URL(following.id)
                                        )
                                    l_new_following.save()
                                    if obj.user_type == 'inspiring':
                                        l_new_following.inspiringuser.add(obj)
                                        l_new_following.save()
                                    if obj.user_type == 'member':
                                        l_new_following.member.add(obj)
                                        l_new_following.save()
                                    self.l_found_followings += 1

                            if l_existing_followings:
                                for following in l_existing_followings:
                                    l_existing = Following.objects.filter(instagram_user_id=following)

                                    if l_existing.count() != 0:
                                        l_existing = get_object_or_404(Following, instagram_user_id=following)
                                        if obj.user_type == 'inspiring':
                                            l_existing.inspiringuser.add(obj)
                                            l_existing.save()
                                        if obj.user_type == 'member':
                                            l_existing.member.add(obj)
                                            l_existing.save()

                        else:
                            buf = "Not enough Instagram API requests available (available %s, needed %s)" % \
                                  (self.l_instagram_api_limit_start, (l_analyze_n_followers + 50))
                            pass

            obj.save()

        self.l_instagram_api_limit_end, self.l_instagram_api_limit = \
            ig_session.get_api_limits()

        if not buf:
            buf = 'Analyzed %s Inspiring Users. Analyzed %s followings. Found %s private followings.' \
                  ' Found %s new Followings (%s existing Followings). Instagram API (%s - %s/%s / diff: %s)' \
                  % (self.l_analyzed_goodusers, self.l_analyzed_followings,
                     self.l_private_followings, self.l_found_followings, self.l_already_followings,
                     self.l_instagram_api_limit_start, self.l_instagram_api_limit_end,
                     self.l_instagram_api_limit,
                     (int(self.l_instagram_api_limit_start) - int(self.l_instagram_api_limit_end))
            )
        return buf
    analyze_instagram_user_find_followings.short_description = 'Find Instagram user''s followings'

    def analyze_instagram_user(self, api, p_instagram_user):
        """Do the processing of Good User with Instagram API

           Parameters:
           p_gooduser - one GoodUser we want to process
        """
        buf = None
        user_search = None

        if api:
            user_search = api.is_instagram_user_valid(p_instagram_user.instagram_user_name)

        if (len(user_search) > 0) and (user_search[0].username == p_instagram_user.instagram_user_name):
            buf = 'Success'
            instagram_user = api.get_instagram_user(user_search[0].id)

            p_instagram_user.number_of_followers = instagram_user.counts[u'followed_by']
            p_instagram_user.number_of_followings = instagram_user.counts[u'follows']
            p_instagram_user.number_of_media = instagram_user.counts[u'media']
            p_instagram_user.instagram_user_name = instagram_user.username
            p_instagram_user.instagram_user_full_name = instagram_user.full_name
            p_instagram_user.instagram_user_id = instagram_user.id
            p_instagram_user.instagram_profile_picture_URL = instagram_user.profile_picture
            p_instagram_user.instagram_user_bio = instagram_user.bio
            p_instagram_user.instagram_user_website_URL = instagram_user.website
            p_instagram_user.instagram_user_name_valid = True
        else:
            p_instagram_user.instagram_user_name_valid = False
            buf = "analyze_gooduser: ERR-00008 Could not find user %s on Instagram." % (p_instagram_user.instagram_user_name)

        return p_instagram_user, buf

    def process_instagram_user(self, request, queryset):
        """Do what is needed to process a Instagram User with Instagram API
           Process only users that are marked to be processed -> to_be_processed==True
        """

        queryset = queryset.filter(
            Q(to_be_processed_for_basic_info=True) | \
            Q(to_be_processed_for_photos=True) | \
            Q(to_be_processed_for_friends=True) | \
            Q(to_be_processed_for_followings=True)
        )

        l_counter_for_basic_info = 0
        l_counter_for_friends = 0
        l_counter_for_followings = 0
        l_counter_pics = 0
        message_basic_info = None
        message_find_friends = None
        message_best_photos = None
        message_followings = None

        ig_session = InstagramSession(
            p_is_admin=True, p_token=''
        )
        ig_session.init_instagram_API()

        self.l_instagram_api_limit_start, self.l_instagram_api_limit = \
            ig_session.get_api_limits()

        for obj in queryset:
            if obj.to_be_processed_for_basic_info == True:
                obj.to_be_processed_for_basic_info = False
                obj.last_processed_date = timezone.datetime.now()
                obj.times_processed_for_basic_info = obj.times_processed_for_basic_info + 1
                instagram_utils = InstagramUserAdminUtils()
                obj.instagram_user_profile_page_URL = instagram_utils.generate_instagram_profile_page_URL(obj.instagram_user_name)
                obj.iconosquare_user_profile_page_URL = instagram_utils.generate_iconosquare_profile_page_URL(obj.instagram_user_id)
                # get Instagram user data
                obj, message_basic_info = self.analyze_instagram_user(ig_session, obj)
                l_counter_for_basic_info += 1
                obj.last_processed_for_basic_info_date = timezone.now()
                obj.save()

            # Analyze photos of this user
            if obj.to_be_processed_for_photos == True:
                if obj.user_type == 'inspiring':
                    self.l_find_top_n_photos = INSPIRING_USERS_FIND_TOP_N_PHOTOS
                    self.l_search_last_photos = INSPIRING_USERS_SEARCH_N_PHOTOS

                if obj.user_type == 'friend':
                    self.l_find_top_n_photos = FRIENDS_FIND_TOP_N_PHOTOS
                    self.l_search_last_photos = FRIENDS_SEARCH_N_PHOTOS

                if obj.user_type == 'member':
                    self.l_find_top_n_photos = MEMBERS_FIND_TOP_N_PHOTOS
                    self.l_search_last_photos = MEMBERS_SEARCH_N_PHOTOS

                if obj.user_type == 'following':
                    self.l_find_top_n_photos = FOLLOWINGS_FIND_TOP_N_PHOTOS
                    self.l_search_last_photos = FOLLOWINGS_SEARCH_N_PHOTOS

                if TEST_APP == '1':
                    # reduce number of photos to search
                    self.l_search_last_photos = 200

                l_best_photos = BestPhotos(obj.instagram_user_id, self.l_find_top_n_photos,
                                           self.l_search_last_photos, ig_session
                )
                l_best_photos.get_instagram_photos()
                l_top_photos = None
                if l_best_photos.l_user_has_photos:
                    l_polynom, l_max_days, l_min_days, l_max_likes, l_min_likes = l_best_photos.get_top_photos()
                    if l_polynom.order == 2:
                        obj.poly_theta_2 = l_polynom.coeffs[0]
                        obj.poly_theta_1 = l_polynom.coeffs[1]
                        obj.poly_theta_0 = l_polynom.coeffs[2]
                        obj.poly_min_days = l_min_days
                        obj.poly_max_days = l_max_days
                        obj.poly_min_likes = l_min_likes
                        obj.poly_max_likes = l_max_likes
                        obj.poly_order = 2
                    l_top_photos = l_best_photos.top_photos_list
                    obj.times_processed_for_photos = obj.times_processed_for_photos + 1
                    obj.last_processed_for_photos_date = timezone.now()
                obj.save()

                # Delete old best photos for this user
                if obj.user_type == 'inspiring':
                    Photo.objects.filter(inspiring_user_id=obj.pk).delete()
                if obj.user_type == 'follower':
                    Photo.objects.filter(friend_id=obj.pk).delete()
                if obj.user_type == 'member':
                    Photo.objects.filter(member_id=obj.pk).delete()
                if obj.user_type == 'following':
                    Photo.objects.filter(following_id=obj.pk).delete()

                # Insert new best photos for this user
                if l_top_photos:
                    for val in l_top_photos:
                        rec = None
                        if Photo.objects.filter(instagram_photo_id=val[0]).exists():

                            try:
                                rec = Photo.objects.get(instagram_photo_id=val[0])
                            except ObjectDoesNotExist:
                                rec = None
                            except:
                                raise

                            if obj.user_type == 'inspiring':
                                rec.inspiring_user_id=obj
                            if obj.user_type == 'follower':
                                rec.friend_id=obj
                            if obj.user_type == 'member':
                                rec.member_id=obj
                            if obj.user_type == 'following':
                                rec.following_id=obj
                            rec.save()
                        else:
                            if obj.user_type == 'inspiring':
                                rec = Photo(instagram_photo_id=val[0], photo_rating=val[1], inspiring_user_id=obj)
                            if obj.user_type == 'follower':
                                rec = Photo(instagram_photo_id=val[0], photo_rating=val[1], friend_id=obj)
                            if obj.user_type == 'member':
                                rec = Photo(instagram_photo_id=val[0], photo_rating=val[1], member_id=obj)
                            if obj.user_type == 'following':
                                rec = Photo(instagram_photo_id=val[0], photo_rating=val[1], following_id=obj)
                            rec.save()
                        l_counter_pics += 1

                obj.to_be_processed_for_photos = False

                obj.save()
                message_best_photos = 'Success'

            # Analyze followers of this user for friends
            if obj.to_be_processed_for_friends == True:
                message_find_friends = self.analyze_instagram_user_find_friends(request, obj)
                obj.to_be_processed_for_friends = False
                obj.times_processed_for_friends = obj.times_processed_for_friends + 1
                obj.last_processed_for_friends_date = timezone.now()
                obj.save()
                l_counter_for_friends += 1

            # Analyze followers of this user for followings
            if obj.to_be_processed_for_followings == True:
                message_followings = self.analyze_instagram_user_find_followings(request, obj)
                l_counter_for_followings += 1
                obj.times_processed_for_followings = obj.times_processed_for_followings + 1
                obj.to_be_processed_for_followings = False
                obj.last_processed_for_followings_date = timezone.now()
                obj.save()
                #message_followings = 'Success'
                pass

        self.l_instagram_api_limit_end, self.l_instagram_api_limit = \
            ig_session.get_api_limits()

        buf = '%s users processed for basic info (Messages "%s").' \
              ' Processed %s photos (Messages "%s").' \
              ' Processed %s users for friends (Messages "%s").' \
              ' Processed %s users for followings (Messages: "%s").' \
              ' Instagram API (%s - %s/%s / diff: %s)' % \
              (l_counter_for_basic_info, message_basic_info,
               l_counter_pics, message_best_photos,
               l_counter_for_friends, message_find_friends,
               l_counter_for_followings, message_followings,
               self.l_instagram_api_limit_start, self.l_instagram_api_limit_end,
               self.l_instagram_api_limit,
               (int(self.l_instagram_api_limit_start) - int(self.l_instagram_api_limit_end))
              )

        return buf
        #self.message_user(request, buf)
    process_instagram_user.short_description = 'Process Instagram User by Instagram API'

    def set_instagram_users_process_true(self, request, queryset):

        queryset = queryset.filter(to_be_processed_for_basic_info=False)
        l_counter = 0

        for obj in queryset:
            obj.to_be_processed_for_basic_info = True
            obj.save()
            l_counter += 1


        buf = '%s user(s) flagged to "To Be Processed for basic info" successfully.' \
              % (l_counter)

        return buf

    def set_instagram_users_process_false(self, request, queryset):

        queryset = queryset.filter(to_be_processed_for_basic_info=True)
        l_counter = 0

        for obj in queryset:
            obj.to_be_processed_for_basic_info = False
            obj.save()
            l_counter += 1

        buf = '%s user(s) flagged to "Not To Be Processed for basic info" successfully.' \
              % (l_counter)

        return buf

    def set_instagram_users_process_photos_true(self, request, queryset):

        queryset = queryset.filter(to_be_processed_for_basic_info=False)
        l_counter = 0

        for obj in queryset:
            obj.to_be_processed_for_photos = True
            obj.save()
            l_counter += 1

        buf = '%s user(s) flagged to "To Be Processed for photos" successfully.' \
              % (l_counter)

        return buf

    def set_instagram_users_process_photos_false(self, request, queryset):

        queryset = queryset.filter(to_be_processed_for_basic_info=True)
        l_counter = 0

        for obj in queryset:
            obj.to_be_processed_for_photos = False
            obj.save()
            l_counter += 1

        buf = '%s user(s) flagged to "Not To Be Processed for photos" successfully.' \
              % (l_counter)

        return buf

    def set_instagram_users_process_friends_true(self, request, queryset):

        queryset = queryset.filter(to_be_processed_for_basic_info=False)
        l_counter = 0

        for obj in queryset:
            obj.to_be_processed_for_friends = True
            obj.save()
            l_counter += 1

        buf = '%s user(s) flagged to "To Be Processed for Friends" successfully.' \
              % (l_counter)

        return buf

    def set_instagram_users_process_friends_false(self, request, queryset):

        queryset = queryset.filter(to_be_processed_for_basic_info=True)
        l_counter = 0

        for obj in queryset:
            obj.to_be_processed_for_friends = False
            obj.save()
            l_counter += 1

        buf = '%s user(s) flagged to "Not To Be Processed for Friends" successfully.' \
              % (l_counter)

        return buf

    def set_instagram_users_process_followings_true(self, request, queryset):

        queryset = queryset.filter(to_be_processed_for_basic_info=False)
        l_counter = 0

        for obj in queryset:
            obj.to_be_processed_for_followings = True
            obj.save()
            l_counter += 1

        buf = '%s user(s) flagged to "To Be Processed for Followings" successfully.' \
              % (l_counter)

        return buf

    def set_instagram_users_process_followings_false(self, request, queryset):

        queryset = queryset.filter(to_be_processed_for_basic_info=True)
        l_counter = 0

        for obj in queryset:
            obj.to_be_processed_for_followings = False
            obj.save()
            l_counter += 1

        buf = '%s user(s) flagged to "Not To Be Processed for Followings" successfully.' \
              % (l_counter)

        return buf

    def generate_instagram_profile_page_URL(self, p_instagram_user_name):
        """Generate Instagram.com profile page URL for the user

        Parameters:
        p_instagram_user_name: Instagram user name, used to generate URL for profile page

        Returns:
        URL of Instagram profile page for this GoodUser
        """

        l_instagram_profile_page_URL = 'http://www.instagram.com/%s' % (p_instagram_user_name)
        return l_instagram_profile_page_URL
    generate_instagram_profile_page_URL.short_description = 'Instagram profile page URL'

    def generate_iconosquare_profile_page_URL(self, p_instagram_user_id):
        """Generate Iconosquare.com profile page URL for the user

        Parameters:
        p_instagram_user_id: Instagram user ID, used to generate URL for profile page

        Returns:
        URL of Iconosquare profile page for this GoodUser
        """

        l_iconosquare_profile_page_URL = 'http://iconosquare.com/viewer.php#/user/%s/' % (p_instagram_user_id)
        return l_iconosquare_profile_page_URL
    generate_iconosquare_profile_page_URL.short_description = 'Iconosquare profile page URL'

    def get_instagram_photo_info(self, api, p_photo):
        """Retrieves information about on Instagram photo

        Parameters:
        api - Instagram session object
        p_photo - source Photo object
        Returns - object filled with Instagram photo information
        """

        l_photo = api.get_instagram_photo_info(p_photo.instagram_photo_id)

        if l_photo:
            p_photo.instagram_photo_valid = True
            p_photo.instagram_photo_id = l_photo.id
            p_photo.instagram_low_resolution_URL = \
                l_photo.get_low_resolution_url()
            p_photo.instagram_thumbnail_URL = l_photo.get_thumbnail_url()
            p_photo.instagram_standard_resolution_URL = \
                l_photo.get_standard_resolution_url()
            p_photo.instagram_link_URL = l_photo.link
            #l_cleaned_caption = self.cleanup_instagram_caption_text(l_photo.caption)
            try:
                p_photo.instagram_caption = l_photo.caption.text
            except:
                # no caption on the photo
                p_photo.instagram_caption = None
            #p_photo.instagram_tags = ','.join(l_photo.tags)
            p_photo.instagram_created_time = l_photo.created_time
            p_photo.instagram_likes = l_photo.like_count
            p_photo.instagram_comments = l_photo.comment_count
        else:
            p_photo.instagram_photo_valid = False

        return p_photo


    def process_photos_by_instagram_api(self, request, queryset):
        """Action -> process photos by Instagram API"""

        ig_session = InstagramSession(p_is_admin=True, p_token='')
        ig_session.init_instagram_API()

        self.l_instagram_api_limit_start, self.l_instagram_api_limit = \
            ig_session.get_api_limits()

        l_counter = 0

        for obj in queryset:
            l_instagram_api_limit_current, foo = ig_session.get_api_limits()  # @UnusedVariable
            if l_instagram_api_limit_current >= INSTAGRAM_API_THRESHOLD:
                obj = self.get_instagram_photo_info(ig_session, obj)
                obj.instagram_photo_processed = True
                obj.last_processed_date = timezone.datetime.now()
                obj.save()
                l_counter += 1

        self.l_instagram_api_limit_end, self.l_instagram_api_limit = \
            ig_session.get_api_limits()

        if l_counter == 1:
            buf = '1 photo processed successfully. Instagram API (%s - %s/%s / diff: %s)' % \
                  (self.l_instagram_api_limit_start, self.l_instagram_api_limit_end,
                   self.l_instagram_api_limit, (int(self.l_instagram_api_limit_start) - int(self.l_instagram_api_limit_end))
                  )
        else:
            buf = '%s photos processed successfully.  Instagram API (%s - %s/%s / diff: %s)' % \
                  (l_counter, self.l_instagram_api_limit_start, self.l_instagram_api_limit_end,
                   self.l_instagram_api_limit, (int(self.l_instagram_api_limit_start) - int(self.l_instagram_api_limit_end))
                  )

        return buf
    process_photos_by_instagram_api.short_description = 'Process photos by Instagram API'


class InstagramComments():
    """
    Class to read and send Instagram comments
    """

    instagram_photo_id = None
    comments = None
    instagram_session = None
    l_instagram_media = None
    l_instagram_media_owner = None

    def __init__(self, p_photo_id, p_instagram_session):
        self.instagram_photo_id = p_photo_id
        self.instagram_session = p_instagram_session

    def get_all_comments(self):
        """
        Returns all comments for an Instagram post with id self.instagram_photo_id
        :return:
        """

        l_media_comments = None
        l_instagram_thumbnail_url = None
        l_photo_caption = None

        try:
            if self.instagram_session:
                l_media_comments = self.instagram_session.api.media_comments(media_id=self.instagram_photo_id)
                self.l_instagram_media = self.instagram_session.api.media(media_id=self.instagram_photo_id)
                l_instagram_thumbnail_url = self.l_instagram_media.get_thumbnail_url()
                try:
                    l_photo_caption = self.l_instagram_media.caption.text
                except:
                    l_photo_caption = ''
                self.l_instagram_media_owner = self.l_instagram_media.user
        except InstagramAPIError as e:
            logging.exception("init_instagram_API: ERR-00110 Instagram API Error %s : %s" % (e.status_code, e.error_message))
            # self.message_user(request, buf, level=messages.WARNING)

        except InstagramClientError as e:
            logging.exception("init_instagram_API: ERR-00111 Instagram Client Error %s : %s" % (e.status_code, e.error_message))
            # self.message_user(request, buf, level=messages.WARNING)

        except:
            logging.exception("init_instagram_API: ERR-00112 Unexpected error: ")
            raise

        return l_media_comments, l_instagram_thumbnail_url, l_photo_caption

    def send_instagram_comment(self, p_comment_text):

        l_return = False
        l_client_secret = INSTAGRAM_CLIENT_SECRET

        try:
            if self.instagram_session:
                self.instagram_session.api.client_secret = l_client_secret
                self.instagram_session.api.client_ips = '127.0.0.1'
                l_media_comments = self.instagram_session.api.create_media_comment (
                    media_id=self.instagram_photo_id,
                    text=p_comment_text,
                    include_secret=True,
                )
                l_return = True

        except InstagramAPIError as e:
            logging.exception("init_instagram_API: ERR-00110 Instagram API Error %s : %s" % (e.status_code, e.error_message))
            # self.message_user(request, buf, level=messages.WARNING)

        except InstagramClientError as e:
            logging.exception("init_instagram_API: ERR-00111 Instagram Client Error %s : %s" % (e.status_code, e.error_message))
            # self.message_user(request, buf, level=messages.WARNING)

        except:
            logging.exception("init_instagram_API: ERR-00112 Unexpected error: ")
            raise

        return l_return

    def get_comments_count(self):
        l_comment_count = None
        try:
            self.l_instagram_media = self.instagram_session.api.media(media_id=self.instagram_photo_id)
            l_comment_count = self.l_instagram_media.comment_count
            self.l_instagram_media_owner = self.l_instagram_media.user
        except InstagramAPIError as e:
            logging.exception("init_instagram_API: ERR-00110 Instagram API Error %s : %s" % (e.status_code, e.error_message))
            # self.message_user(request, buf, level=messages.WARNING)

        except InstagramClientError as e:
            logging.exception("init_instagram_API: ERR-00111 Instagram Client Error %s : %s" % (e.status_code, e.error_message))
            # self.message_user(request, buf, level=messages.WARNING)

        except:
            logging.exception("init_instagram_API: ERR-00112 Unexpected error: ")
            raise

        return l_comment_count

    def process_instagram_comments(self, p_arrangement_type, l_comments):
        """

        :param p_arrangement_type:
        :type p_arrangement_type: 'list', 'thread'
        :param l_comments:
        :type l_comments: list of Instagram comments
        :return:
        :rtype: list of SquareSensor comments
        """

        l_comments_list = []
        l_order = 1
        l_resulting_list = None

        for x_comment in l_comments:
            # process text and replace with urls

            # 1. split into words
            l_comment_words = x_comment.text.split()
            l_cleaned_comment = ''
            l_references = ()  # which comments this comment references
            for x_word in l_comment_words:
                if x_word[0] == '#':
                    # this is hashtag - replace with our hashtag link
                    l_hashtag_text = x_word[1:]
                    if len(l_hashtag_text)<0:
                        x_word = '<a href="%s">%s</a>' % \
                                 (reverse('hashtags:hashtag_name', kwargs={'p_hashtag_name':l_hashtag_text}),
                                  x_word
                                 )
                if x_word[0] == '@':
                    # this is user - replace with our user link
                    l_username_text = x_word[1:]
                    l_username_text = l_username_text.strip(" .!#$%^&*()+=,;'"":/?")
                    try:
                        l_inspiring_user = InspiringUser.objects.get(instagram_user_name=l_username_text)
                    except ObjectDoesNotExist:
                        l_inspiring_user = None
                    except:
                        raise

                    # find reference - comment may be linked to previous comment
                    l_current_order = l_order
                    l_pom_cnt = 1
                    l_del = ','
                    l_last_reference = None
                    for c in l_comments:
                        if l_pom_cnt == 1 and self.l_instagram_media_owner.username == c.user.username:
                            pass  # skip the first comment - it is the post caption
                        else:
                            if c.user.username == l_username_text:
                                l_last_reference = l_pom_cnt

                        l_pom_cnt += 1
                        if l_pom_cnt == l_current_order:
                            if l_last_reference:
                                l_references += (str(l_last_reference),)
                                break

                    if l_inspiring_user:
                        if len(l_inspiring_user.instagram_user_name)<0:
                            x_word = '<a href="%s"><span class="glyphicon glyphicon-user"></span>%s</a>' % \
                                     (reverse('instagramuser:alltimebest',
                                              kwargs={'p_username': l_inspiring_user.instagram_user_name, 'p_mode': 'view'}
                                              ),
                                      x_word
                                     )
                    else:
                        if len(l_username_text)< 0:
                            x_word = '<a href="%s" target="_blank">@%s</a>' % \
                                     (reverse('instagramuser:any_user_recent_best',
                                              kwargs={'p_instagram_user_name': l_username_text}
                                              )
                                      , l_username_text)

                l_cleaned_comment += x_word + ' '

            l_is_photo_owner = False
            if self.l_instagram_media_owner.username == x_comment.user.username:
                l_is_photo_owner = True
            l_cleaned_comment = Emoji.replace_unicode(l_cleaned_comment)
            l_is_response = False
            l_comment_item = \
                [l_order,
                 l_cleaned_comment,
                 x_comment.user.username,
                 l_is_photo_owner,
                 l_references,
                 l_is_response,
                 x_comment.user.profile_picture
                ]
            l_order += 1

            l_comments_list.append(l_comment_item)

        if p_arrangement_type == 'thread':
            # we now have coments and references
            # let's build the comment section
            l_order = 1
            l_resulting_list = list(l_comments_list)
            if len(l_comments_list) > 0:
                for y_comment in l_comments_list:
                    # for each comment
                    if len(y_comment[4]) > 0:
                        for ref in y_comment[4]:
                            l_insert_idx = None
                            l_cnt_x = 1
                            for x in l_resulting_list:
                                if x[0] == int(ref):
                                    l_insert_idx = l_cnt_x
                                    break
                                else:
                                    l_cnt_x += 1
                            l_remove_idx = None
                            l_cnt_x = 1

                            if l_insert_idx:
                                new_element = y_comment[:]
                                new_element[5] = True
                                new_element[4] = ()
                                # remove the reply first
                                l_remove_idx = 1

                                l_resulting_list.insert(l_insert_idx, new_element)


                    l_order += 1

        # remove replies
        l_new_resulting_list = []
        for x in l_resulting_list:
            if len(x[4]) > 0 and (x[5] == False):
                pass
            else:
                l_new_resulting_list.append(x)

        return l_new_resulting_list

    def get_unanswered_comments(self, p_instagram_user_id):
        """
        Returns list of photos with unanswered comments
        p_instagram_user_id - photo owner id
        """

        l_media_comments, foo1, foo2 = self.get_all_comments()

        l_unanswered_comments_list = []
        l_order = 0
        l_unanswered_comments_and_posts = []

        #First scan all non owner comments
        for comment in l_media_comments:
            l_order += 1
            #check if comment is from owner of post
            l_is_owners_comment = False
            if comment.user.id == p_instagram_user_id:
                l_is_owners_comment = True
                continue

            l_time_diff = datetime.today() - comment.created_at
            l_time_diff_seconds = l_time_diff.seconds + (86400 * l_time_diff.days)
            l_diff = None
            if l_time_diff_seconds < 60:
                # less than minute
                l_diff = '<1 min'
            else:
                if l_time_diff_seconds < 3600:
                    # less than hour
                    l_minutes = l_time_diff_seconds // 60
                    l_diff = '%s min' % (l_minutes)
                else:
                    if l_time_diff_seconds < 86400:
                        l_hours = l_time_diff_seconds // 3660
                        l_diff = '%s h' % (l_hours)
                    else:
                        if l_time_diff_seconds < 604800:
                            l_days = l_time_diff_seconds // 86400
                            l_diff = '%s days' % (l_days)
                        else:
                            if l_time_diff_seconds > 604800:
                                l_days = l_time_diff_seconds // 86400
                                l_diff = '%s days' % (l_days)

            l_unanswered_comments_and_posts.append([l_order, comment, l_diff])

        l_return_unanswered_comments = []
        for unanswered_comment in l_unanswered_comments_and_posts:
            # check if some next comment contains reference to unanswered comment owner
            # if it does - it is answered

            l_order = 0
            is_answered = False
            for comment in l_media_comments:
                l_order += 1

                if l_order <= unanswered_comment[0]:
                    continue

                # we found later comment
                # check if it is owner's
                if comment.user.id == p_instagram_user_id:
                    # it is owner's comment - check if it contains any reference to unanswered comment's username
                    # if it does - we consider the comment answered
                    l_comment_words = comment.text.split()
                    for x_word in l_comment_words:
                        if x_word[0] == '@':
                            l_username_text = x_word[1:]
                            l_username_text = l_username_text.strip(" .!#$%^&*()+=,;'"":/?")
                            if l_username_text == unanswered_comment[1].user.username:
                                is_answered = True
                                break

            if not is_answered:
                l_return_unanswered_comments.extend([unanswered_comment])

        return l_return_unanswered_comments


class SmartFeedHelper():

    feed_owner_instagram_id = None
    recent_media = None
    instagram_session = None
    batch_size = None
    best_media_list = None
    is_user_private = False
    x_next = None
    last_media_id = None
    min_id = None
    date_from = None
    date_to = None

    def __init__(self,
                 p_feed_owner_instagram_id,
                 p_instagram_session,
                 p_batch_size,
                 p_min_id,
                 p_date_from = None,
                 p_date_to = None
    ):

        self.feed_owner_instagram_id = p_feed_owner_instagram_id
        self.instagram_session = p_instagram_session
        self.batch_size = p_batch_size
        self.min_id = p_min_id
        self.date_from = p_date_from
        self.date_to = p_date_to


    def get_recent_media(self, p_starting_media_id):

        self.recent_media = []
        l_user_private = False
        media_feed = None

        try:
            self.recent_media, self.x_next = self.instagram_session.api.user_media_feed (
                user_id=self.feed_owner_instagram_id,
                count=self.batch_size,
                max_id=p_starting_media_id,
                min_id=self.min_id
            )
        except InstagramAPIError as e:
            if (e.status_code == 400):
                l_user_private = True            # @UnusedVariable
            else:
                logging.exception("get_instagram_user: ERR-00040 Instagram API Error %s : %s" % (e.status_code, e.error_message))
        except InstagramClientError as e:
            logging.exception("get_instagram_user: ERR-00041 Instagram Client Error %s : %s" % (e.status_code, e.error_message))
        except IndexError:
            logging.exception("get_instagram_user: ERR-00042 Instagram search unsuccessful: %s" % (exc_info()[0]))
        except:
            logging.exception("get_instagram_user: ERR-00043 Unexpected error: %s" % (exc_info()[0]))
            raise

    def find_best_media(self, p_media_to_return, p_starting_media_id, p_logged_member, p_max_days):

        l_media_cnt = 0
        l_safety = 0
        self.best_media_list = []
        first_media = True

        self.instagram_session.get_api_limits()
        x_ratelimit_remaining, x_ratelimit = self.instagram_session.get_api_limits()
        l_max_days_reached = False


        while (l_media_cnt < p_media_to_return) and (l_safety < 1000) and (x_ratelimit_remaining > 100) \
                and (not l_max_days_reached):
            self.get_recent_media(p_starting_media_id=self.last_media_id)

            x_ratelimit_remaining, x_ratelimit = self.instagram_session.get_api_limits()

            if (len(self.recent_media) == 0):
                break

            for x_media in self.recent_media:
                self.last_media_id = x_media.id
                l_safety += 1
                l_author_instagram_id = x_media.user.id
                l_likes_cnt = x_media.like_count
                l_time_delta = datetime.today() - x_media.created_time
                l_days = l_time_delta.days

                if self.date_from and self.date_to:
                    if (x_media.created_time <= self.date_from):
                        l_max_days_reached = True
                        break
                    if (x_media.created_time >= self.date_to):
                        continue

                if l_days > p_max_days:

                    break

                if l_media_cnt >= p_media_to_return:
                    break

                try:
                    l_squarefollowing = SquareFollowing.objects.get(
                        instagram_user_id=l_author_instagram_id,
                        member_id2=p_logged_member
                    )
                    l_squarefollowing_level = SquareFollowingMember.objects.get(
                        squarefollowing=l_squarefollowing,
                        member=p_logged_member
                    ).squarefollowing_level
                except ObjectDoesNotExist:
                    l_squarefollowing = None
                    l_squarefollowing_level = None
                except:
                    raise


                if l_squarefollowing:
                    #normalize likes and age, poly values
                    if l_squarefollowing_level == 'G':
                        l_media_cnt += 1
                        self.best_media_list.extend([x_media])

                    if l_squarefollowing_level == 'Y':
                        if (l_squarefollowing.poly_max_likes - l_squarefollowing.poly_min_likes) != 0:
                            l_likes_cnt = (l_likes_cnt - l_squarefollowing.poly_min_likes) / \
                                     (l_squarefollowing.poly_max_likes - l_squarefollowing.poly_min_likes)
                        else:
                            l_likes_cnt = 0

                        if (l_squarefollowing.poly_max_days - l_squarefollowing.poly_min_days) != 0:
                            l_days = (l_days - l_squarefollowing.poly_min_days) / \
                                     (l_squarefollowing.poly_max_days - l_squarefollowing.poly_min_days)
                        else:
                            l_days = 0

                        l_prediction = l_squarefollowing.poly_theta_0 + l_squarefollowing.poly_theta_1*l_days + \
                                       l_squarefollowing.poly_theta_2*l_days*l_days

                        if l_prediction < l_likes_cnt:
                            l_media_cnt += 1
                            if p_logged_member.smartfeed_last_seen_instagram_photo_id != x_media.id:
                                self.best_media_list.extend([x_media])
                            if first_media:
                                if self.date_from is None and self.date_to is None:
                                    p_logged_member.smartfeed_last_seen_instagram_photo_id = x_media.id
                                    p_logged_member.save()
                                    first_media = False



        return self.best_media_list


def update_member_limits_f(req, logged_member):
    """
    Called by AJAX and every refresh
    :param req:
    :type req:
    :return:
    :rtype:
    """
    l_likes_in_last_minute = None
    l_comments_in_last_minute = None

    try:
        l_likes_in_last_minute = logged_member.likes_in_last_minute
        l_comments_in_last_minute = logged_member.comments_in_last_minute
        l_likes_in_last_minute_interval_start = logged_member.likes_in_last_minute_interval_start
        l_comments_in_last_minute_interval_start = logged_member.comments_in_last_minute_interval_start

        l_timedelta = timedelta(hours=+INSTAGRAM_LIMIT_PERIOD_RESET_TIME_HOURS)

        if l_likes_in_last_minute_interval_start:
            l_diff = timezone.now() - l_likes_in_last_minute_interval_start
            if l_diff > l_timedelta:
                #hour has passed - reset the counters
                logged_member.likes_in_last_minute = 0
                logged_member.likes_in_last_minute_interval_start = timezone.now()
                logged_member.save()
                l_likes_in_last_minute = 0
        else:
            logged_member.likes_in_last_minute = 0
            logged_member.likes_in_last_minute_interval_start = timezone.now()
            logged_member.save()
            l_likes_in_last_minute = 0

        if l_comments_in_last_minute_interval_start:
            l_diff = timezone.now() - l_likes_in_last_minute_interval_start
            if l_diff > l_timedelta:
                #hour has passed - reset the counters
                logged_member.comments_in_last_minute = 0
                logged_member.comments_in_last_minute_interval_start = timezone.now()
                logged_member.save()
                l_comments_in_last_minute = 0
        else:
            logged_member.comments_in_last_minute = 0
            logged_member.comments_in_last_minute_interval_start = timezone.now()
            logged_member.save()
            l_comments_in_last_minute = 0

        # New friends limits
        l_timedelta_day = timedelta(days=+FIND_FRIENDS_LIMIT_PERIOD_RESET_TIME_DAYS)
        l_new_friends_in_last_day_interval_start = logged_member.new_friends_in_last_day_interval_start
        if l_new_friends_in_last_day_interval_start:
            l_diff = timezone.now() - l_new_friends_in_last_day_interval_start
            if l_diff > l_timedelta_day:
                # hour has passed - reset the counters
                logged_member.new_friends_in_last_day = 0
                logged_member.new_friends_in_last_day_interval_start = timezone.now()
                logged_member.save()

        # Membership limits
        logged_member.check_membership_expired()

    except ObjectDoesNotExist:
        logged_member = None
    except:
        raise

    return l_likes_in_last_minute, l_comments_in_last_minute