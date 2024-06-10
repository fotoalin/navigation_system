
import json
import logging

from navigation import OrderNavigationSystem

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


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
            nav_system.display_settings()
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
            nav_system.display_settings()
            nav_system.print_data()
            # logger.debug(f"Navigation Mode changed: group_navigation={nav_system.group_navigation}")
            continue
        elif action in ["data", "d"]:
            nav_system.print_data()
            continue
        elif action in ['settings', 'config', 'conf']:
            nav_system.display_settings()
            continue
        elif action in ['continue', 'c']:
            nav_system.continue_item()
            

        # show whole dataset after each action
        nav_system.print_data()
        
        
if __name__ == "__main__":
    main()
