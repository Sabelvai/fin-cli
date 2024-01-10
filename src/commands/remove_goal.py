from api import dbapi

def remove_goals(goals):
    dbapi.delete("savings", "goal", goals)
    print(f"{goals} removed from savings")
