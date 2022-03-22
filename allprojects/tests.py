from django.test import TestCase

# Create your tests here.
from django.contrib.auth.models import User
from django.test import TestCase
from .models import Project, Profile

class ProjectTestClass(TestCase):  # Project class test
    def setUp(self):
        user1 = User.objects.create(
            username="test", first_name="john", last_name="wick"
        )

        self.project = Project(
            title="Project 1",
            description="TestDescription",
            image="image.jpg",
            user=user1,
            url="https://www.linkedin.com/jobs/view/2948680713/"
        )

    def test_instance(self):
        self.assertTrue(isinstance(self.project, Project))

    def test_save_method(self):
        self.project.save_project()
        projects = Project.objects.all()
        self.assertTrue(len(projects) > 0)

    def test_delete_method(self):
        self.project.save_project()
        self.project.delete_project()
        projects = Project.objects.all()
        self.assertTrue(len(projects) == 0)


