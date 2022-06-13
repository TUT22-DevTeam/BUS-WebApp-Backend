from fastapi import FastAPI
system = FastAPI()
ride_bus_list = []
@system.get("user_id/{user_id}/ride_bus/{ride_bool}/time/{time}")
def bus_line_count(user_id,ride_bool,time):
        ride_bus_list.append({'user_id': user_id,'ride': ride_bool,'ride_time':time})
        return len(ride_bus_list)