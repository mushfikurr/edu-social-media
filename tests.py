"""
Unit Test for users on the website.
Used for development purposes only.
"""
from datetime import datetime, timedelta
import unittest
from lore import app, db
from lore.models import User, Post


class UserModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        """
        Tests the hashing of passwords
        """
        u = User(
            username='susan',
            email='susain@gmail.com',
            first_name='Susan',
            last_name='Da Vinci'
        )
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))

    def test_follow(self):
        """
        Tests the follow function
        """
        u1 = User(
            username='john',
            email='johnathan@gmail.com',
            first_name='John',
            last_name='Da Vinci'
        )
        u2 = User(
            username='susan',
            email='susain@gmail.com',
            first_name='Susan',
            last_name='Da Vinci'
        )
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        self.assertEqual(u1.followed.all(), [])
        self.assertEqual(u1.followers.all(), [])

        u1.follow(u2)
        db.session.commit()

        self.assertTrue(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 1)
        self.assertEqual(u1.followed.first().username, 'susan')
        self.assertEqual(u2.followers.count(), 1)
        self.assertEqual(u2.followers.first().username, 'john')

        u1.unfollow(u2)
        db.session.commit()

        self.assertFalse(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 0)
        self.assertEqual(u2.followers.count(), 0)

    def test_follow_posts(self):
        # create four users
        u1 = User(
            username='john',
            email='johnathan@gmail.com',
            first_name='John',
            last_name='Da Vinci'
        )
        u2 = User(
            username='susan',
            email='susain@gmail.com',
            first_name='Susan',
            last_name='Da Vinci'
        )
        u3 = User(
            username='mary',
            email='mary@gmail.com',
            first_name='Mary',
            last_name='Da Vinci'
        )
        u4 = User(
            username='david',
            email='david@gmail.com',
            first_name='David',
            last_name='Da Vinci'
        )
        db.session.add_all([u1, u2, u3, u4])

        # create four posts
        now = datetime.utcnow()
        p1 = Post(title="susie",
                  body="post from john", author=u1,
                  publish_date=now + timedelta(seconds=1))
        p2 = Post(title="susie",
                  body="post from susan", author=u2,
                  publish_date=now + timedelta(seconds=4))
        p3 = Post(title="susie",
                  body="post from mary", author=u3,
                  publish_date=now + timedelta(seconds=3))
        p4 = Post(title="susie",
                  body="post from david", author=u4,
                  publish_date=now + timedelta(seconds=2))
        db.session.add_all([p1, p2, p3, p4])
        db.session.commit()

        # setup the followers
        u1.follow(u2)  # john follows susan
        u1.follow(u4)  # john follows david
        u2.follow(u3)  # susan follows mary
        u3.follow(u4)  # mary follows david
        db.session.commit()

        # check the followed posts of each user
        f1 = u1.followed_posts().all()
        f2 = u2.followed_posts().all()
        f3 = u3.followed_posts().all()
        f4 = u4.followed_posts().all()
        self.assertEqual(f1, [p2, p4, p1])
        self.assertEqual(f2, [p2, p3])
        self.assertEqual(f3, [p3, p4])
        self.assertEqual(f4, [p4])


if __name__ == '__main__':
    unittest.main(verbosity=2)
