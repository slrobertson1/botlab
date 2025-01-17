'''
Created on June 28, 2016

This file is subject to the terms and conditions defined in the
file 'LICENSE.txt', which is part of this source code package.

@author: David Moss
'''

import pytz
import datetime
import utilities
import intelligence.index
import importlib
import domain


class Location:
    """This class simply keeps track of our location and figures out the state of the location's security system"""
    def __init__(self, botengine, location_id):
        """Constructor"""
        self.location_id = int(location_id)

        # Dictionary of all device objects. { 'device_id': <device_object> }
        self.devices = {}
        
        # Born on date
        self.born_on = botengine.get_timestamp()
        
        # Mode of this location (i.e. "HOME", "AWAY", etc.). This is the mode of the security system.
        self.mode = botengine.get_mode(self.location_id)

        # Timestamp of the last time we did a garbage collection
        self.garbage_timetamp_ms = 0
        
        # All Location Intelligence modules
        self.intelligence_modules = {}

        # Try to update our current mode
        self.update_mode(botengine)

        # Conversational UI
        self.conversational_ui = None

        # Occupancy status as determined by AI occupancy detection algorithms.
        self.occupancy_status = ""

        # Reason for the current occupancy status. For example: "ML.MOTION" or "USER".
        self.occupancy_reason = ""

        # Last time our location properties were sync'd
        self.properties_timestamp_ms = 0

        # Latest copy of our location properties
        self.location_properties = {}

        # Narratives we're tracking from various microservices for your location.  { "unique_id" : ( narrative_id, narrative_time ) }.
        self.location_narratives = {}

        # Narratives we're tracking from various microservices for your organization. { "unique_id" : ( narrative_id, narrative_time ) }.
        self.org_narratives = {}

        
    def initialize(self, botengine):
        """Mandatory to run with every execution"""
        # Refresh this with every execution
        if not hasattr(self, 'conversational_ui'):
            self.conversational_ui = None

        # Added November 29, 2018
        if not hasattr(self, 'occupancy_status'):
            self.occupancy_status = ""
            self.occupancy_reason = ""

        # Added June 1, 2019
        if not hasattr(self, 'properties_timestamp_ms'):
            self.properties_timestamp_ms = 0
            self.location_properties = {}

        # Added June 14, 2019
        if not hasattr(self, 'location_narratives'):
            self.location_narratives = {}

        # Added June 14, 2019
        if not hasattr(self, 'org_narratives'):
            self.org_narratives = {}

        for d in self.devices:
            self.devices[d].initialize(botengine)
            
        # Synchronize intelligence capabilities
        if len(self.intelligence_modules) != len(intelligence.index.MICROSERVICES['LOCATION_MICROSERVICES']):
            
            # Add more microservices
            # 10014: [{"module": "intelligence.rules.device_entry_intelligence", "class": "EntryRulesIntelligence"}],
            for intelligence_info in intelligence.index.MICROSERVICES['LOCATION_MICROSERVICES']:
                if intelligence_info['module'] not in self.intelligence_modules:
                    try:
                        intelligence_module = importlib.import_module(intelligence_info['module'])
                        class_ = getattr(intelligence_module, intelligence_info['class'])
                        botengine.get_logger().info("Adding location microservice: " + str(intelligence_info['module']))
                        intelligence_object = class_(botengine, self)
                        self.intelligence_modules[intelligence_info['module']] = intelligence_object
                    except Exception as e:
                        botengine.get_logger().error("Could not add location microservice: " + str(intelligence_info) + ": " + str(e))
                        import traceback
                        traceback.print_exc()
                        
                    
            # Remove microservices that no longer exist
            for module_name in self.intelligence_modules.keys():
                found = False
                for intelligence_info in intelligence.index.MICROSERVICES['LOCATION_MICROSERVICES']:
                    if intelligence_info['module'] == module_name:
                        found = True
                        break
                    
                if not found:
                    botengine.get_logger().info("Deleting location microservice: " + str(module_name))
                    self.intelligence_modules[module_name].destroy(botengine)
                    del self.intelligence_modules[module_name]
                    
        # Location intelligence execution
        for i in self.intelligence_modules:
            self.intelligence_modules[i].parent = self
            self.intelligence_modules[i].initialize(botengine)
        
        
    
    def garbage_collect(self, botengine):
        """
        Clean up the garbage
        :param botengine: BotEngine environment
        """
        for device_id in self.devices:
            self.devices[device_id].garbage_collect(botengine)
            
    def add_device(self, botengine, device_object):
        """
        Start tracking a new device here.
        Perform any bounds checking, for example with multiple gateways at one location.
        :param device_object: Device object to track
        """
        self.devices[device_object.device_id] = device_object

        if hasattr(device_object, "intelligence_modules"):
            for intelligence_id in device_object.intelligence_modules:
                device_object.intelligence_modules[intelligence_id].device_added(botengine, device_object)

        for intelligence_id in self.intelligence_modules:
            self.intelligence_modules[intelligence_id].device_added(botengine, device_object)

    def delete_device(self, botengine, device_id):
        """
        Delete the given device ID
        :param device_id: Device ID to delete
        """
        device_object = None
        if device_id in self.devices:
            device_object = self.devices[device_id]
            
            if hasattr(device_object, "intelligence_modules"):
                for intelligence_id in device_object.intelligence_modules:
                    device_object.intelligence_modules[intelligence_id].destroy(botengine)
            
            del self.devices[device_id]
            
            for intelligence_id in self.intelligence_modules:
                self.intelligence_modules[intelligence_id].device_deleted(botengine, device_object)
    
    def mode_updated(self, botengine, mode):
        """
        Update this location's mode
        """
        self.mode = mode
        botengine.get_logger().info("location mode_updated(): " + self.mode + " mode.")
        
        for intelligence_id in self.intelligence_modules:
            self.intelligence_modules[intelligence_id].mode_updated(botengine, mode)

        # Device intelligence modules
        for device_id in self.devices:
            if hasattr(self.devices[device_id], "intelligence_modules"):
                for intelligence_id in self.devices[device_id].intelligence_modules:
                    self.devices[device_id].intelligence_modules[intelligence_id].mode_updated(botengine, mode)
    
    def device_measurements_updated(self, botengine, device_object):
        """
        Evaluate a device that was recently updated
        :param botengine: BotEngine environment
        :param device_object: Device object that was updated
        """
        for intelligence_id in self.intelligence_modules:
            self.intelligence_modules[intelligence_id].device_measurements_updated(botengine, device_object)
    
    def device_metadata_updated(self, botengine, device_object):
        """
        Evaluate a device that is new or whose goal/scenario was recently updated
        :param botengine: BotEngine environment
        :param device_object: Device object that was updated
        """
        for intelligence_id in self.intelligence_modules:
            self.intelligence_modules[intelligence_id].device_metadata_updated(botengine, device_object)

    def device_alert(self, botengine, device_object, alert_type, alert_params):
        """
        Device sent an alert
        :param botengine: BotEngine environment
        :param device_object: Device object that sent the alert
        :param alerts_list: List of alerts
        """
        for intelligence_id in self.intelligence_modules:
            self.intelligence_modules[intelligence_id].device_alert(botengine, device_object, alert_type, alert_params)

    def question_answered(self, botengine, question):
        """
        The user answered a question
        :param botengine: BotEngine environment
        :param question: Question object
        """
        for intelligence_id in self.intelligence_modules:
            self.intelligence_modules[intelligence_id].question_answered(botengine, question)
        
        # Device intelligence modules
        for device_id in self.devices:
            if hasattr(self.devices[device_id], "intelligence_modules"):
                for intelligence_id in self.devices[device_id].intelligence_modules:
                    self.devices[device_id].intelligence_modules[intelligence_id].question_answered(botengine, question)
    
    
    def datastream_updated(self, botengine, address, content):
        """
        Data Stream Updated
        :param botengine: BotEngine environment
        :param address: Data Stream address
        :param content: Data Stream content
        """
        for intelligence_id in self.intelligence_modules:
            try:
                self.intelligence_modules[intelligence_id].datastream_updated(botengine, address, content)
            except Exception as e:
                botengine.get_logger().warn("location.py - Error delivering datastream message to location microservice (continuing execution): " + str(e))
                import traceback
                botengine.get_logger().error(traceback.format_exc())
        
        # Device intelligence modules
        for device_id in self.devices:
            if hasattr(self.devices[device_id], "intelligence_modules"):
                for intelligence_id in self.devices[device_id].intelligence_modules:
                    try:
                        self.devices[device_id].intelligence_modules[intelligence_id].datastream_updated(botengine, address, content)
                    except Exception as e:
                        botengine.get_logger().warn("location.py - Error delivering datastream message to device microservice (continuing execution): " + str(e))
                        import traceback
                        botengine.get_logger().error(traceback.format_exc())
                    
            
    def schedule_fired(self, botengine, schedule_id):
        """
        Schedule Fired.
        It is this location's responsibility to notify all sub-intelligence modules, including both device and location intelligence modules
        :param botengine: BotEngine environment
        """
        # Location intelligence modules
        for intelligence_id in self.intelligence_modules:
            self.intelligence_modules[intelligence_id].schedule_fired(botengine, schedule_id)
        
        # Device intelligence modules
        for device_id in self.devices:
            if hasattr(self.devices[device_id], "intelligence_modules"):
                for intelligence_id in self.devices[device_id].intelligence_modules:
                    self.devices[device_id].intelligence_modules[intelligence_id].schedule_fired(botengine, schedule_id)
                    
        # Garbage collect
        if botengine.get_timestamp() - self.garbage_timetamp_ms > utilities.ONE_WEEK_MS:
            self.garbage_collect(botengine)
        
    def timer_fired(self, botengine, argument):
        """
        Timer fired
        :param botengine: BotEngine environment
        :param argument: Optional argument
        """
        return


    def file_uploaded(self, botengine, device_object, file_id, filesize_bytes, content_type, file_extension):
        """
        A device file has been uploaded
        :param botengine: BotEngine environment
        :param device_object: Device object that uploaded the file
        :param file_id: File ID to reference this file at the server
        :param filesize_bytes: The file size in bytes
        :param content_type: The content type, for example 'video/mp4'
        :param file_extension: The file extension, for example 'mp4'
        """
        for intelligence_id in self.intelligence_modules:
            self.intelligence_modules[intelligence_id].file_uploaded(botengine, device_object, file_id, filesize_bytes, content_type, file_extension)

    def user_role_updated(self, botengine, user_id, category, location_access, previous_category, previous_location_access):
        """
        A user changed roles
        :param botengine: BotEngine environment
        :param location_id: Location ID
        :param user_id: User ID that changed roles
        :param category: User's current alert/communications category (1=resident; 2=supporter)
        :param location_access: User's access to the location and devices. (0=None; 10=read location/device data; 20=control devices and modes; 30=update location info and manage devices)
        :param previous_category: User's previous category, if any
        :param previous_location_access: User's previous access to the location, if any
        """
        # Location intelligence modules
        for intelligence_id in self.intelligence_modules:
            self.intelligence_modules[intelligence_id].user_role_updated(botengine, user_id, category, location_access, previous_category, previous_location_access)

        # Device intelligence modules
        for device_id in self.devices:
            if hasattr(self.devices[device_id], "intelligence_modules"):
                for intelligence_id in self.devices[device_id].intelligence_modules:
                    self.devices[device_id].intelligence_modules[intelligence_id].user_role_updated(botengine, user_id, category, location_access, previous_category, previous_location_access)

    def data_request_ready(self, botengine, reference, device_csv_dict):
        """
        A botengine.request_data() asynchronous request for CSV data is ready.
        :param botengine: BotEngine environment
        :param reference: Optional reference passed into botengine.request_data(..)
        :param device_csv_dict: { 'device_id': 'csv data string' }
        """
        # Location microservices
        for intelligence_id in self.intelligence_modules:
            try:
                self.intelligence_modules[intelligence_id].data_request_ready(botengine, reference, device_csv_dict)
            except Exception as e:
                botengine.get_logger().warn("location.py - Error delivering data_request_ready to location microservice : " + str(e))
                import traceback
                botengine.get_logger().error(traceback.format_exc())


        # Device microservices
        for device_id in self.devices:
            if hasattr(self.devices[device_id], "intelligence_modules"):
                for intelligence_id in self.devices[device_id].intelligence_modules:
                    try:
                        self.devices[device_id].intelligence_modules[intelligence_id].data_request_ready(botengine, reference, device_csv_dict)
                    except Exception as e:
                        botengine.get_logger().warn("location.py - Error delivering data_request_ready to device microservice : " + str(e))
                        import traceback
                        botengine.get_logger().error(traceback.format_exc())

    #===========================================================================
    # General location information
    #===========================================================================
    def get_location_name(self, botengine):
        """
        Get the nickname of this location
        :param botengine: BotEngine environment
        :return: Nickname
        """
        return botengine.get_location_name()

    def get_location_latitude(self, botengine):
        """
        Get the latitude of this location
        :param botengine: BotEngine environment
        :return: Latitude, or None if it doesn't exist
        """
        return botengine.get_location_latitude()

    def get_location_longitude(self, botengine):
        """
        Get the longitude of this location
        :param botengine: BotEngine environment
        :return: Longitude, or None if it doesn't exist
        """
        return botengine.get_location_longitude()


    #===========================================================================
    # Mode
    #===========================================================================
    def set_mode(self, botengine, mode, comment=None):
        """
        Set the mode for this location
        :param botengine: BotEngine environment
        :param comment: Optional comment about why the mode was set
        """
        self.track(botengine, 'set_mode_{}'.format(mode), properties={"comment": comment, "mode": mode})
        botengine.set_mode(self.location_id, mode, comment)
        # Allow the bot to trigger again and set the mode from a single unified action.


    def distribute_occupancy_status(self, botengine, status, reason, last_status, last_reason):
        """
        Distribute the newest occupancy status from AI occupancy algorithms
        :param botengine: BotEngine environment
        :param status: Current status
        :param reason: Current reason
        :param last_status: Last status
        :param last_reason: Last reason
        :return:
        """
        for intelligence_id in self.intelligence_modules:
            try:
                self.intelligence_modules[intelligence_id].occupancy_status_updated(botengine, status, reason, last_status, last_reason)
            except Exception as e:
                botengine.get_logger().warn("location.py - Error delivering occupancy_status_updated to location microservice (continuing execution): " + str(e))
                import traceback
                botengine.get_logger().error(traceback.format_exc())

        # Device intelligence modules
        for device_id in self.devices:
            if hasattr(self.devices[device_id], "intelligence_modules"):
                for intelligence_id in self.devices[device_id].intelligence_modules:
                    try:
                        self.devices[device_id].intelligence_modules[intelligence_id].occupancy_status_updated(botengine, status, reason, last_status, last_reason)
                    except Exception as e:
                        botengine.get_logger().warn("location.py - Error delivering occupancy_status_updated message to device microservice (continuing execution): " + str(e))
                        import traceback
                        botengine.get_logger().error(traceback.format_exc())

    #===========================================================================
    # Bot-to-UI content delivery
    #===========================================================================
    def set_ui_content(self, botengine, address, json_content):
        """
        Set information to be consumed by user interfaces through a known address.

        Application-layer developers first collectively agree upon the data
        that needs to be produced by the bot to be rendered on a UI. Then the UI
        can read the address to extract the JSON information to render natively.

        It is therefore possible for the bot to also produce new addressable content,
        as long as the addresses are retrievable from a well known base address. For example,
        you could save some UI content that includes a list of reports, each report saved under
        a unique address. Then, save UI content for each report under their unique addresses.

        :param botengine: BotEngine environment
        :param address: Address to save information into, in a way that can be recalled by an app.
        :param json_content: Raw JSON content to deliver to an app/UI.
        """
        botengine.set_ui_content(self.location_id, address, json_content)

    #===========================================================================
    # Location Properties
    #===========================================================================
    def set_location_property(self, botengine, property_name, property_value):
        """
        Set a location property
        :param botengine: BotEngine environment
        :param property_name: Property name
        :param property_value: Property value
        """
        self._sync_location_properties(botengine)
        self.location_properties[property_name] = property_value
        botengine.set_ui_content(self.location_id, 'location_properties', self.location_properties)

        import importlib
        try:
            analytics = importlib.import_module('analytics')
            analytics.get_analytics(botengine).people_set(botengine, {property_name: property_value})

        except ImportError:
            pass

    def update_location_properties(self, botengine, properties_dict):
        """
        Update multiple location properties simultaneously from a dictionary.
        If the properties don't exist yet, they will be added.

        :param botengine: BotEngine environment
        :param properties_dict: Properties dictionary with key/values to update
        """
        self._sync_location_properties(botengine)
        self.location_properties.update(properties_dict)
        botengine.set_ui_content(self.location_id, 'location_properties', self.location_properties)

        import importlib
        try:
            analytics = importlib.import_module('analytics')
            analytics.get_analytics(botengine).people_set(botengine, properties_dict)

        except ImportError:
            pass

    def increment_location_property(self, botengine, property_name, increment_amount=1):
        """
        Increment a location property integer by the amount given.

        If the property doesn't exist, it will be initialized to 0 and then incremented by the amount given.
        An existing property must be numeric to increment.

        :param botengine: BotEngine environment
        :param property_name: Property name to increment
        :param increment_amount: Incremental amount to add (default is 1)
        """
        self._sync_location_properties(botengine)
        if property_name not in self.location_properties:
            self.location_properties[property_name] = 0

        self.location_properties[property_name] += increment_amount
        botengine.set_ui_content(self.location_id, 'location_properties', self.location_properties)

        import importlib
        try:
            analytics = importlib.import_module('analytics')
            analytics.get_analytics(botengine).people_increment(botengine, {property_name: increment_amount})

        except ImportError:
            pass

    def get_location_property(self, botengine, property_name):
        """
        Retrieve a location property
        :param botengine: BotEngine environment
        :param property_name: Property name to retrieve
        :return: The property value, or None if it doesn't exist
        """
        self._sync_location_properties(botengine)
        if property_name in self.location_properties:
            return self.location_properties[property_name]
        return None

    def delete_location_property(self, botengine, property_name):
        """
        Delete a location property
        :param botengine: BotEngine environment
        :param property_name: Property name to delete
        """
        self._sync_location_properties(botengine)
        if property_name in self.location_properties:
            del(self.location_propertyes[property_name])
            botengine.set_ui_content(self.location_id, 'location_properties', self.location_properties)

    def set_location_property_separately(self, botengine, additional_property_name, additional_property_json):
        """
        Set a large location property. The name is referenced by our 'location_properties' but stored separately
        and referenced in the location_properties as 'additional_properties'.
        :param botengine: BotEngine environment
        :param additional_property_name: Property name to store separately and reference in our location_properties
        :param additional_property_json: Property JSON value
        :return:
        """
        additional_properties = self.get_location_property(botengine, 'additional_properties')
        if additional_properties is None:
            additional_properties = []

        if additional_property_name not in additional_properties:
            additional_properties.append(additional_property_name)
            self.set_location_property(botengine, 'additional_properties', additional_properties)

        botengine.set_ui_content(self.location_id, additional_property_name, additional_property_json)

    def _sync_location_properties(self, botengine):
        """
        Internal method to synchornize our local copy of location properties with the server
        :param botengine: BotEngine environment
        """
        if self.properties_timestamp_ms != botengine.get_timestamp():
            properties = botengine.get_ui_content(self.location_id, 'location_properties')
            if properties is not None:
                self.location_properties = properties

            else:
                self.location_properties = {}

            self.properties_timestamp_ms = botengine.get_timestamp()

    #===========================================================================
    # Data Stream Message delivery
    #===========================================================================
    def distribute_datastream_message(self, botengine, address, content=None, internal=True, external=True):
        """
        Distribute a data stream message both internally to any intelligence module within this bot,
        and externally to any other bots that might be listening.
        :param botengine: BotEngine environment
        :param address: Data stream address
        :param content: Message content
        :param internal: True to deliver this message internally to any intelligence module that's listening (default)
        :param external: True to deliver this message externally to any other bot that's listening (default)
        """
        if internal:
            self.datastream_updated(botengine, address, content)

        if external:
            botengine.send_datastream_message(address, content)



    #===========================================================================
    # Conversations
    #===========================================================================
    def get_conversation_types(self, botengine):
        """
        Return the module that documents the conversation types. Or None if the conversation microservice package is not included in this build.
        :param botengine:
        :return: Conversations module documenting the conversation types.
        """
        try:
            import intelligence.conversations.conversations as conversations
            return conversations

        except:
            botengine.get_logger().info("location.get_conversation_types(): No conversations microservice package in this build.")
            return None

    def start_conversation(self, botengine, conversation_type, homeowner_message, supporter_message, professional_monitoring_code=None, sms_callback_method=None, next_conversation_object=None, force=False):
        """
        Start a new conversation by creating the conversation and adding it to the queue.
        :param botengine: BotEngine environment
        :param conversation_type: Conversation type
        :param homeowner_message: Homeowner message / question
        :param supporter_message: Supporter message
        :param professional_monitoring_code: Override the default professional monitoring code, if any.
        :param sms_callback_method: Method to call back when the question is answered. def some_method(self, botengine, question_object)
        :param next_conversation_object: Conversation to link and execute immediately after this conversation ends.
        :param force: True to force the conversation, even if the conversation is disabled (for testing)
        :return: conversation_object for reference in update_conversation(..). Or None if this conversation will not be active.
        """
        # Try to add the conversational UI, which would be captured in one of our microservices.
        for module_name in self.intelligence_modules:
            if 'location_conversation_microservice' in module_name:
                return self.intelligence_modules[module_name].start_conversation(botengine,
                                                                                 conversation_type,
                                                                                 homeowner_message,
                                                                                 supporter_message,
                                                                                 professional_monitoring_code=professional_monitoring_code,
                                                                                 sms_callback_method=sms_callback_method,
                                                                                 next_conversation_object=next_conversation_object,
                                                                                 force=force)

        return None

    def create_conversation(self, botengine, conversation_type, homeowner_message, supporter_message, professional_monitoring_code=None, sms_callback_method=None, next_conversation_object=None, force=False):
        """
        Create and return a new conversation without executing on it or putting it into the queue.
        This does not start the conversation.
        This allows us to create a conversation and link it to another with ConversationType.next_conversation_object.
        :param botengine: BotEngine environment
        :param conversation_type: Conversation type
        :param homeowner_message: Homeowner message / question
        :param supporter_message: Supporter message
        :param professional_monitoring_code: Override the default professional monitoring code, if any.
        :param sms_callback_method: Method to call back when the question is answered. def some_method(self, botengine, question_object)
        :param next_conversation_object: Conversation to link and execute immediately after this conversation ends.
        :param force: True to force the conversation, even if the conversation is disabled (for testing)
        :return: conversation_object for reference in update_conversation(..). Or None if this conversation will not be active.
        """
        # Try to add the conversational UI, which would be captured in one of our microservices.
        for module_name in self.intelligence_modules:
            if 'location_conversation_microservice' in module_name:
                return self.intelligence_modules[module_name].create_conversation(botengine,
                                                                                  conversation_type,
                                                                                  homeowner_message,
                                                                                  supporter_message,
                                                                                  professional_monitoring_code=professional_monitoring_code,
                                                                                  sms_callback_method=sms_callback_method,
                                                                                  next_conversation_object=next_conversation_object,
                                                                                  force=force)

        return None

    def update_conversation(self, botengine, conversation_object, message=None, resolved=False):
        """
        Update a conversation
        :param botengine: BotEngine environment
        :param conversation_object: Conversation object to update
        :param message: Message to send out to either homeowners or supporters
        :param resolved: True to resolve and end the conversation (default is False)
        :return conversation_object for reference in update_conversation(..). Or None if this conversation will no longer be active.
        """
        if conversation_object is None:
            return None

        for module_name in self.intelligence_modules:
            if 'location_conversation_microservice' in module_name:
                return self.intelligence_modules[module_name].update_conversation(botengine, conversation_object, message, resolved)

        return None


    def total_sms_recipients(self, botengine, to_residents=True, to_supporters=True):
        """
        Get the total number of SMS recipients
        :param botengine: BotEngine environment
        :param residents: True to count the total homeowners
        :param supporters: True to count the total supporters
        :return: Integer number of recipients
        """
        return len(botengine.get_location_user_names(to_residents=to_residents, to_supporters=to_supporters, sms_only=True))

    #===========================================================================
    # Narration
    #===========================================================================
    def narrate(self, botengine, title=None, description=None, priority=None, icon=None, timestamp_ms=None, file_ids=None, extra_json_dict=None, update_narrative_id=None, update_narrative_timestamp=None, user_id=None, users=None, device_id=None, devices=None, goal_id=None, question_key=None, comment=None, status=None, microservice_identifier=None, to_user=True, to_admin=False):
        """
        Narrate some activity
        :param botengine: BotEngine environment
        :param title: Title of the event
        :param description: Description of the event
        :param priority: 0=debug; 1=info; 2=warning; 3=critical
        :param icon: Icon name, like 'motion' or 'phone-alert'. See http://peoplepowerco.com/icons
        :param timestamp_ms: Optional timestamp for this event. Can be in the future. If not set, the current timestamp is used.
        :param file_ids: List of file ID's (media) to reference and show as part of the record in the UI
        :param extra_json_dict: Any extra JSON dictionary content we want to communicate with the UI
        :param update_narrative_id: Specify a narrative ID to update an existing record.
        :param update_narrative_timestamp: Specify a narrative timestamp to update an existing record. This is a double-check to make sure we're not overwriting the wrong record.
        :param admin: True to deliver to an administrator History
        :param location: True to deliver to end user History
        :return: { "narrativeId": id, "narrativeTime": timestamp_ms } if successful, otherwise None.
        """
        payload = {}

        if user_id is not None:
            payload['user_id'] = user_id

        if users is not None:
            payload['users'] = users

        if device_id is not None:
            payload['device_id'] = device_id

        if devices is not None:
            payload['devices'] = devices

        if goal_id is not None:
            payload['goal_id'] = goal_id

        if question_key is not None:
            payload['question_key'] = question_key

        if comment is not None:
            payload['comment'] = comment

        if status is not None:
            payload['status'] = int(status)

        if extra_json_dict is None:
            extra_json_dict = payload

        else:
            extra_json_dict.update(payload)

        if to_admin:
            response_dict = botengine.narrate(self.location_id, title, description, priority, icon, timestamp_ms=timestamp_ms, file_ids=file_ids, extra_json_dict=extra_json_dict, update_narrative_id=update_narrative_id, update_narrative_timestamp=update_narrative_timestamp, admin=True)

            if response_dict is not None:
                if microservice_identifier is not None:
                    self.org_narratives[microservice_identifier] = ( response_dict['narrativeId'], response_dict['narrativeTime'] )

        else:
            if microservice_identifier is not None:
                if microservice_identifier in self.org_narratives:
                    del(self.org_narratives[microservice_identifier])

        if to_user:
            response_dict = botengine.narrate(self.location_id, title, description, priority, icon, timestamp_ms=timestamp_ms, file_ids=file_ids, extra_json_dict=extra_json_dict, update_narrative_id=update_narrative_id, update_narrative_timestamp=update_narrative_timestamp, admin=False)

            if response_dict is not None:
                if microservice_identifier is not None:
                    self.location_narratives[microservice_identifier] = (response_dict['narrativeId'], response_dict['narrativeTime'])

        else:
            if microservice_identifier is not None:
                if microservice_identifier in self.location_narratives:
                    del(self.location_narratives[microservice_identifier])

        return response_dict

    def resolve_narrative(self, botengine, microservice_identifier):
        """
        Resolve a narrative entry
        :param botengine: BotEngine environment
        :param microservice_identifier: The same microservice identifier used to create the narrative
        :param admin: True to update the admin status on this narrative
        :return:  { "narrativeId": id, "narrativeTime": timestamp_ms } if successful, otherwise None.
        """
        if microservice_identifier in self.org_narratives:
            narrative_id, narrative_timestamp = self.org_narratives[microservice_identifier]
            self.narrate(botengine, self.location_id, update_narrative_id=narrative_id, update_narrative_timestamp=narrative_timestamp, status=2, to_admin=True, to_user=False)
            del(self.org_narratives[microservice_identifier])

        if microservice_identifier in self.location_narratives:
            narrative_id, narrative_timestamp = self.location_narratives[microservice_identifier]
            self.narrate(botengine, self.location_id, update_narrative_id=narrative_id, update_narrative_timestamp=narrative_timestamp, status=2, to_admin=False, to_user=True)
            del(self.location_narratives[microservice_identifier])

    def track(self, botengine, title, properties=None):
        """
        Track analytics both in Maestro and in the 3rd party analytics package
        :param botengine: BotEngine environment
        :param title: Unique identifier for this analytic
        :param properties: JSON dictionary of properties
        """
        import importlib
        try:
            analytics = importlib.import_module('analytics')
            from copy import copy

            analytics.get_analytics(botengine).track(botengine,
                                                     event_name=title,
                                                     properties=properties)

        except ImportError:
            pass
        except Exception as e:
            botengine.get_logger().error("location.py : " + str(e))

        # Option to capture analytics details into the server database.
        # return self.narrate(botengine,
        #              title=title,
        #              description=None,
        #              priority=botengine.NARRATIVE_PRIORITY_DETAIL,
        #              icon="analytics",
        #              extra_json_dict=properties,
        #              to_admin=True,
        #              to_user=False)

    def delete_narration(self, botengine, narrative_id, narrative_timestamp):
        """
        Delete a narrative record
        :param botengine: BotEngine environment
        :param narrative_id: ID of the record to delete
        :param narrative_timestamp: Timestamp of the record to delete
        """
        botengine.delete_narration(self.location_id, narrative_id, narrative_timestamp)

    #===========================================================================
    # Mode helper methods
    #===========================================================================
    def is_present(self, botengine=None):
        """
        Is the person likely physically present in the home?
        :return: True if the person is in HOME, STAY, SLEEP, or TEST mode. False for all others.
        """
        return "ABSENT" not in self.occupancy_status \
               and "A2H" not in self.occupancy_status \
               and "H2A" not in self.occupancy_status \
               and "AWAY" not in self.occupancy_status \
               and "VACATION" not in self.occupancy_status
    
    def is_present_and_protected(self, botengine=None):
        """
        Is the person at home and wants to be alerted if the perimeter is breached?
        :return: True if the person is in STAY or SLEEP mode
        """
        return utilities.MODE_STAY in self.mode \
               or "SLEEP" in self.occupancy_status \
               or "H2S" in self.occupancy_status \
               or "S2H" in self.occupancy_status

    def is_sleeping(self, botengine=None):
        """
        :return: True if the person is about to go to sleep, or they're sleeping, or about to wake up.
        """
        return "SLEEP" in self.occupancy_status \
               or "H2S" in self.occupancy_status \
               or "S2H" in self.occupancy_status
    
    def update_mode(self, botengine):
        """
        Extract this location's current mode from our botengine environment
        :param botengine: BotEngine environment
        """
        location_block = botengine.get_location_info()
        if location_block is not None:
            if 'event' in location_block['location']:
                self.mode = str(location_block['location']['event'])

    #===========================================================================
    # Time
    #===========================================================================
    def get_local_datetime(self, botengine):
        """
        Get the datetime in the user's local timezone.
        :param botengine: BotEngine environment
        :param timestamp: Unix timestamp in milliseconds
        :returns: datetime
        """
        return self.get_local_datetime_from_timestamp(botengine, botengine.get_timestamp())
    
    def get_local_datetime_from_timestamp(self, botengine, timestamp_ms):
        """
        Get a datetime in the user's local timezone, based on an input timestamp_ms
        :param botengine: BotEngine environment
        :param timestamp_ms: Timestamp in milliseconds to transform into a timezone-aware datetime object
        """
        return datetime.datetime.fromtimestamp(timestamp_ms / 1000.0, pytz.timezone(self.get_local_timezone_string(botengine)))
        
    def get_local_timezone_string(self, botengine):
        """
        Get the local timezone string
        :param botengine: BotEngine environment
        :return: timezone string
        """
        location_block = botengine.get_location_info()

        # Try to get the user's location's timezone string
        if 'timezone' in location_block['location']:
            return location_block['location']['timezone']['id']

        return domain.DEFAULT_TIMEZONE

    def get_relative_time_of_day(self, botengine, timestamp_ms=None):
        """
        Transform our local datetime into a float hour and minutes
        :param botengine: BotEngine environment
        :param timestamp_ms: Transform this timestamp if given, otherwise transform the current time from botengine.
        :return: Relative time of day - hours.minutes where minutes is divided by 60. 10:15 AM = 10.25
        """
        if timestamp_ms is not None:
            # Use the given timestamp
            dt = self.get_local_datetime_from_timestamp(botengine, timestamp_ms)
        else:
            # Use the current time
            dt = self.get_local_datetime(botengine)

        return dt.hour + (dt.minute / 60.0)

    def get_midnight_last_night(self, botengine):
        """
        Get a datetime of midnight last night in local time
        :param botengine: BotEngine environment
        :return: Datetime object of midnight last night in the local timezone
        """
        return self.get_local_datetime(botengine).replace(hour=0, minute=0, second=0, microsecond=0)

    def get_midnight_tonight(self, botengine):
        """
        Get a datetime of midnight tonight in local time
        :param botengine: BotEngine environment
        :return: Datetime object of midnight tonight in the local timezone
        """
        return self.get_local_datetime(botengine).replace(hour=23, minute=59, second=59, microsecond=999999)


    def local_timestamp_ms_from_relative_hours(self, botengine, weekday, hours):
        """
        Calculate an absolute timestamp from relative day-of-week and hour
        :param botengine: BotEngine environment
        :param dow: day-of-week (Monday is 0)
        :param hours: Relative hours into the day (i.e. 23.5 = 11:30 PM local time)
        :return: Unix epoch timestamp in milliseconds
        """
        from datetime import timedelta

        reference = self.get_local_datetime(botengine)
        hour, minute = divmod(hours, 1)
        minute *= 60
        days = reference.weekday() - weekday
        target_dt = (reference - timedelta(days=days)).replace(hour=int(hour), minute=int(minute), second=0, microsecond=0)
        timestamp_ms = self.timezone_aware_datetime_to_unix_timestamp(botengine, target_dt)
        if timestamp_ms < botengine.get_timestamp():
            timestamp_ms += utilities.ONE_WEEK_MS

        return timestamp_ms

    def timezone_aware_datetime_to_unix_timestamp(self, botengine, dt):
        """
        Convert a local datetime / timezone-aware datetime to a unix timestamp
        :param botengine: BotEngine environment
        :param dt: Datetime to convert to unix timestamp
        :return: timestamp in milliseconds
        """
        from tzlocal import get_localzone
        return int((dt.astimezone(get_localzone())).strftime("%s")) * 1000

    def get_local_hour_of_day(self, botengine):
        """
        Get the local hour of the day (float), used in machine learning algorithms.

        Examples:
        * Midnight last night = 0.0
        * Noon = 12.0
        * 9:15 PM = 21.25

        :param botengine: BotEngine environment
        :return: hour of the day (float)
        """
        return (botengine.get_timestamp() - self.timezone_aware_datetime_to_unix_timestamp(botengine, self.get_midnight_last_night(botengine))) / 1000 / 60.0 / 60.0

    def get_local_day_of_week(self, botengine):
        """
        Get the local day of the week (0-6)

        :param botengine: BotEngine environment
        :return: local day of the week (0 - 6)
        """
        return self.get_local_datetime(botengine).weekday()


    #===========================================================================
    # Weather
    #===========================================================================
    def get_weather_forecast(self, botengine, units=None, hours=12):
        """
        Get the weather forecast for this location
        :param units: Default is Metric. 'e'=English; 'm'=Metric; 'h'=Hybrid (UK); 's'=Metric SI units (not available for all APIs)
        :param hours: Forecast depth in hours, default is 12. Available hours are 6, 12.
        :return: Weather JSON data
        """
        return botengine.get_weather_forecast_by_location(self.location_id, units, hours)

    def get_current_weather(self, botengine, units=None):
        """
        Get the current weather by Location ID
        :param units: Default is Metric. 'e'=English; 'm'=Metric; 'h'=Hybrid (UK); 's'=Metric SI units (not available for all APIs)
        :return: Weather JSON data
        """
        return botengine.get_current_weather_by_location(self.location_id, units)


    #===========================================================================
    # CSV methods for machine learning algorithm integrations
    #===========================================================================
    def get_csv(self, botengine, oldest_timestamp_ms=None, newest_timestamp_ms=None):
        """
        Get a .csv string of all the data
        :param botengine: BotEngine environment
        :param oldest_timestamp_ms: oldest timestamp in milliseconds
        :param newest_timestamp_ms: newest timestamp in milliseconds
        :return: .csv string, largely matching the .csv data you would receive from the "botengine --download_device [device_id]" command line interface. Or None if this device doesn't have data.
        """
        output = "location_id,timestamp_ms,timestamp_iso,event,source_type\n"

        try:
            modes = botengine.get_mode_history(self.location_id, oldest_timestamp_ms=oldest_timestamp_ms, newest_timestamp_ms=newest_timestamp_ms)
        except:
            # This can happen because this bot may not have read permissions for this device.
            botengine.get_logger().warning("Cannot synchronize modes history for location {}".format(self.location_id))
            return None

        if 'events' not in modes:
            return None

        botengine.get_logger().info("{} mode changes captured".format(len(modes['events'])))

        for event in modes['events']:
            timestamp_ms = event['eventDateMs']
            dt = self.get_local_datetime_from_timestamp(botengine, timestamp_ms)

            event_name = event['event'].replace(",",".")

            output += "{},{},{},{},{}".format(self.location_id, timestamp_ms, utilities.iso_format(dt), event_name, event['sourceType'])
            output += "\n"

        return output
