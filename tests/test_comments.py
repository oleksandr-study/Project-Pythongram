import unittest
import sys
sys.path.insert(0, '../src')
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from src.models.models import Comment
from src.schemas.comments import CommentBase
from src.repository.comments import (get_comments, 
                                      get_comment, 
                                      create_comment, 
                                      update_comment, 
                                      delete_comment)  

class TestComments(unittest.IsolatedAsyncioTestCase):
    
    def setUp(self):
        self.session = MagicMock(spec=Session)

    async def test_get_comments(self):
        image_id = 1
        expected_comments = [Comment(id=1, comment='Comment', image_id=image_id, user_id=1)]

        self.session.query().filter().all.return_value = expected_comments

        result = await get_comments(image_id, self.session)

        self.assertEqual(result, expected_comments)

    async def test_get_comment(self):
        image_id = 1
        expected_comment = Comment(id=1, comment='Comment', image_id=image_id, user_id=1)

        self.session.query().filter().first.return_value = expected_comment

        result = await get_comment(image_id, self.session)

        self.assertEqual(result, expected_comment)

    async def test_create_comment(self):
        image_id = 1
        user_id = 1
        comment = CommentBase(comment='Comment')
        db_comment = Comment(id=1, comment=comment.comment, image_id=image_id, user_id=user_id)

        result = await create_comment(image_id=image_id, comment=comment, db=self.session, user_id=user_id)

        self.assertEqual(result.image_id, db_comment.image_id)
        self.assertEqual(result.comment, db_comment.comment)
        self.assertEqual(result.user_id, db_comment.user_id)

    async def test_update_comment(self):
        comment_id = 1
        user_id = 1
        body = CommentBase(comment='New comment')
        existing_comment = Comment(id=comment_id, comment='Comment', user_id=user_id, image_id=1)

        self.session.query().filter().first.return_value = existing_comment

        result = await update_comment(comment_id=comment_id, body=body, db=self.session, user_id=user_id)

        self.assertEqual(result.comment, body.comment)

    async def test_delete_comment(self):
        comment_id = 1
        existing_comment = Comment(id=comment_id, comment='Comment', user_id=1, image_id=1)

        self.session.query().filter().first.return_value = existing_comment

        result = await delete_comment(comment_id=comment_id, db=self.session)

        self.assertEqual(result, existing_comment)

if __name__ == '__main__':
    unittest.main()
