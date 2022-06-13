from fastapi import FastAPI
system = FastAPI()
ride_bus_list = []
@system.get("user_id/{user_id}/time/{time}")
def bus_line_count(user_id,time):
        ride_bus_list.append({'user_id': user_id,'ride_time':time})
        return len(ride_bus_list)
