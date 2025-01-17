'''
Created on May 6, 2017

This file is subject to the terms and conditions defined in the
file 'LICENSE.txt', which is part of this source code package.

@author: David Moss
'''

from devices.device import Device

class LeakDevice(Device):
    """Water Leak Sensor"""
    
    # List of Device Types this class is compatible with
    DEVICE_TYPES = [10017, 10076]
        
    # Low battery tag
    LOW_BATTERY_TAG = "lowbattery_cr2450"

    # Measurement Names
    MEASUREMENT_NAME_STATUS = 'waterLeak'

    MEASUREMENT_PARAMETERS_LIST = [
        MEASUREMENT_NAME_STATUS
    ]

    def __init__(self, botengine, device_id, device_type, device_description, precache_measurements=True):
        Device.__init__(self, botengine, device_id, device_type, device_description, precache_measurements=precache_measurements)
        
    def initialize(self, botengine):
        Device.initialize(self, botengine)
    
    def get_device_type_name(self):
        """
        :return: the name of this device type in the given language, for example, "Entry Sensor"
        """
        # NOTE: Device type name
        return _("Leak Sensor")
    
    def get_image_name(self):
        """
        :return: the font icon name of this device type
        """
        return "water"
    
    
    #===========================================================================
    # Helper methods
    #===========================================================================
    def did_change_state(self, botengine=None):
        """
        :return: True if this entry sensor's state was updated just now
        """
        return LeakDevice.MEASUREMENT_NAME_STATUS in self.last_updated_params

    def is_leak_detected(self):
        """
        :return: True if a leak is currently detected
        """
        if LeakDevice.MEASUREMENT_NAME_STATUS in self.measurements:
            return self.measurements[LeakDevice.MEASUREMENT_NAME_STATUS][0][0]
        
        return False
    