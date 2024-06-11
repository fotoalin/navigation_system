
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
    if not handler_name:
        handler_name = "▒▒▒▒▒▒▒▒▒▒ALIN"
    nav_system = OrderNavigationSystem(data, handler_name, group_navigation=True)
    
    actions = ['help', 'toggle print', 'toggle navigation', 'print', 'next', 'prev', 'next page', 'prev page', 'state', 'exit', 'data', 'settings', 'continue', 'reset', 'reset group', 'reset all']

    # Print the data at the start
    nav_system.display_settings()
    nav_system.print_data()

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
        elif 'start' in action or 'begin' in action:
            action_values = action.split()
            if len(action_values) < 2:
                print("Please provide the group number you want to start")
                continue
            elif not action_values[1].isdigit():
                print("Please provide a valid group number")
                continue
            elif int(action_values[1]) > len(data):
                print("Group number out of range")
                continue
            nav_system.start(int(action_values[1]) - 1)
        elif action in ["toggle print", "tp", "toggle_print", "toggle autoprint", "toggle_autoprint"]:
            nav_system.toggle_autoprint()
            nav_system.display_settings()
            # print_data()
        elif action in ["print"]:
            nav_system.mark_current_item_as_complete()
        elif action in ["next", "n"]:
            nav_system.next_item()
        elif action in ["prev", "p", "previous"]:
            nav_system.previous_item()
        elif action in ["next page", "next_page", "np", "next group", "next_group", "ng"]:
            nav_system.next_page()
        elif action in ["prev page", "prev_group", "pg", "previous_page", "prev_page", "pp"]:
            nav_system.previous_page()
        elif action in ["state", "s"]:
            logger.debug(json.dumps(nav_system.get_current_state(), indent=4))
            continue
        elif action in ["exit", "e", "quit", "q"]:
            print("Exiting...")
            break
        elif action in ["toggle navigation", "tn", "toggle_nav", "toggle nav", "toggle_navigation"]:
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
        # 'reset', 'reset group', 'reset all'
        elif action in ['reset', 'r']:
            nav_system.reset_current_item()
        elif action in ['reset group', 'rg', 'reset page', 'rp']:
            nav_system.reset_current_group()
        elif action in ['reset all', 'ra']:
            nav_system.reset_all()
            

        # show whole dataset after each action
        nav_system.display_settings()
        nav_system.print_data()
        
        
if __name__ == "__main__":
    main()
