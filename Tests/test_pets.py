import os.path
from api import Pets

pt = Pets()


def test_get_token():
    status = pt.get_token()[1]
    assert status == 200


def test_list_users():
    status = pt.get_list_users()[0]
    amount = pt.get_list_users()[1]
    assert status == 200
    assert amount


def test_post_pet():
    status = pt.post_pet()[1]
    pet_id = pt.post_pet()[0]
    assert status == 200
    assert pet_id


def test_post_pet_photo():
    status = pt.post_pet_photo()
    assert status == 200


def test_list_of_pets_for_user():
    status = pt.get_pets_of_user()[1]
    amount = pt.get_pets_of_user()[2]
    assert status == 200
    assert amount


def test_put_like_to_pet():
    status = pt.put_like_to_pet()
    print(status)
    assert status == 200


def test_put_comment_to_pet():
    status = pt.put_comment_to_pet()
    print(status)
    assert status == 200


def test_get_pet_info():
    status = pt.get_pet_info()[1]
    pet_id = pt.get_pet_info()[0]
    assert status == 200
    assert pet_id


def test_update_pet_age():
    status = pt.update_pet_age()
    assert status == 200


def test_delete_pet():
    status = pt.delete_pet()[0]
    assert status == 200





