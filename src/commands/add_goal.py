from api import dbapi

def add_goal(goal, how_much_to_add):
    goal_check = dbapi.check_goal(goal)

    for sublist_index, sublist in enumerate(goal_check, start=1):
        if len(sublist) == 2:
            how_much_collected, how_much_need = sublist

            if how_much_collected == how_much_need:
                print("Goal Completed")
            elif how_much_collected > how_much_need:
                print(f"More then need for goal you can take back money {how_much_collected - how_much_need}")
            else:
                dbapi.add_goal(goal, how_much_to_add)
