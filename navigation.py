"""
Order Navigation System
-----------------------
This class is used to navigate through a list of items in a specific order.
The items should be grouped and the navigation can be done by groups or by
individual items. The items can be marked as viewed or completed. The class
also allows for auto-printing the items when they are viewed by setting auto_print=True

The class has the following methods:
- next_item(): Move to the next item in the list.
- previous_item(): Move to the previous item in the list.
- next_page(): Move to the next group of items.
- previous_page(): Move to the previous group of items.
- get_current_state(): Get the current state of the navigation system.
- get_current_item(): Get the current item.
- toggle_autoprint(): Toggle the auto-print feature.
- mark_current_item_as_complete(): Mark the current item as completed.

The class takes the following parameters:
- data: A list of lists containing dictionaries with information about the items.
- handler_name: The name of the handler using the navigation system.
- group_navigation: A boolean value indicating whether to navigate by groups or by individual items.
- auto_print: A boolean value indicating whether to auto-print the items when they are viewed.

Example Usage:
--------------
data = [
    [{"id": 1, "name": "Item 1"}, {"id": 2, "name": "Item 2"}, {"id": 3, "name": "Item 3"}],
    [{"id": 4, "name": "Item 4"}, {"id": 5, "name": "Item 5"}, {"id": 6, "name": "Item 6"}, {"id": 7, "name": "Item 7"}],
    [{"id": 8, "name": "Item 8"}, {"id": 9, "name": "Item 9"}],
    [{"id": 10, "name": "Item 10"}, {"id": 11, "name": "Item 11"}, {"id": 12, "name": "Item 12"}],
    [{"id": 13, "name": "Item 13"}, {"id": 14, "name": "Item 14"}, {"id": 15, "name": "Item 15"}]
]

handler_name = "John"
nav_system = OrderNavigationSystem(data, handler_name, group_navigation=False)

nav_system.next_item()
nav_system.previous_item()
nav_system.next_page()
nav_system.previous_page()
nav_system.continue_item()
nav_system.get_current_state()
nav_system.get_current_item()
nav_system.toggle_autoprint()
nav_system.mark_current_item_as_complete()
"""

import json
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(lineno)d')

ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)


class OrderNavigationSystem:
    def __init__(self, data, handler_name, group_navigation=False, auto_print=False):
        self.data = data
        self.current_group = 0
        self.current_order = 0
        self.group_navigation = group_navigation
        self.handler_name = handler_name
        self.auto_print = auto_print
        self._view_current_item()

        if len(data) == 0:
            raise ValueError("Data should not be empty.")
        
        if not isinstance(data, list):
            raise ValueError("Data should be a list of lists.")
        
        for group in data:
            if not isinstance(group, list):
                raise ValueError("Each group in data should be a list.")
            for item in group:
                if not isinstance(item, dict):
                    raise ValueError("Each item in a group should be a dictionary.")
                if 'state' not in item:
                    raise ValueError("Each item should have a 'state' key.")
                if 'handlers' not in item:
                    raise ValueError("Each item should have a 'handlers' key.")
                if not isinstance(item['handlers'], list):
                    raise ValueError("Handlers should be a list.")
                if not isinstance(item['state'], (str, type(None))):
                    raise ValueError("State should be a string or None.")
                if item['state'] not in [None, 'view', 'completed']:
                    raise ValueError("State should be one of None, 'view', or 'completed'.")
                if not isinstance(item['id'], int):
                    raise ValueError("Item ID should be an integer.")

    def _view_current_item(self):
        item = self.get_current_item()
        if self.handler_name not in item['handlers']:
            item['handlers'].append(self.handler_name)
        if self.auto_print:
            item['state'] = 'completed'
        elif item['state'] != 'completed':
            item['state'] = 'view'

    def _leave_current_item(self):
        item = self.get_current_item()
        if self.handler_name in item['handlers']:
            item['handlers'].remove(self.handler_name)
        if not item['handlers'] and item['state'] != 'completed':
            item['state'] = None

    def _next_item_index(self):
        if not self.auto_print:
            if self.current_order < len(self.data[self.current_group]) - 1:
                return self.current_order + 1
            else:
                return None
        for i in range(self.current_order + 1, len(self.data[self.current_group])):
            item = self.data[self.current_group][i]
            if item['state'] != 'view':
                return i
        for i in range(self.current_order + 1, len(self.data[self.current_group])):
            item = self.data[self.current_group][i]
            if item['state'] == 'view':
                return i
        return None

    def _previous_item_index(self):
        if not self.auto_print:
            if self.current_order > 0:
                return self.current_order - 1
            else:
                return None
        for i in range(self.current_order - 1, -1, -1):
            item = self.data[self.current_group][i]
            if item['state'] != 'view':
                return i
        for i in range(self.current_order - 1, -1, -1):
            item = self.data[self.current_group][i]
            if item['state'] == 'view':
                return i
        return None

    def next_item(self):
        """Move to the next item in the list."""
        self._leave_current_item()
        next_index = self._next_item_index()
        if next_index is not None:
            self.current_order = next_index
        else:
            if self.group_navigation and self.current_group < len(self.data) - 1:
                self.current_group += 1
                self.current_order = 0
                while self.current_order < len(self.data[self.current_group]) and (
                        self.data[self.current_group][self.current_order]['state'] == 'view' or
                        self.data[self.current_group][self.current_order]['state'] == 'completed'):
                    self.current_order += 1
                if self.current_order >= len(self.data[self.current_group]):
                    logger.debug("All items in the next group are viewed or completed.")
                    self.current_order = 0
            else:
                logger.debug("You are at the last item in the current group.")
        self._view_current_item()

    def previous_item(self):
        """Move to the previous item in the list."""
        self._leave_current_item()
        prev_index = self._previous_item_index()
        if prev_index is not None:
            self.current_order = prev_index
        else:
            if self.group_navigation and self.current_group > 0:
                self.current_group -= 1
                self.current_order = len(self.data[self.current_group]) - 1
                while self.current_order >= 0 and (
                        self.data[self.current_group][self.current_order]['state'] == 'view' or
                        self.data[self.current_group][self.current_order]['state'] == 'completed'):
                    self.current_order -= 1
                if self.current_order < 0:
                    logger.debug("All items in the previous group are viewed or completed.")
                    self.current_order = len(self.data[self.current_group]) - 1
            else:
                logger.debug("You are at the first item in the current group.")
        self._view_current_item()

    def next_page(self):
        """Move to the next group of items."""
        self._leave_current_item()
        if self.current_group < len(self.data) - 1:
            self.current_group += 1
            self.current_order = 0
            while self.current_order < len(self.data[self.current_group]) and (
                    self.data[self.current_group][self.current_order]['state'] == 'view' or
                    self.data[self.current_group][self.current_order]['state'] == 'completed'):
                self.current_order += 1
            if self.current_order >= len(self.data[self.current_group]):
                self.current_order = 0
        else:
            logger.debug("You are at the last group.")
        self._view_current_item()

    def previous_page(self):
        """Move to the previous group of items."""
        self._leave_current_item()
        if self.current_group > 0:
            self.current_group -= 1
            self.current_order = len(self.data[self.current_group]) - 1
            while self.current_order >= 0 and (
                    self.data[self.current_group][self.current_order]['state'] == 'view' or
                    self.data[self.current_group][self.current_order]['state'] == 'completed'):
                self.current_order -= 1
            if self.current_order < 0:
                self.current_order = len(self.data[self.current_group]) - 1
        else:
            logger.debug("You are at the first group.")
        self._view_current_item()

    def continue_item(self):
        """Move to the next item in the current list that is not viewed or completed."""
        self._leave_current_item()
        for i in range(len(self.data[self.current_group])):
            if self.data[self.current_group][i]['state'] != 'view' and self.data[self.current_group][i]['state'] != 'completed':
                self.current_order = i
                self._view_current_item()
                return
        for i in range(len(self.data[self.current_group])):
            if self.data[self.current_group][i]['state'] == 'view':
                self.current_order = i
                self._view_current_item()
                return
        logger.debug("All items in the current group are viewed or completed.")
        self._view_current_item()

    def get_current_state(self):
        """Get the current state of the navigation system."""
        return {
            "current_group": self.current_group,
            "current_order": self.current_order,
            "item": self.get_current_item()
        }

    def get_current_item(self):
        """Get the current item."""
        if self.data == [] or self.data == [[]]:
            raise ValueError("'data' is empty.")
        elif self.data[self.current_group] == []:
            raise ValueError("Current group is empty.")
        elif self.current_group >= len(self.data):
            raise ValueError("Current group index is out of range.")
        return self.data[self.current_group][self.current_order]

    def toggle_autoprint(self):
        """Toggle the auto-print ON/OFF (True/False)."""
        self.auto_print = not self.auto_print
        logger.debug(f"Auto print toggled: {self.auto_print}")

    def toggle_group_navigation(self):
        """Toggle the group navigation ON/OFF (True/False)."""
        self.group_navigation = not self.group_navigation
        logger.debug(f"Group navigation toggled: {self.group_navigation}")

    def mark_current_item_as_complete(self):
        """Mark the current item as completed."""
        item = self.get_current_item()
        item['state'] = 'completed'
        logger.debug(f"Item {item['id']} marked as completed.")


def main():
    # Example data: List of lists containing dictionaries with state and handlers
    data = [
        [{"id": 1, "name": "Item 1", "state": None, "handlers": []}, {"id": 2, "name": "Item 2", "state": None, "handlers": []}, {"id": 3, "name": "Item 3", "state": None, "handlers": []}],
        [{"id": 4, "name": "Item 4", "state": None, "handlers": []}, {"id": 5, "name": "Item 5", "state": "view", "handlers": ["ZAC"]}, {"id": 6, "name": "Item 6", "state": "view", "handlers": ["JOHN", "TOM"]}, {"id": 7, "name": "Item 7", "state": None, "handlers": []}],
        [{"id": 8, "name": "Item 8", "state": "view", "handlers": ["aaa"]}, {"id": 9, "name": "Item 9", "state": "view", "handlers": ["bbb"]}],
        [{"id": 10, "name": "Item 10", "state": None, "handlers": []}, {"id": 11, "name": "Item 11", "state": None, "handlers": []}, {"id": 12, "name": "Item 12", "state": None, "handlers": []}],
        [{"id": 13, "name": "Item 13", "state": None, "handlers": []}, {"id": 14, "name": "Item 14", "state": None, "handlers": []}, {"id": 15, "name": "Item 15", "state": None, "handlers": []}, {"id": 16, "name": "Item 16", "state": None, "handlers": []}, {"id": 17, "name": "Item 17", "state": None, "handlers": []}]
    ]

    handler_name = input("Enter your handler name: ")
    nav_system = OrderNavigationSystem(data, handler_name, group_navigation=True)
    
    actions = ['toggle', 'print', 'next', 'prev', 'next_group', 'prev_group', 'state', 'exit', 'mode', 'data', 'settings']

    def print_data():
        print('\n\n', '=' * 50)
        for group in data:
            print(group)
            print('-' * 50)
        print('=' * 50, end='\n\n')

    def display_settings():
        print(f"Auto print: {nav_system.auto_print}")
        print(f"Handler name: {nav_system.handler_name}")
        print(f"Group navigation: {nav_system.group_navigation}")

    while True:
        action = input("Enter action: ")
        if not action:
            continue
        elif isinstance(action, str):
            action = action.lower().strip()
        elif action not in actions:
            print("Invalid action. Type 'help' to see available actions.")
            continue

        if action in ["help", "h"]:
            print("\nAvailable actions: \n\t", actions, '\n')
        elif action in ["tp", "toggle autoprint", "toggle_autoprint", "toggle_print", "toggle print"]:
            nav_system.toggle_autoprint()
            display_settings()
            # print_data()
        elif action in ["print"]:
            nav_system.mark_current_item_as_complete()
        elif action in ["next", "n"]:
            nav_system.next_item()
        elif action in ["prev", "p", "previous"]:
            nav_system.previous_item()
        elif action in ["next_group", "ng", "next_page", "np"]:
            nav_system.next_page()
        elif action in ["prev_group", "pg", "previous_page", "prev_page", "pp"]:
            nav_system.previous_page()
        elif action in ["state", "s"]:
            logger.debug(json.dumps(nav_system.get_current_state(), indent=4))
            continue
        elif action in ["exit", "e", "quit", "q"]:
            print("Exiting...")
            break
        elif action in ["toggle_nav", "tn", "toggle nav", "toggle navigation"]:
            nav_system.toggle_group_navigation()
            display_settings()
            print_data()
            # logger.debug(f"Navigation Mode changed: group_navigation={nav_system.group_navigation}")
            continue
        elif action in ["data", "d"]:
            print_data()
            continue
        elif action in ['settings', 'config', 'conf']:
            display_settings()
            continue
        elif action in ['continue', 'c']:
            nav_system.continue_item()
            

        # show whole dataset after each action
        print_data()
        
        
if __name__ == "__main__":
    main()
