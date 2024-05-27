import unittest
from unittest.mock import MagicMock
from src.repository.tags import get_tags, get_tag, remove_tag
from src.models.models import Tag, User

class TestTagServices(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.db_session = MagicMock()

    async def test_get_tags(self):
        # Arrange
        skip = 0
        limit = 10
        user = User(id=1, username="testuser", email="testuser@example.com")
        expected_tags = [Tag(id=1, name="tag1"), Tag(id=2, name="tag2")]
        self.db_session.query().offset().limit().all.return_value = expected_tags

        # Act
        result = await get_tags(skip, limit, self.db_session, user)

        # Assert
        self.assertEqual(result, expected_tags)

    async def test_get_tag(self):
        # Arrange
        tag_id = 1
        user = User(id=1, username="testuser", email="testuser@example.com")
        expected_tag = Tag(id=tag_id, name="tag1")
        self.db_session.query().filter().first.return_value = expected_tag

        # Act
        result = await get_tag(tag_id, self.db_session, user)

        # Assert
        self.assertEqual(result, expected_tag)

    async def test_remove_tag(self):
        # Arrange
        tag_id = 1
        user = User(id=1, username="testuser", email="testuser@example.com")
        expected_tag = Tag(id=tag_id, name="tag1")
        self.db_session.query().filter().first.return_value = expected_tag
        self.db_session.commit = MagicMock()

        # Act
        result = await remove_tag(tag_id, self.db_session, user)

        # Assert
        self.assertEqual(result, expected_tag)
        self.assertTrue(self.db_session.delete.called)
        self.assertTrue(self.db_session.commit.called)

if __name__ == '__main__':
    unittest.main()
