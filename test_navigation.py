import logging

import pytest

from .navigation import OrderNavigationSystem

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Sample data
data = [
        [{"id": 1, "name": "Item 1", "state": None, "handlers": []}, {"id": 2, "name": "Item 2", "state": None, "handlers": []}, {"id": 3, "name": "Item 3", "state": None, "handlers": []}],
        [{"id": 4, "name": "Item 4", "state": None, "handlers": []}, {"id": 5, "name": "Item 5", "state": "view", "handlers": ["ZAC"]}, {"id": 6, "name": "Item 6", "state": "view", "handlers": ["JOHN", "TOM"]}, {"id": 7, "name": "Item 7", "state": None, "handlers": []}],
        [{"id": 8, "name": "Item 8", "state": "view", "handlers": ["aaa"]}, {"id": 9, "name": "Item 9", "state": "view", "handlers": ["bbb"]}],
        [{"id": 10, "name": "Item 10", "state": None, "handlers": []}, {"id": 11, "name": "Item 11", "state": None, "handlers": []}, {"id": 12, "name": "Item 12", "state": None, "handlers": []}],
        [{"id": 13, "name": "Item 13", "state": None, "handlers": []}, {"id": 14, "name": "Item 14", "state": None, "handlers": []}, {"id": 15, "name": "Item 15", "state": None, "handlers": []}, {"id": 16, "name": "Item 16", "state": None, "handlers": []}, {"id": 17, "name": "Item 17", "state": None, "handlers": []}]
]

handler_name = "John"

def test_initialize_group_navigation_group_nav_true():
    nav_system = OrderNavigationSystem(data, handler_name, group_navigation=True)
    assert nav_system.group_navigation is True
    assert nav_system.get_current_state()['current_group'] == 0

def test_initialize_group_navigation_group_nav_false():
    nav_system = OrderNavigationSystem(data, handler_name, group_navigation=False)
    assert nav_system.group_navigation is False
    assert nav_system.get_current_state()['current_group'] == 0

def test_next_item():
    nav_system = OrderNavigationSystem(data, handler_name, group_navigation=False)
    initial_item = nav_system.get_current_item()
    nav_system.next_item()
    next_item = nav_system.get_current_item()
    assert next_item != initial_item and next_item['name'] == 'Item 2'

def test_previous_item():
    nav_system = OrderNavigationSystem(data, handler_name, group_navigation=False)
    nav_system.next_item()  # Move to the second item
    second_item = nav_system.get_current_item()
    nav_system.previous_item()
    assert nav_system.get_current_item() != second_item
    assert nav_system.get_current_item()['name'] == 'Item 1'


def test_next_page():
    nav_system = OrderNavigationSystem(data, handler_name, group_navigation=True)
    initial_page = nav_system.get_current_state()['current_group']
    nav_system.next_page()
    assert nav_system.get_current_state()['current_group'] != initial_page


def test_previous_page():
    nav_system = OrderNavigationSystem(data, handler_name, group_navigation=True)
    nav_system.next_page()  # Move to the second group
    second_group = nav_system.get_current_state()['current_group']
    nav_system.previous_page()
    assert nav_system.get_current_state()['current_group'] != second_group


def test_toggle_autoprint():
    nav_system = OrderNavigationSystem(data, handler_name, group_navigation=False, auto_print=False)
    nav_system.toggle_autoprint()
    assert nav_system.auto_print is True


def test_mark_current_item_as_complete():
    nav_system = OrderNavigationSystem(data, handler_name, group_navigation=False)
    current_item = nav_system.get_current_item()
    nav_system.mark_current_item_as_complete()
    assert 'state' in current_item and current_item['state'] == 'completed'


def test_next_item_at_end():
    nav_system = OrderNavigationSystem(data, handler_name, group_navigation=False)
    for _ in range(len(data[-1])):
        nav_system.next_item()
    last_item = nav_system.get_current_item()
    nav_system.next_item()
    assert nav_system.get_current_item() == last_item  # Should stay at the last item


def test_previous_item_at_start():
    nav_system = OrderNavigationSystem(data, handler_name, group_navigation=False)
    nav_system.previous_item()
    first_item = nav_system.get_current_item()
    assert nav_system.get_current_item() == first_item  # Should stay at the first item


def test_toggle_group_navigation():
    nav_system = OrderNavigationSystem(data, handler_name, group_navigation=False)
    nav_system.toggle_group_navigation()
    assert nav_system.group_navigation is True
    nav_system.toggle_group_navigation()
    assert nav_system.group_navigation is False


def test_next_when_autoprint_true_and_group_nav_false():
    nav_system = OrderNavigationSystem(data, handler_name, auto_print=True, group_navigation=False)
    nav_system.start(0)
    current_item = nav_system.get_current_item()
    assert current_item['state'] == 'completed' and current_item['name'] == 'Item 1'
    nav_system.next_item()
    current_item = nav_system.get_current_item()
    assert current_item['state'] == 'completed' and current_item['name'] == 'Item 2'
    nav_system.next_item()
    current_item = nav_system.get_current_item()
    assert current_item['state'] == 'completed' and current_item['name'] == 'Item 3'
    nav_system.next_item()
    current_item = nav_system.get_current_item()
    assert current_item['state'] == 'completed' and current_item['name'] == 'Item 3'
    


# def test_previous_when_autoprint_true_and_group_nav_false():
#     nav_system = OrderNavigationSystem(data, handler_name, auto_print=True, group_navigation=False)
#     nav_system.next_item()
#     current_item = nav_system.get_current_item()
#     assert current_item['state'] == 'completed' and  current_item['name'] == 'Item 1'
#     nav_system.next_item()
#     current_item = nav_system.get_current_item()
#     assert current_item['state'] == 'completed' and  current_item['name'] == 'Item 2'
    


    # assert current_item['state'] == 'completed' and nav_system.get_current_item()['name'] == 'Item 2'
    # nav_system.next_item()
    # current_item = nav_system.get_current_item()
    # assert current_item['state'] == 'completed' and current_item['name'] == 'Item 3'
    # nav_system.previous_item()
    # current_item = nav_system.get_current_item()
    # assert current_item['state'] == 'completed' and current_item['name'] == 'Item 2'
    # nav_system.previous_item()
    # current_item = nav_system.get_current_item()
    # assert current_item['state'] == 'completed' and current_item['name'] == 'Item 1'
    # nav_system.previous_item()
    # current_item = nav_system.get_current_item()
    # assert current_item['state'] == 'completed' and current_item['name'] == 'Item 1'









def test_next_when_autoprint_true_and_group_nav_true():
    nav_system = OrderNavigationSystem(data, handler_name, group_navigation=True, auto_print=True)
    current_item = nav_system.get_current_item()
    assert current_item['state'] == 'completed' and current_item['name'] == 'Item 1'

    nav_system.next_page()
    current_item = nav_system.get_current_item()
    assert current_item['state'] == 'completed' and current_item['name'] == 'Item 4'

# # def test_next_when_autoprint_true_and_group_nav_true():
# # #     # ISSUE: returns the last item in the current group instead the first 
# #     nav_system = OrderNavigationSystem(data, handler_name, group_navigation=True, auto_print=True)
# #     nav_system.print_data()
# #     current_item = nav_system.get_current_item()
# #     assert current_item['state'] == 'completed' and current_item['name'] == 'Item 1'
# #     nav_system.next_page()
# #     current_item = nav_system.get_current_item()
# #     assert current_item['name'] == 'Item 2' and current_item['state'] == 'completed'



def test_mark_completed_item():
    nav_system = OrderNavigationSystem(data, handler_name, group_navigation=False)
    nav_system.mark_current_item_as_complete()
    first_mark = nav_system.get_current_item()['state']
    nav_system.mark_current_item_as_complete()
    second_mark = nav_system.get_current_item()['state']
    assert first_mark == second_mark == 'completed'


def test_empty_data():
    empty_data = []
    with pytest.raises(ValueError, match="'data' is empty."):
        OrderNavigationSystem(empty_data, handler_name, group_navigation=False)


def test_reset_current_item():
    nav_system = OrderNavigationSystem(data, handler_name, group_navigation=False)
    nav_system.start(0)
    nav_system.mark_current_item_as_complete()
    assert nav_system.get_current_item()['state'] == 'completed'
    nav_system.reset_current_item()
    assert nav_system.get_current_item()['state'] is None
    assert nav_system.get_current_item()['name'] == 'Item 1'
    assert nav_system.get_current_item()['handlers'] == []

def test_reset_current_group():
    nav_system = OrderNavigationSystem(data, handler_name, group_navigation=True)
    nav_system.start(0)
    nav_system.mark_current_item_as_complete()
    current_item = nav_system.get_current_item()
    assert current_item['state'] == 'completed' and current_item['name'] == 'Item 1'
    nav_system.next_item()
    nav_system.mark_current_item_as_complete()
    current_item = nav_system.get_current_item()
    assert current_item['state'] == 'completed' and current_item['name'] == 'Item 2'
    nav_system.next_item()
    nav_system.mark_current_item_as_complete()
    current_item = nav_system.get_current_item()
    assert current_item['state'] == 'completed' and current_item['name'] == 'Item 3'
    nav_system.reset_current_group()
    for item in nav_system.get_current_group():
        assert item['state'] is None
        assert item['handlers'] == []

def test_reset_all():
    nav_system = OrderNavigationSystem(data, handler_name, group_navigation=True)
    nav_system.start(0)
    nav_system.mark_current_item_as_complete()
    current_item = nav_system.get_current_item()
    assert current_item['state'] == 'completed' and current_item['name'] == 'Item 1'
    nav_system.next_item()
    nav_system.mark_current_item_as_complete()
    current_item = nav_system.get_current_item()
    assert current_item['state'] == 'completed' and current_item['name'] == 'Item 2'
    nav_system.next_item()
    nav_system.mark_current_item_as_complete()
    current_item = nav_system.get_current_item()
    assert current_item['state'] == 'completed' and current_item['name'] == 'Item 3'
    nav_system.next_page()
    nav_system.mark_current_item_as_complete()
    current_item = nav_system.get_current_item()
    assert current_item['state'] == 'completed' and current_item['name'] == 'Item 4'
    nav_system.next_item()
    nav_system.mark_current_item_as_complete()
    current_item = nav_system.get_current_item()
    assert current_item['state'] == 'completed' and current_item['name'] == 'Item 5'
    nav_system.next_item()
    nav_system.mark_current_item_as_complete()
    current_item = nav_system.get_current_item()
    assert current_item['state'] == 'completed' and current_item['name'] == 'Item 6'
    nav_system.next_item()
    nav_system.mark_current_item_as_complete()
    current_item = nav_system.get_current_item()
    assert current_item['state'] == 'completed' and current_item['name'] == 'Item 7'
    nav_system.reset_all()
    for group in nav_system.data:
        for item in group:
            assert item['state'] is None
            assert item['handlers'] == []


if __name__ == "__main__":
    pytest.main()