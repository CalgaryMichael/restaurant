import datetime
import json
import pytest
import urllib.parse
from django.urls import reverse
from webapp.restaurant import choices, views
from . import utils


def _create_restaurant1():
    date = datetime.date(2018, 1, 1)
    restaurant = utils.create_restaurant(code="30004700", name="WENDY'S", type_slug="hamburgers")
    utils.create_restaurant_contact(
        restaurant=restaurant,
        boro=choices.Boro.BROOKLYN,
        building_number="100",
        street="123 Somewhere Ave.",
        zip_code="12345",
        phone="4445554444")
    utils.create_inspection(
        restaurant=restaurant,
        inspection_type="Cycle Inspection / Initial Inspection",
        date=date,
        score=14)
    utils.create_inspection(
        restaurant=restaurant,
        inspection_type="Cycle Inspection / Re-inspection",
        date=date + datetime.timedelta(days=30),
        grade_slug="a",
        score=10)
    return restaurant


def _create_restaurant2():
    date = datetime.date(2018, 3, 1)
    restaurant = utils.create_restaurant(code="30075445", name="MORRIS PARK BAKE SHOP", type_slug="bakery")
    utils.create_restaurant_contact(
        restaurant=restaurant,
        boro=choices.Boro.BRONX,
        building_number="1007",
        street="MORRIS PARK AVE",
        zip_code="10462",
        phone="7188924968")
    utils.create_inspection(
        restaurant=restaurant,
        inspection_type="Cycle Inspection / Initial Inspection",
        date=date,
        grade_slug="b",
        score=20)
    return restaurant


@pytest.mark.django_db
def test_restaurant_view_set__list__single_restaurant(client):
    restaurant = _create_restaurant1()
    response = client.get(reverse("restaurant-list"))
    expected_data = [
        {
            "id": restaurant.id,
            "code": "30004700",
            "name": "WENDY'S",
            "restaurant_type": "Hamburgers",
            "contact": {
                "boro": "brooklyn",
                "building_number": "100",
                "street": "123 Somewhere Ave.",
                "zip_code": "12345",
                "phone": "4445554444"
            },
            "inspections": [
                {
                    "inspection_date": "2018-01-01",
                    "score": 14,
                    "grade": None,
                    "grade_date": None
                },
                {
                    "inspection_date": "2018-01-31",
                    "score": 10,
                    "grade": "A",
                    "grade_date": "2018-01-31"
                }
            ]
        }
    ]
    assert response.status_code == 200
    assert json.loads(response.content)["results"] == expected_data


@pytest.mark.django_db
def test_restaurant_view_set__list__multiple_restaurants(client):
    restaurant1 = _create_restaurant1()
    restaurant2 = _create_restaurant2()

    response = client.get(reverse("restaurant-list"))
    expected_data = [
        {
            "id": restaurant1.id,
            "code": "30004700",
            "name": "WENDY'S",
            "restaurant_type": "Hamburgers",
            "contact": {
                "boro": "brooklyn",
                "building_number": "100",
                "street": "123 Somewhere Ave.",
                "zip_code": "12345",
                "phone": "4445554444"
            },
            "inspections": [
                {
                    "inspection_date": "2018-01-01",
                    "score": 14,
                    "grade": None,
                    "grade_date": None
                },
                {
                    "inspection_date": "2018-01-31",
                    "score": 10,
                    "grade": "A",
                    "grade_date": "2018-01-31"
                }
            ]
        },
        {
            "id": restaurant2.id,
            "code": "30075445",
            "name": "MORRIS PARK BAKE SHOP",
            "restaurant_type": "Bakery",
            "contact": {
                "boro": "bronx",
                "building_number": "1007",
                "street": "MORRIS PARK AVE",
                "zip_code": "10462",
                "phone": "7188924968"
            },
            "inspections": [
                {
                    "inspection_date": "2018-03-01",
                    "score": 20,
                    "grade": "B",
                    "grade_date": "2018-03-01"
                }
            ]
        }
    ]
    data = json.loads(response.content)
    assert response.status_code == 200
    assert data["count"] == 2
    assert data["results"] == expected_data


@pytest.mark.django_db
def test_restaurant_view_set__search__restaurant_type(client):
    _create_restaurant1()
    _create_restaurant2()

    params = urllib.parse.urlencode({"restaurant_type": "bakery"})
    url = reverse("restaurant-list") + "?{}".format(params)
    response = client.get(url)
    data = json.loads(response.content)

    assert response.status_code == 200
    assert data["count"] == 1
    assert data["results"][0]["code"] == "30075445"


@pytest.mark.django_db
def test_restaurant_view_set__minimum_grade__a(client):
    _create_restaurant1()
    _create_restaurant2()

    params = urllib.parse.urlencode({"minimum_grade": "a"})
    url = reverse("restaurant-list") + "?{}".format(params)
    response = client.get(url)
    data = json.loads(response.content)

    assert response.status_code == 200
    assert data["count"] == 1
    assert data["results"][0]["code"] == "30004700"


@pytest.mark.django_db
def test_restaurant_view_set__minimum_grade__b(client):
    _create_restaurant1()
    _create_restaurant2()

    params = urllib.parse.urlencode({"minimum_grade": "b"})
    url = reverse("restaurant-list") + "?{}".format(params)
    response = client.get(url)
    data = json.loads(response.content)

    assert response.status_code == 200
    assert data["count"] == 2
    assert data["results"][0]["code"] == "30004700"
    assert data["results"][1]["code"] == "30075445"
