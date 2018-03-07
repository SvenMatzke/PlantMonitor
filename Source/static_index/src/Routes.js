import React, { Component } from 'react';
import { bindActionCreators} from 'redux';
import { connect } from 'react-redux';
import axios from 'axios';
var Immutable = require('immutable');

const actions = {
    updateSensorHistory: sensor_data_list => (
      { type: 'SENSOR_DATA_HISTORY',
        sensor_list: sensor_data_list}
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
    )
};

class CurrentData extends Component {
    componentDidMount(){
    axios.get('/rest/data')
      .then((response) => {
         this.setState(response.data) //Change
      }).catch((err) => {
         this.setState(Object.assign({"Current data could not be recived": 404}))
      });
  }

  add_list_element(key, value){
    return(
      <li className="list-group-item d-flex justify-content-between align-items-center">
        {key}
        <span className="badge badge-primary badge-pill">{value}</span>
      </li>
    )
  }
  render() {
    let elements = "data"
    // Object.keys(settings).map(
    //   (element) => this.add_list_element(element, settings[element])
    // )
    return(
      <div>
      <ul className="list-group">
        {elements}
      </ul>
      </div>
    )
  }
}


class SettingsComp extends Component {

  componentDidMount(){
    axios.get('/rest/settings')
      .then((response) => {
          this.acts.updateSettings(response.data)
      }).catch((err) => {
         // cant set anything
      });
  }

  submitNewSettings(event){
    const { settings, acts } = this.props;
    axios.post('/rest/settings', settings)
    event.preventDefault();
  }

  render() {
    const { settings, acts } = this.props;
    return(
      <form onSubmit={this.submitNewSettings}>
        <div className="form-row">
          <div className="form-group col-md-6">
             <label for="inputssid">SSID</label>
             <input type="text" className="form-control" id="inputssid" placeholder="SSID" value={settings.wlan.ssid}
              />
           </div>
           <div className="form-group col-md-6">
             <label for="inputPassword">Password</label>
             <input type="password" className="form-control" id="inputPassword" placeholder="Password" defaultValue={ settings.wlan.password }
              onChange={event => settings.wlan.password = event.target.value} />
           </div>
        </div>
       <div className="form-group">
         <label for="inputRequestUrl">Requesturl (address to send current data on every wakeup)</label>
         <input type="text" className="form-control" id="inputRequestUrl" placeholder="" defaultValue={ settings.request_url }
          onChange={event => settings.request_url = event.target.value} />
       </div>
       <div className="form-group">
         <label for="inputConfigTime">Time in seconds for the html interface to be only if Requesturl is not set or reachable</label>
         <input type="text" className="form-control" id="inputConfigTime" placeholder="" defaultValue={ settings.awake_time_for_config }
          onChange={event => settings.awake_time_for_config = event.target.value} />
       </div>
       <div className="form-group">
         <label for="inputDeepsleep">Time in seconds this plantmonitor will be in deepsleep</label>
         <input type="text" className="form-control" id="inputDeepsleep" placeholder="" defaultValue={ settings.deepsleep_s }
          onChange={event => settings.deepsleep_s = event.target.value} />
       </div>
       <div className="form-row">
         <div className="form-group col-md-6">
            <label for="inputAwakeTime">max awake time in seconds</label>
            <input type="text" className="form-control" id="inputAwakeTime" placeholder="" defaultValue={ settings.max_awake_time_s }
             onChange={event => settings.max_awake_time_s = event.target.value} />
          </div>
          <div className="form-group col-md-6">
            <label for="inputKeepAlive">keep alive time in seconds</label>
            <input type="text" className="form-control" id="inputKeepAlive" placeholder="" defaultValue={ settings.keep_alive_time_s }
              onChange={event => settings.keep_alive_time_s = event.target.value} />
          </div>
       </div>
       <button type="submit" className="btn btn-primary">change</button>
      </form>
    )
  }
}

const Settings = connect(
  state => ({settings: state.settings }),
  dispatch=> { acts: bindActionCreators(actions, dispatch) }
)(SettingsComp)

export {CurrentData, Settings};
