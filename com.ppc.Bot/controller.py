'''
Created on March 27, 2017

This file is subject to the terms and conditions defined in the
file 'LICENSE.txt', which is part of this source code package.

@author: David Moss
'''

import copy

from locations.location import Location

from devices.camera.camera_peoplepower_presenceandroid import PeoplePowerPresenceAndroidCameraDevice
from devices.camera.camera_peoplepower_presenceios import PeoplePowerPresenceIosCameraDevice
from devices.entry.entry import EntryDevice
from devices.environment.temperature import TemperatureDevice
from devices.environment.temperaturehumidity import TemperatureHumidityDevice
from devices.gateway.gateway_peoplepower_iotgateway import PeoplePowerIotGatewayDevice
from devices.gateway.gateway_qorvo_lcgw import QorvoLcgwGatewayDevice
from devices.leak.leak import LeakDevice
from devices.light.light import LightDevice
from devices.light.lightswitch_ge import LightswitchGeDevice
from devices.motion.motion import MotionDevice
from devices.movement.touch import TouchDevice
from devices.siren.siren_linkhigh import LinkhighSirenDevice
from devices.siren.siren_smartenit_zbalarm import SmartenitZbalarmDevice
from devices.smartplug.smartplug import SmartplugDevice
from devices.smartplug.smartplug_centralite_3series import Centralite3SeriesSmartplugDevice  # TODO how do we cast objects that are already created with this into a different class?
from devices.thermostat.thermostat_centralite_pearl import ThermostatCentralitePearlDevice
from devices.thermostat.thermostat_honeywell_lyric import ThermostatHoneywellLyricDevice
from devices.thermostat.thermostat_sensibo_sky import ThermostatSensiboSkyDevice
from devices.thermostat.thermostat_ecobee import ThermostatEcobeeDevice
from devices.touchpad.touchpad_peoplepower import PeoplePowerTouchpadDevice
from devices.button.button import ButtonDevice
from devices.lock.lock import LockDevice
from devices.gas.carbon_monoxide import CarbonMonoxideDevice
from devices.pictureframe.pictureframe_peoplepower_ios import PeoplePowerPictureFrameIosDevice
from devices.pictureframe.pictureframe_peoplepower_android import PeoplePowerPictureFrameAndroidDevice
from devices.smartplug.smartplug_smartenit_largeload import SmartenitLargeLoadControllerDevice


class Controller:
    """This is the main class that will coordinate all our sensors and behavior"""
    
    def __init__(self):
        """
        Constructor
        """
        # A list of our locations, where the key is the location ID. Most users only have 1 location, but our architecture supports multiple so we prepare for that
        self.locations = {}
            
        # A map of device_id : locationId
        self.location_devices = {}
        
        
    def initialize(self, botengine):
        """
        Initialize the controller.
        This is mandatory to call once for each new execution of the bot
        """
        #self.print_status(botengine)
        for key in self.locations:
            self.locations[key].initialize(botengine)
            
    
    def print_status(self, botengine):
        """
        Print the status of this object
        """
        logger = botengine.get_logger()
        logger.info("Controller Status")
        logger.info("-----")
        logger.info("self.locations: " + str(self.locations))
        logger.info("self.location_devices: " + str(self.location_devices))
        logger.info("-----")
            
    
    def track_new_and_deleted_devices(self, botengine):
        """
        Track any new or deleted devices
        :param botengine: Execution environment
        :param controller: Controller object managing all locations and devices
        """
        access = botengine.get_access_block()
        
        if access is None:
            botengine.get_logger().error("Bot Server error: No 'access' block in our inputs!")
            return
        
        locations_list = []
        
        # Maintenance: Add new devices
        for item in access:
            if item['category'] == botengine.ACCESS_CATEGORY_MODE:
                if 'location' in item:
                    if 'locationId' in item['location']:
                        locations_list.append(item['location']['locationId'])
                
            elif item['category'] == botengine.ACCESS_CATEGORY_DEVICE:
                if 'device' not in item:
                    import json
                    botengine.get_logger().warn("Got a Device Category in our access block, but there was no 'device' element:\n" + json.dumps(access, indent=2, sort_keys=True))
                    continue
                
                device_id = item['device']['deviceId']
                device_type = item['device']['deviceType']
                device_desc = item['device']['description']
                location_id = item['device']['locationId']
                
                device_object = self.get_device(device_id)

                if device_object is not None:
                    if device_type != device_object.device_type:
                        # The device type changed. We have to restart this device.
                        # This happens when a device gets registered to our cloud and looks like some device type,
                        # and then starts reporting extra information and features in later that make the cloud realize
                        # it is actually a different device type than what was originally conceived.
                        self.delete_device(botengine, device_id)
                        device_object = None
                        continue
                
                if device_object is None:
                    if device_type in PeoplePowerPresenceAndroidCameraDevice.DEVICE_TYPES:
                        device_object = PeoplePowerPresenceAndroidCameraDevice(botengine, device_id, device_type, device_desc)
                        
                    elif device_type in PeoplePowerPresenceIosCameraDevice.DEVICE_TYPES:
                        device_object = PeoplePowerPresenceIosCameraDevice(botengine, device_id, device_type, device_desc)
                        
                    elif device_type in EntryDevice.DEVICE_TYPES:
                        device_object = EntryDevice(botengine, device_id, device_type, device_desc)
                    
                    elif device_type in TemperatureDevice.DEVICE_TYPES:
                        device_object = TemperatureDevice(botengine, device_id, device_type, device_desc)
                        
                    elif device_type in TemperatureHumidityDevice.DEVICE_TYPES:
                        device_object = TemperatureHumidityDevice(botengine, device_id, device_type, device_desc)
                        
                    elif device_type in PeoplePowerIotGatewayDevice.DEVICE_TYPES:
                        device_object = PeoplePowerIotGatewayDevice(botengine, device_id, device_type, device_desc)
                    
                    elif device_type in QorvoLcgwGatewayDevice.DEVICE_TYPES:
                        device_object = QorvoLcgwGatewayDevice(botengine, device_id, device_type, device_desc)
                        
                    elif device_type in LeakDevice.DEVICE_TYPES:
                        device_object = LeakDevice(botengine, device_id, device_type, device_desc)
                        
                    elif device_type in LightDevice.DEVICE_TYPES:
                        device_object = LightDevice(botengine, device_id, device_type, device_desc)
                        
                    elif device_type in LightswitchGeDevice.DEVICE_TYPES:
                        device_object = LightswitchGeDevice(botengine, device_id, device_type, device_desc)
                        
                    elif device_type in MotionDevice.DEVICE_TYPES:
                        device_object = MotionDevice(botengine, device_id, device_type, device_desc)
                        
                    elif device_type in TouchDevice.DEVICE_TYPES:
                        device_object = TouchDevice(botengine, device_id, device_type, device_desc)
                        
                    elif device_type in SmartenitZbalarmDevice.DEVICE_TYPES:
                        device_object = SmartenitZbalarmDevice(botengine, device_id, device_type, device_desc)

                    elif device_type in LinkhighSirenDevice.DEVICE_TYPES:
                        device_object = LinkhighSirenDevice(botengine, device_id, device_type, device_desc)

                    elif device_type in SmartplugDevice.DEVICE_TYPES:
                        device_object = SmartplugDevice(botengine, device_id, device_type, device_desc)
                        
                    elif device_type in ThermostatCentralitePearlDevice.DEVICE_TYPES:
                        device_object = ThermostatCentralitePearlDevice(botengine, device_id, device_type, device_desc)
                    
                    elif device_type in ThermostatHoneywellLyricDevice.DEVICE_TYPES:
                        device_object = ThermostatHoneywellLyricDevice(botengine, device_id, device_type, device_desc)
                        
                    elif device_type in ThermostatSensiboSkyDevice.DEVICE_TYPES:
                        device_object = ThermostatSensiboSkyDevice(botengine, device_id, device_type, device_desc)

                    elif device_type in ThermostatEcobeeDevice.DEVICE_TYPES:
                        device_object = ThermostatEcobeeDevice(botengine, device_id, device_type, device_desc)
                        
                    elif device_type in PeoplePowerTouchpadDevice.DEVICE_TYPES:
                        device_object = PeoplePowerTouchpadDevice(botengine, device_id, device_type, device_desc)

                    elif device_type in ButtonDevice.DEVICE_TYPES:
                        device_object = ButtonDevice(botengine, device_id, device_type, device_desc)

                    elif device_type in LockDevice.DEVICE_TYPES:
                        device_object = LockDevice(botengine, device_id, device_type, device_desc)

                    elif device_type in CarbonMonoxideDevice.DEVICE_TYPES:
                        device_object = CarbonMonoxideDevice(botengine, device_id, device_type, device_desc)

                    elif device_type in PeoplePowerPictureFrameIosDevice.DEVICE_TYPES:
                        device_object = PeoplePowerPictureFrameIosDevice(botengine, device_id, device_type, device_desc)

                    elif device_type in PeoplePowerPictureFrameAndroidDevice.DEVICE_TYPES:
                        device_object = PeoplePowerPictureFrameAndroidDevice(botengine, device_id, device_type, device_desc)

                    elif device_type in SmartenitLargeLoadControllerDevice.DEVICE_TYPES:
                        device_object = SmartenitLargeLoadControllerDevice(botengine, device_id, device_type, device_desc)

                    else:
                        botengine.get_logger().warn("Unsupported device type: " + str(device_type) + " ('" + device_desc + "')")
                        continue
                
                device_object.is_connected = item['device']['connected']
                device_object.can_read = item['read']
                device_object.can_control = item['control']
                device_object.device_id = device_id.encode('utf-8')
                device_object.description = device_desc.encode('utf-8').strip()
                
                if 'remoteAddrHash' in item['device']:
                    device_object.remote_addr_hash = item['device']['remoteAddrHash']
                
                if 'proxyId' in item['device']:
                    device_object.proxy_id = item['device']['proxyId']
                
                if 'goalId' in item['device']:
                    device_object.goal_id = item['device']['goalId']

                if 'startDate' in item['device']:
                    device_object.born_on = item['device']['startDate']

                self.sync_device(botengine, location_id, device_id, device_object)

                if hasattr(device_object, "latitude") and hasattr(device_object, "longitude"):
                    if 'latitude' in item['device'] and 'longitude' in item['device']:
                        if float(item['device']['latitude']) != device_object.latitude or float(item['device']['longitude']) != device_object.longitude:
                            device_object.update_coordinates(botengine, float(item['device']['latitude']), float(item['device']['longitude']))


        # Maintenance: Prune out deleted locations
        if len(locations_list) > 0:
            for location_id in self.locations.keys():
                if location_id not in locations_list:
                    self.delete_location(botengine, location_id)
            
        # Maintenance: Prune out old devices
        for device_id in copy.copy(self.location_devices):
            found = False

            for item in access:
                if item['category'] == botengine.ACCESS_CATEGORY_DEVICE:
                    if 'device' in item:
                        if item['device']['deviceId'] == device_id:
                            found = True
                            break
    
            if not found:
                self.delete_device(botengine, device_id)
    

    def sync_device(self, botengine, location_id, device_id, device_object):
        """
        Synchronize the device with the tracking system
        + Make sure the device's name is up-to-date
        + Create the location if it doesn't exist
        + Move the device to the correct location if it's in the wrong location
        + Make sure the location is tracking this device object
        + Tell the location to re-evaluate its state based on this new information
        
        :param botengine: BotEngine environment
        :param location_id: Location ID
        :param device_id: Device ID
        :param device_object: Device object
        """
        # Make sure the location exists
        if location_id not in self.locations:
            # The location isn't being tracked yet, add it
            botengine.get_logger().info("\t=> Now tracking location " + str(location_id))
            self.locations[location_id] = Location(botengine, location_id)

        # Make sure the device is being tracked, and it's in the correct location
        if device_id not in self.location_devices:
            # The device isn't being tracked at all - add it
            botengine.get_logger().info("\t=> Now tracking device " + str(device_id))
            self.location_devices[device_id] = location_id
            self.locations[location_id].add_device(botengine, device_object)
            device_object.location_object = self.locations[location_id]

        elif self.location_devices[device_id] != location_id:
            # The device is in the wrong location, move it.
            botengine.get_logger().info("\t=> Moving device " + str(device_id) + " to location " + str(location_id))
            self.locations[self.location_devices[device_id]].delete_device(botengine, device_id)
            self.location_devices[device_id] = location_id
            self.locations[location_id].devices[device_id] = device_object
            device_object.location_object = self.locations[location_id]
    
    def device_measurements_updated(self, botengine, location_id, device_object):
        """
        A device's measurements have been updated
        :param botengine: BotEngine environment
        :param location_id: Location ID
        :param device_object: Device object
        """
        self.locations[location_id].device_measurements_updated(botengine, device_object)

    def device_metadata_updated(self, botengine, location_id, device_object):
        """
        Evaluate a device that is new or whose goal/scenario was recently updated
        :param botengine: BotEngine environment
        :param location_id: Location ID
        :param device_object: Device object
        """
        self.locations[location_id].device_metadata_updated(botengine, device_object)

    def device_alert(self, botengine, location_id, device_object, alert_type, alert_params):
        """
        Device alerts were updated
        :param botengine: BotEngine environment
        :param location_id: Location ID
        :param device_object: Device object that generated the alert
        :param alert_type: Type of alert
        :param alert_params: Dictionary of alert parameters
        :return:
        """
        self.locations[location_id].device_alert(botengine, device_object, alert_type, alert_params)

    def file_uploaded(self, botengine, device_object, file):
        """
        File was uploaded
        :param botengine: BotEngine environment
        :param device_object: Device object that uploaded the file
        :param file: File JSON structure
        """
        location_id = self.location_devices[device_object.device_id]
        content_type = None
        file_extension = None
        file_id = None
        filesize_bytes = None

        if 'contentType' in file:
            content_type = file['contentType']

        if 'extension' in file:
            file_extension = file['extension']

        if 'fileId' in file:
            file_id = file['fileId']

        if 'fileSize' in file:
            filesize_bytes = file['fileSize']

        device_object.file_uploaded(botengine, device_object, file_id, filesize_bytes, content_type, file_extension)
        self.locations[location_id].file_uploaded(botengine, device_object, file_id, filesize_bytes, content_type, file_extension)

    def user_role_updated(self, botengine, location_id, user_id, category, location_access, previous_category, previous_location_access):
        """
        A user changed roles
        :param botengine: BotEngine environment
        :param location_id: Location ID
        :param user_id: User ID that changed roles
        :param category: User's current alert/communications category (1=resident; 2=supporter)
        :param location_access: User's current access to the location
        :param previous_category: User's previous category, if any
        :param previous_location_access: User's previous access to the location, if any
        :return:
        """
        if location_id not in self.locations:
            # The location isn't being tracked yet, add it
            botengine.get_logger().info("\t=> Now tracking location " + str(location_id))
            self.locations[location_id] = Location(botengine, location_id)

        self.locations[location_id].user_role_updated(botengine, user_id, category, location_access, previous_category, previous_location_access)

    def data_request_ready(self, botengine, reference, device_csv_dict):
        """
        A botengine.request_data() request is ready
        :param botengine: BotEngine environment
        :param reference: Optional reference passed into botengine.request_data(..)
        :param device_csv_dict: { 'device_id': 'csv data string' }
        """
        for location_id in self.locations:
            self.locations[location_id].data_request_ready(botengine, reference, device_csv_dict)

    def sync_mode(self, botengine, mode, location_id):
        """
        Update the mode.
        
        This notifies the specific location that its mode changed, and it is that location's responsibility to signal the mode_updated to all children device and location intelligence modules.
        
        :param botengine: BotEngine environment
        :param mode: Mode of the home, like "HOME" or "AWAY"
        :param location_id: Location that had its mode changed
        """
        botengine.get_logger().info("Controller: Sync mode for location " + str(location_id))
        if location_id not in self.locations:
            self.locations[location_id] = Location(botengine, location_id)

        self.locations[location_id].mode_updated(botengine, mode)
        
    def sync_datastreams(self, botengine, address, content):
        """
        Synchronize the data stream messages across all location objects
        :param botengine: BotEngine environment
        :param address: Data Stream address
        :param content: Data Stream content
        """
        for location_id in self.locations:
            self.locations[location_id].datastream_updated(botengine, address, content)
    
    
    def sync_question(self, botengine, question):
        """
        Synchronize an answered question
        :param botengine: BotEngine environment
        :param question: Answered question
        """
        # Sync location intelligence
        for location_id in self.locations:
            self.locations[location_id].question_answered(botengine, question)


    def run_location_intelligence(self, botengine, intelligence_id, argument):
        """
        Because we don't know what location_id owns this intelligence module, we have to own the responsibility of discovering the intelligence module here.
        :param botengine: BotEngine environment
        :param intelligence_id: ID of the intelligence module which needs its timer fired
        :param argument: Argument to pass into the timer_fired() method of the intelligence module
        """
        botengine.get_logger().info("Location Intelligence Timer Fired: " + str(intelligence_id))
        for location_id in self.locations:
            # Search for and trigger individual location instances
            if str(intelligence_id) == str(location_id):
                self.locations[location_id].timer_fired(botengine, argument)
                return

            # Search for and trigger location intelligence instances
            for intelligence_module_name in self.locations[location_id].intelligence_modules:
                if intelligence_id == self.locations[location_id].intelligence_modules[intelligence_module_name].intelligence_id:
                    self.locations[location_id].intelligence_modules[intelligence_module_name].timer_fired(botengine, argument)
                    return

    def run_device_intelligence(self, botengine, intelligence_id, argument):
        """
        Because we don't know what location_id owns this intelligence module, we have to own the responsibility of discovering the intelligence module here.
        :param botengine: BotEngine environment
        :param intelligence_id: ID of the intelligence module which needs its timer fired
        :param argument: Argument to pass into the timer_fired() method of the intelligence module
        """
        botengine.get_logger().info("Device Intelligence Timer Fired: " + str(intelligence_id))
        for location_id in self.locations:
            for device_id in self.locations[location_id].devices:
                for intelligence_module_name in self.locations[location_id].devices[device_id].intelligence_modules:
                    if intelligence_id == self.locations[location_id].devices[device_id].intelligence_modules[intelligence_module_name].intelligence_id:
                        self.locations[location_id].devices[device_id].intelligence_modules[intelligence_module_name].timer_fired(botengine, argument)
                        return

    def run_intelligence_schedules(self, botengine, schedule_id):
        """
        Notify each location that the schedule fired. 
        The location should be responsible for telling all device and location intelligence modules, 
        and performing periodic tasks like garbage collection.
        :param botengine: BotEngine environment
        """
        for location_id in self.locations:
            self.locations[location_id].schedule_fired(botengine, schedule_id)
        
    def get_device(self, device_id):
        """
        Get the device represented by the device ID, if it exists
        :return: the device object represented by the device ID, or return None if the device does not yet exist
        """
        try:
            return self.locations[self.location_devices[device_id]].devices[device_id]
            
        except:
            return None
    
    def delete_device(self, botengine, device_id):
        """
        Delete the given device ID
        :param device_id: Device ID to delete
        """
        botengine.get_logger().info("Deleting device: " + str(device_id))
        if device_id in self.location_devices:
            location = self.locations[self.location_devices[device_id]]
            location.delete_device(botengine, device_id)
            del self.location_devices[device_id]
        
    def delete_location(self, botengine, location_id):
        """
        Delete the given location ID
        :param location_id: Location ID to delete
        """
        botengine.get_logger().info("Deleting Location: " + str(location_id))
        if location_id in self.locations.keys():
            for device_id in copy.copy(self.location_devices):
                if self.location_devices[device_id] == location_id:
                    self.delete_device(botengine, device_id)
            
            del self.locations[location_id]
        
        