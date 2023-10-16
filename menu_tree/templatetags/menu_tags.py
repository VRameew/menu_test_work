from django import template
from menu_tree.models import MenuItem

register = template.Library()

@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    request = context['request']
    active_url = request.path

    menu_items = MenuItem.objects.filter(name=menu_name).prefetch_related('children')

    def render_menu_item(menu_item):
        is_active = active_url.startswith(menu_item.url)
        children = menu_item.children.all()

        return {
            'menu_item': menu_item,
            'is_active': is_active,
            'children': [render_menu_item(child) for child in children]
        }

    menu_items = [render_menu_item(menu_item) for menu_item in menu_items if not menu_item.parent]

    return {
        'menu_items': menu_items
    }
