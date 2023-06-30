#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab
#########################################################################
#  Code based on https://github.com/Bouni/python-luxtronik
#  Copyright 2021      Michael Schatz
#########################################################################
#  This file is part of SmartHomeNG.
#  https://www.smarthomeNG.de
#  https://knx-user-forum.de/forum/supportforen/smarthome-py
#
#  Plugin for the heatpump controller luxtronik
#  This plugin is based on the code of this github repository: https://github.com/Bouni/python-luxtronik
#
#  SmartHomeNG is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  SmartHomeNG is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with SmartHomeNG. If not, see <http://www.gnu.org/licenses/>.
#
#########################################################################

import logging
import socket
import struct

from lib.model.smartplugin import *
from lib.item import Items

from .calculations import Calculations
from .parameters import Parameters
from .visibilities import Visibilities

#from .webif import WebInterface

class luxtronik(SmartPlugin):
    """
    Main class of the Plugin. Does all plugin specific stuff and provides
    the update functions for the items
    """

    PLUGIN_VERSION = '1.1.0'    # (must match the version specified in plugin.yaml), use '1.0.0' for your initial plugin 

    def __init__(self, sh):

        # Call init code of parent class (SmartPlugin)
        super().__init__()
        self.logger = logging.getLogger(__name__)
        #self.logger.debug("Plugin geladen")

        self._host = self.get_parameter_value('host')
        self._port = self.get_parameter_value('port')
        self._socket = None

        # cycle time in seconds, only needed, if hardware/interface needs to be
        # polled for value changes by adding a scheduler entry in the run method of this plugin
        # (maybe you want to make it a plugin parameter?)
        self._cycle = self.get_parameter_value('cycle')

        # Initialization code goes here
        self.run()

        # On initialization error use:
        #   self._init_complete = False
        #   return

        # if plugin should start even without web interface
        #self.init_webinterface(WebInterface)
        # if plugin should not start without web interface
        # if not self.init_webinterface():
        #     self._init_complete = False

        return

    def run(self):
        """
        Run method for the plugin
        """
        self.alive = True
        #self.logger.debug("Run method called with cycle")
        # setup scheduler for device poll loop   (disable the following line, if you don't need to poll the device. Rember to comment the self_cycle statement in __init__ as well)
        #self.scheduler_add('poll_device', self.poll_device, cycle=self._cycle)
        self.scheduler_add('poll_device', self._poll_device, cycle=self._cycle)
        #self.scheduler_add("poll_device", self._poll_device, prio=3, cron=None, cycle=self._cycle, value=None, offset=None, next=None)

        #self.alive = True
        # if you need to create child threads, do not make them daemon = True!
        # They will not shutdown properly. (It's a python bug)

    def stop(self):
        """
        Stop method for the plugin
        """
        #self.logger.debug("Stop method called")
        self.scheduler_remove('poll_device')
        self.alive = False

    def parse_item(self, item):
        """
        Default plugin parse_item method. Is called when the plugin is initialized.
        The plugin can, corresponding to its attribute keywords, decide what to do with
        the item in future, like adding it to an internal array for future reference
        :param item:    The item to process.
        :return:        If the plugin needs to be informed of an items change you should return a call back function
                        like the function update_item down below. An example when this is needed is the knx plugin
                        where parse_item returns the update_item function when the attribute knx_send is found.
                        This means that when the items value is about to be updated, the call back function is called
                        with the item, caller, source and dest as arguments and in case of the knx plugin the value
                        can be sent to the knx with a knx write function within the knx plugin.
        """
        #if self.has_iattr(item.conf, 'luxtronik_calculations'):
            #self.logger.debug("parse item: {}".format(item))
            #_items-configuration
            #hier weiter machen!
            #self.calculations.get("ID_WEB_Temperatur_TVL") = item
            #self._items[self.get_iattr_value(item.conf, 'luxtronik_calculations')] = item
            #return self.update_item

        # todo
        # if interesting item for sending values:
        #   return self.update_item

    #def parse_logic(self, logic):
    #    """
    #    Default plugin parse_logic method
    #    """
    #    if 'xxx' in logic.conf:
            # self.function(logic['name'])
    #        pass

    def update_item(self, item, caller=None, source=None, dest=None):
        """
        Item has been updated

        This method is called, if the value of an item has been updated by SmartHomeNG.
        It should write the changed value out to the device (hardware/interface) that
        is managed by this plugin.

        :param item: item to be updated towards the plugin
        :param caller: if given it represents the callers name
        :param source: if given it represents the source
        :param dest: if given it represents the dest
        """
        #if self.alive and caller != self.get_shortname():
            # code to execute if the plugin is not stopped
            # and only, if the item has not been changed by this this plugin:
            #self.logger.info("Update item: {}, item has been changed outside this plugin".format(item.id()))

           #if self.has_iattr(item.conf, 'luxtronik_calculations'):
           #    self.logger.debug("update_item was called with item '{}' from caller '{}', source '{}' and dest '{}'".format(item, caller, source, dest))
           # pass

    def _poll_device(self):
        """
        Polls for updates of the device

        This method is only needed, if the device (hardware/interface) does not propagate
        changes on it's own, but has to be polled to get the actual status.
        It is called by the scheduler which is set within run() method.
        """
        # get the value from the device
        self.calculations = Calculations()
        self.parameters = Parameters(safe=True)
        self.visibilities = Visibilities()
        self.read()
        
        items = Items.get_instance()
        for item in items.find_items('luxtronik_calculations'):
            item(repr(self.calculations.get(item.conf['luxtronik_calculations'])),self.get_shortname())
        pass


# ab hier https://github.com/Bouni/python-luxtronik
    def _connect(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((self._host, self._port))
        self.logger.info("Connected to Luxtronik heatpump %s:%s", self._host, self._port)

    def _disconnect(self):
        self._socket.close()
        self.logger.info("Disconnected from Luxtronik heatpump  %s:%s", self._host, self._port)
        
    def read(self):
        """Read data from heatpump."""
        self._connect()
        self._read_parameters()
        self._read_calculations()
        self._read_visibilities()
        self._disconnect()
        
    #def write skipped
    
    def _read_parameters(self):
        data = []
        self._socket.sendall(struct.pack(">ii", 3003, 0))
        cmd = struct.unpack(">i", self._socket.recv(4))[0]
        self.logger.debug("Command %s", cmd)
        length = struct.unpack(">i", self._socket.recv(4))[0]
        self.logger.debug("Length %s", length)
        for _ in range(0, length):
            try:
                data.append(struct.unpack(">i", self._socket.recv(4))[0])
            except struct.error as err:
                # not logging this as error as it would be logged on every read cycle
                self.logger.debug("%s: %s", self._host, err)
        self.logger.info("Read %d parameters", length)
        self.parameters.parse(data)

    def _read_calculations(self):
        data = []
        self._socket.sendall(struct.pack(">ii", 3004, 0))
        cmd = struct.unpack(">i", self._socket.recv(4))[0]
        self.logger.debug("Command %s", cmd)
        stat = struct.unpack(">i", self._socket.recv(4))[0]
        self.logger.debug("Stat %s", stat)
        length = struct.unpack(">i", self._socket.recv(4))[0]
        self.logger.debug("Length %s", length)
        for _ in range(0, length):
            try:
                data.append(struct.unpack(">i", self._socket.recv(4))[0])
            except struct.error as err:
                # not logging this as error as it would be logged on every read cycle
                self.logger.debug("%s: %s", self._host, err)
        self.logger.info("Read %d calculations", length)
        self.calculations.parse(data)

    def _read_visibilities(self):
        data = []
        self._socket.sendall(struct.pack(">ii", 3005, 0))
        cmd = struct.unpack(">i", self._socket.recv(4))[0]
        self.logger.debug("Command %s", cmd)
        length = struct.unpack(">i", self._socket.recv(4))[0]
        self.logger.debug("Length %s", length)
        for _ in range(0, length):
            try:
                data.append(struct.unpack(">b", self._socket.recv(1))[0])
            except struct.error as err:
                # not logging this as error as it would be logged on every read cycle
                self.logger.debug("%s: %s", self._host, err)
        self.logger.info("Read %d visibilities", length)
        self.visibilities.parse(data)