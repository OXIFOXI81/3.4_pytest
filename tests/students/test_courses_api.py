import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from model_bakery import baker

from students.models import Student,Course


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def student_1():
    return Student.objects.create('Oxana')



@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)

    return factory



@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return factory


@pytest.mark.django_db
def test_get_course(client, course_factory):
    #Arrange
    course = course_factory(name='API')
    url = f'/courses/{course.id}/'
    #Act
    response = client.get(url)
    #Assert
    assert response.status_code == 200
    data=response.json()
    assert data['name']=='API'

@pytest.mark.django_db
def test_list_courses(client, course_factory):
    # Arrange
    # students=student_factory(_quantity=5)
    courses = course_factory(_quantity=10)

    # Act
    response = client.get('/courses/')

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(courses)
    for i, m in enumerate(data):
         assert m['name'] == courses[i].name


@pytest.mark.django_db
# def test_create_course(client,student_1):
#     response=client.post('/courses/',data={'name':'Django','students':[student_1.id]})
#     assert response.status_code==201

def test_create_course(client):

    response=client.post('/courses/',data={'name':'Django'})
    assert response.status_code==201

@pytest.mark.django_db
def test_update_course(client, course_factory):
    course = course_factory(name='API')
    data = {
        'name': 'Django'

    }

    url = f'/courses/{course.id}/'
    response = client.patch(url, data)
    course.refresh_from_db()

    assert response.status_code == 200

    assert course.name == 'Django'

@pytest.mark.django_db
def test_delete_course(client, course_factory):
    course = course_factory(name='API')
    url = f'/courses/{course.id}/'
    response = client.delete(url)
    print(response.status_code)
    assert response.status_code == 204

@pytest.mark.django_db
def test_filter_course(client, course_factory):
    course_1 = course_factory(name='API', id='1')
    course_2 = course_factory(name='Django', id='2')

    filter = 'API'
    url = f'/courses/?name={filter}'

    response = client.get(url)

    assert len(response.data) == 1
    assert response.data[0]['name'] == 'API'

    filter = 2
    url = f'/courses/?id={filter}'

    response = client.get(url)

    assert len(response.data) == 1
    assert response.data[0]['id'] == 2