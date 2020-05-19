# coding: utf8
from sweet.tests import TestCase, User
from sweet.template import Template


class TestForm(TestCase):

    def setUp(self):
        self.user = User(id=1, name="ryanpoy", age=20, sex='F')

    def test_for_tag(self):
        t = Template("""
<%= using form(action="/user/new", method="POST", multipart=True, remote=False) do f %>
<% end %>
""")
        self.assertEqual("""
<form action="/user/new" method="POST" accept-charset="UTF8" enctype="multipart/form-data">
</form>
""", t.render())

    def test_for_model(self):
        t = Template("""
<%= using form(action="/user/new", model=user, method="POST", multipart=True, remote=False) do f %>
<% end %>
""")
        self.assertEqual("""
<form action="/user/new" method="POST" accept-charset="UTF8" enctype="multipart/form-data">
</form>
""", t.render(user=self.user))

    def test_form_with_url_and_ignore_multipart_if_method_is_not_POST(self):
        t = Template("""
<%= using form(action="/user/new", _id="user_new_id", method="GET", multipart=True, remote=False) do f %>
<% end %>
""")
        self.assertEqual("""
<form id="user_new_id" action="/user/new" method="GET" accept-charset="UTF8">
</form>
""", t.render())

    def test_form_with_url_and_html_id(self):
        t = Template("""
<%= using form(action="/user/new", method="POST", multipart=True, remote=False, html={"data-index": 10}) do f %>
<% end %>
""")
        self.assertEqual("""
<form action="/user/new" method="POST" accept-charset="UTF8" enctype="multipart/form-data" data-index="10">
</form>
""", t.render())


if __name__ == '__main__':
    import unittest
    unittest.main()
