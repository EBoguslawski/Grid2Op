# Copyright (c) 2019-2023, RTE (https://www.rte-france.com)
# See AUTHORS.txt
# This Source Code Form is subject to the terms of the Mozilla Public License, version 2.0.
# If a copy of the Mozilla Public License, version 2.0 was not distributed with this file,
# you can obtain one at http://mozilla.org/MPL/2.0/.
# SPDX-License-Identifier: MPL-2.0
# This file is part of Grid2Op, Grid2Op a testbed platform to model sequential decision making in power systems.

import copy
import os
from typing import Optional, Tuple
from grid2op.Space import RandomObject
from datetime import timedelta, datetime


# TODO logger !
class BaseHandler(RandomObject):
    """This is the base class that represents a time series "handler".
    
    Basically a "handler" will, for a certain type of data (*eg* load_p or maintenance etc.)
    handle the way this data type is generated.
    
    To be a valid "handler" an class must first inherit from :class:`BaseHandler` and then implements:
    TODO
    
    
    If the data represents "real time" data (*ie* the data seen by the agent in real 
    time in the observation) then it needs to implement TODO
    
    If the data represents "forecast data" (*ie* the data accessed by the agent when it uses
    :func:`grid2op.Observation.BaseObservation.simulate` or :class:`grid2op.simulator.Simulator`
    or :func:`grid2op.Observation.BaseObservation.get_forecasted_env`) then it needs to implement
    TODO
    
    And if the "handler" represents a 
    """
    def __init__(self, array_name, max_iter=-1, h_forecast=(5, )):
        super().__init__()
        self.max_iter : int = max_iter
        self.init_datetime : Optional[datetime] = None
        self.time_interval : Optional[timedelta] = None
        self.array_name : str = array_name
        self._h_forecast : tuple = copy.deepcopy(h_forecast)
        self.path : Optional[os.PathLike] = None
        self.max_episode_duration : Optional[int] = None
    
    def set_max_iter(self, max_iter):
        if max_iter is not None:
            self.max_iter = int(max_iter)
        else:
            self.max_iter = -1
            
    def set_max_episode_duration(self, max_episode_duration):
        if max_episode_duration is not None:
            self.max_episode_duration = int(max_episode_duration)
        else:
            self.max_episode_duration = None
        
    def get_max_iter(self):
        return self.max_iter
    
    def set_path(self, path):
        self.path = path
    
    def set_chunk_size(self, chunk_size):
        # Chunk size is part of public API but has no sense for 
        # data not read from a disk
        pass
        
    def set_times(self,
                  init_datetime,
                  time_interval):
        self.init_datetime = init_datetime
        self.time_interval = time_interval
    
    def _clear(self):
        self.init_datetime = None
        self.time_interval = None

    def get_kwargs(self, dict_):
        # no need to remember special kwargs for the base class
        pass
    
    def set_h_forecast(self, h_forecast):
        self._h_forecast = copy.deepcopy(h_forecast)
    
    def get_available_horizons(self):
        return copy.deepcopy(self._h_forecast)
        
    def initialize(self, order_backend_arrays, names_chronics_to_backend):
        raise NotImplementedError()
    
    def done(self):
        raise NotImplementedError()
    
    def load_next(self, dict_):
        raise NotImplementedError()
    
    def check_validity(self, backend):
        raise NotImplementedError()    
    
    def load_next_maintenance(self):
        # TODO
        raise NotImplementedError()
    
    def load_next_hazard(self):
        # TODO
        raise NotImplementedError()
        
    def forecast(self,
                 forecast_horizon_id : int,
                 inj_dict_env : dict,
                 inj_dict_previous_forecast : dict,
                 # eg gen_p_handler if this is set to gen_p_for_handler:
                 env_handler : "BaseHandler",  
                 # list of the 4 env handlers: (load_p_handler, load_q_handler, gen_p_handler, gen_v_handler)
                 env_handlers : Tuple["BaseHandler", "BaseHandler", "BaseHandler", "BaseHandler"]
                 ):
        raise NotImplementedError()
    
    def get_future_data(self, horizon: int):
        return None
