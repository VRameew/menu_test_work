from django.test import TestCase
from django.urls import reverse
from .models import MenuItem


class MenuTestCase(TestCase):
    def setUp(self):
        self.menu_item_1 = MenuItem.objects.create(name='Menu Item 1', url='/menu-item-1/')
        self.menu_item_2 = MenuItem.objects.create(name='Menu Item 2', url='/menu-item-2/')
        self.menu_item_3 = MenuItem.objects.create(name='Menu Item 3', url='/menu-item-3/', parent=self.menu_item_1)
        self.menu_item_4 = MenuItem.objects.create(name='Menu Item 4', url='/menu-item-4/', parent=self.menu_item_1)

    def test_menu_item_str(self):
        self.assertEqual(str(self.menu_item_1), 'Menu Item 1')

    def test_menu_item_has_children(self):
        self.assertTrue(self.menu_item_1.children.exists())

    def test_menu_item_has_no_children(self):
        self.assertFalse(self.menu_item_2.children.exists())

    def test_draw_menu(self):
        response = self.client.get(reverse('menu'))
        self.assertContains(response, 'Menu Item 1')
        self.assertContains(response, 'Menu Item 2')
        self.assertContains(response, 'Menu Item 3')
        self.assertContains(response, 'Menu Item 4')