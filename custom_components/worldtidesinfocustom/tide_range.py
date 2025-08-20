import time
import logging

_LOGGER = logging.getLogger(__name__)
from pyworldtidesinfo.worldtidesinfo_server import give_info_from_raw_data
from .sensor_service import convert_to_perform
# data = self._worldtidesinfo_server_scheduler._Data_Retrieve.data
# current_time = time.time()

def convert_to_unit_to_display(heigh_array, unit_to_display):
    convert_meter_to_feet, convert_km_to_miles = convert_to_perform(
            unit_to_display
        )
    heigh_value = []
    for index in range(len(heigh_array)):
        converted_heigh = heigh_array[index] * convert_meter_to_feet
        heigh_value.append(converted_heigh)
    return heigh_value

def convert_to_relative_time(epoch_array, current_time):
    time_scale = 60 * 60
    relative_time_value = []
    for index in range(len(epoch_array)):
        converted_time = (epoch_array[index] - current_time) / time_scale
        relative_time_value.append(converted_time)
    return relative_time_value

def compute_lower_tide_range(data, current_time, target_height, unit_to_display):
    ''' Computes the range(s) of time from current_time to Current_time + 24 hrs
        where the tide level is below target_height '''
    if data is None:
        return
    tformat = '%a %-I:%M %p'

    tide_info = give_info_from_raw_data(data)

    # Retrieve height data within time frame
    # from current_time to current_time + 24 hrs
    epoch_frame_min = current_time 
    epoch_frame_max = (current_time + 24 * 60 * 60)
    
    _LOGGER.error('curent time = %s ', time.strftime(tformat, time.localtime(current_time)))

    # Retrieve height-time data within time frame
    height_data = tide_info.give_tide_prediction_within_time_frame(
        epoch_frame_min, epoch_frame_max
    )

    height_values = convert_to_unit_to_display(height_data.get("height_value"),
                                            unit_to_display)
    #height_times = convert_to_relative_time(height_data.get("height_epoch"),  current_time )
    height_times = height_data.get("height_epoch")
    ranges = []
    summary = ''
    i = 0
    n = len(height_values)
    
    _LOGGER.error('start time = %s , stop time = %s', time.strftime(tformat, time.localtime(height_times[0])), time.strftime(tformat, time.localtime(height_times[-1])))
    while i < n:
        if height_values[i] > target_height:
            i += 1
            continue
        start = i
        while i < n and height_values[i] <= target_height:
            i += 1
        stop = i - 1
        ranges.append([height_times[start], height_times[stop]])
        
        summary = summary + f" from {time.strftime(tformat, time.localtime(height_times[start]))} to {time.strftime(tformat, time.localtime( height_times[stop]))} "
    return summary
    
        
        
