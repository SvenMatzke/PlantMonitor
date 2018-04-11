import {store, actions} from './reducer.js';
import axios from 'axios';

let host = ""
if (process.env.NODE_ENV !== 'production') {
   host = "http://127.0.0.1:8080"
}

function get_settings(){
  axios.get(host+'/rest/settings')
    .then((response) => {
        store.dispatch(actions.updateSettings(response.data))
    }).catch((err) => {
        store.dispatch(actions.addError(err.message))
    });
}

function get_sensor_data(){
  axios.get(host+'/rest/data')
    .then((response) => {
        store.dispatch(actions.addSensorData(response.data))
    }).catch((err) => {
        store.dispatch(actions.addError(err.message))
    });
}

function configure_sensor(){
  axios.post(host+'/rest/configure', "")
  .catch((err) => {
      store.dispatch(actions.addError(err.message))
  });
}

function get_sensor_history(){
  axios.get(host+'/rest/sensor_history')
    .then((response) => {
        store.dispatch(actions.updateSensorHistory(response.data))
    }).catch((err) => {
        store.dispatch(actions.addError(err.message))
    });
}

function post_settings(settings){
   axios.post(host+'/rest/settings', settings)
   .catch((err) => {
       store.dispatch(actions.addError(err.message))
   });
}

function send_deep_sleep(){
    axios.post(host+'/rest/senddeepsleep', "")
    .catch((err) => {
        store.dispatch(actions.addError(err.message))
    });
}

export {send_deep_sleep, post_settings, get_sensor_history, configure_sensor, get_sensor_data, get_settings};
