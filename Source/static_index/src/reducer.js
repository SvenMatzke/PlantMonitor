import { createStore, combineReducers } from 'redux';

const initialState = {
    sensor_history: [
      {
        "soil moisture": 0,
        "humidity": 0,
        "light": 0,
        "temperature": 0,
        "time": 0
      }
    ],
    data: {
      "soil moisture": 0,
      "humidity": 0,
      "light": 0,
      "temperature": 0
    },
    settings: {
      "wlan" : {
         "ssid" : "",
         "password" : ""
      },
      "deepsleep_s" : 600,
      "keep_alive_time_s" : 30,
      "max_awake_time_s" : 120,
      "awake_time_for_config" : 180,
      "request_url" : "",
      "added_infos_to_sensor_data" : {}
    },
    errormessages: []
}

const sensorReducer = (state = initialState.data, action) => {
    switch(action.type){
        case 'ADD_SENSOR_DATA':
            return Object.assign({}, state, action.data);
        default:
            return state;
    }
};

const sensorHistoryReducer = (state = initialState.sensor_history, action) => {
    switch(action.type){
        case 'SENSOR_DATA_HISTORY':
            return [... action.data];
        default:
            return state;
    }
};

const settingsReducer = (state = initialState.settings, action) => {
    switch(action.type){
        case 'UPDATE_SETTINGS':
            return Object.assign({}, state, action.data);
        default:
            return state;
    }
};

const errorReducer = (state = initialState.errormessages, action) => {
  switch(action.type){
      case 'ADD_ERROR':
          return [... action.data];
      default:
          return state;
  }
}


const reducers = combineReducers({
    sensor_history: sensorHistoryReducer,
    data: sensorReducer,
    settings: settingsReducer,
    errormessages: errorReducer,
})


const store = createStore( reducers );


const actions = {
    updateSensorHistory: sensor_data_list => (
      { type: 'SENSOR_DATA_HISTORY',
        data: sensor_data_list}
      ),
    addSensorData: sensor_data => (
      {
        type: 'ADD_SENSOR_DATA',
        data: sensor_data
      }
    ),
    updateSettings: settings => (
      {
        type: 'UPDATE_SETTINGS',
        data : settings
      }
    ),
    addError: errormessage => (
      {
        type: 'ADD_ERROR',
        data: errormessage
      }
    )
};

export {store, actions};
