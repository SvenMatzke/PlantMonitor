import {store, actions} from './reducer.js';
import axios from 'axios';

function get_settings(){
  axios.get('/rest/settings')
    .then((response) => {
        store.dispatch(actions.updateSettings(response.data))
    }).catch((err) => {
        store.dispatch(actions.addError(err.message))
    });
}

function get_sensor_data(){
  axios.get('/rest/data')
    .then((response) => {
        store.dispatch(actions.updateSettings(response.data))
    }).catch((err) => {
        store.dispatch(actions.addError(err.message))
    });
}

function configure_sensor(){
  axios.post('/rest/configure', "")
  .catch((err) => {
      store.dispatch(actions.addError(err.message))
  });
}

function get_sensor_history(){
  axios.get('/rest/get_sensor_history')
    .then((response) => {
        store.dispatch(actions.updateSettings(response.data))
    }).catch((err) => {
        store.dispatch(actions.addError(err.message))
    });
}

function post_settings(settings){
   axios.post('/rest/settings', settings)
   .catch((err) => {
       store.dispatch(actions.addError(err.message))
   });
}

function send_deep_sleep(){
    console.log(store.getState())
    axios.post('/rest/senddeepsleep', "")
    .catch((err) => {
        store.dispatch(actions.addError(err.message))
    });
}

export {send_deep_sleep, post_settings, get_sensor_history, configure_sensor, get_sensor_data, get_settings};
