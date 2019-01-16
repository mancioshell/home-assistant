import logging
import time
from homeassistant.helpers.entity import Entity

DEPENDENCIES = ['sensor']
REQUIREMENTS = ['Adafruit-CharLCD==1.1.1']

CONF_DISPLAY_DATA = 'data'
CONF_DISPLAY_ROWS = 'rows'
CONF_DISPLAY_COLUMNS= 'columns'

_LOGGER = logging.getLogger(__name__)


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the sensor platform."""
    import Adafruit_CharLCD as LCD

    data = config[CONF_DISPLAY_DATA]
    rows = config[CONF_DISPLAY_ROWS]
    columns = config[CONF_DISPLAY_COLUMNS]
 
    #lcd = LCD.Adafruit_CharLCDBackpack()
    #add_devices([CharLCDBackpack(lcd, data, rows, columns)])     
    
    add_devices([CharLCDBackpack(None, data, rows, columns)])     


class Num(object):
    """Representation of a Num."""

    def __init__(self, count):
        self.count = count


class CharLCDBackpack(Entity):
    """Representation of a CharLCD."""

    def __init__(self, lcd, data, rows, columns):
        """Initialize the CharLCDBackpack."""
        self._state = None
        self.lcd = lcd
        self.data = data
        self.rows = rows
        self.columns = columns

    @property
    def name(self):
        """Return the name of the lcd char."""
        return 'Char CharLCDBackpack'

    @property
    def state(self):
        """Return the state of the char lcd."""
        return self._state

    def create_message(self, data):
        """Return message string to write in lcd char display."""

        key = self.data['key']
        description = self.data['description']

        state = self.hass.states.get(key)
        if state is None:
            _LOGGER.error("There isn't any entity_id whith value {}".format(key))
            return None
        else:
            value = state.as_dict()['state']
            return "{} : {} - {}".format(description, value, self.num.count)
    
    def show_message(self, message):
        """Show message to lcd char display."""
        for i in range(self.columns-len(message)):
            time.sleep(0.5)
            self.lcd.move_right()
        for i in range(self.columns-len(message)):
            time.sleep(0.5)
            self.lcd.move_left()

    def update(self):
        """Write data to the lcd char
        This is the only method that should write new data in lcd char for Home Assistant.
        """

        i = 0
        for value in self.data:
            if i >= self.rows:
                break

            message = self.create_message(value)
            if message is not None: 
                #self.lcd.clear()
                #self.lcd.message("{}\n".format(message))
                _LOGGER.error("{}\n".format(message))
                #self.show_message(message)

                i = i+1