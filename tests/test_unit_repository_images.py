import unittest
import sys
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from src.models.models import Image, User, Role
from src.schemas.images import ImageBase
from src.repository.images import (get_all_images,
                                    get_images_by_id,
                                    get_images_by_user,
                                    create_image,
                                    remove_image)

class TestComments(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1, username="testuser", email="testuser@example.com", role = Role.admin)

    async def test_get_images_by_id_found(self):
        image_id = 1
        expected_images = [Image(id=1, image='Comment', user_id=1)]
        self.session.query().filter().all.return_value = expected_images
        result = await get_images_by_id(image_id, self.user, self.session)
        self.assertEqual(result, expected_images)

    async def test_get_images_by_id_not_found(self):
        image_id = 1
        self.session.query().filter().all.return_value = None
        result = await get_images_by_id(image_id, self.user, self.session)
        self.assertIsNone(result)


    async def test_get_images_by_user_found(self):
        user_id = 1
        expected_images = [Image(id=1, image='Comment', user_id=1)]
        self.session.query().filter().all.return_value = expected_images
        result = await get_images_by_user(user_id, self.session)
        self.assertEqual(result, expected_images)

    async def test_get_images_by_user_not_found(self):
        user_id = 1
        self.session.query().filter().all.return_value = None
        result = await get_images_by_user(user_id, self.session)
        self.assertIsNone(result)





    """async def test_create_image(self):

        description = "test"
        image_name = "http://test"
        db_image = Image(id=1, image="http://test", description=description, user_id=self.user.id)
        all_tags = "tag1, tag2"
        result = await create_image(image_name, description, self.user, all_tags, db=self.session)

        self.assertEqual(result.image_id, db_image.image_id)
        self.assertEqual(result.image, db_image.image)
        self.assertEqual(result.user_id, db_image.user_id)
        self.assertEqual(result.description, db_image.description)

    async def test_remove_image_found(self):
        image = Image()
        self.session.query().filter().all.return_value = image
        result = await remove_image(image_id=1, user=self.user, db=self.session)
        self.assertEqual(result, image)"""