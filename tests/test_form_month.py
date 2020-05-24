# coding: utf8
from unittest import TestCase
from sweet_view.template import Template
from .__init__ import User


class TestFormMonth(TestCase):

    def test_for_tag(self):

        t = Template("""
<%= using form("/user/new") do f %>
    <%= f.month("user_born_on") %>
<% end %>
""")
        self.assertEqual("""
<form action="/user/new" method="GET" accept-charset="UTF8">
    <input id="user_born_on" name="user_born_on" type="month" />
</form>
""", t.render())

        t = Template("""
<%= using form("/user/new") do f %>
    <%= f.month("user_born_on", "11") %>
<% end %>
""")
        self.assertEqual("""
<form action="/user/new" method="GET" accept-charset="UTF8">
    <input id="user_born_on" name="user_born_on" type="month" value="11" />
</form>
""", t.render())

        t = Template("""
<%= using form("/user/new") do f %>
    <%= f.month("user_born_on", _min="01") %>
<% end %>
""")
        self.assertEqual("""
<form action="/user/new" method="GET" accept-charset="UTF8">
    <input id="user_born_on" name="user_born_on" type="month" min="01" />
</form>
""", t.render())

    def test_for_model(self):

        t = Template("""
<%= using form("/user/new", model=user) do f %>
    <%= f.month("born_month") %>
<% end %>
""")
        self.assertEqual("""
<form action="/user/new" method="GET" accept-charset="UTF8">
    <input id="user_born_month" name="user['born_month']" type="month" value="12" />
</form>
""", t.render(user=User(born_month=12)))


if __name__ == '__main__':
    import unittest
    unittest.main()
