import React, { Component } from 'react';
import axios from 'axios';


class CurrentData extends Component {
  constructor(props) {
    super(props);
    this.state = {
    }
  }

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
    let elements = Object.keys(this.state).map(
      (element) => this.add_list_element(element, this.state[element])
    )
    return(
      <div>
      <ul className="list-group">
        {elements}
      </ul>
      </div>
    )
  }
}


class Settings extends Component {
  constructor(props) {
    super(props);
    this.state = {
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
    }

    this.submitNewSettings = this.submitNewSettings.bind(this);
  }

  componentDidMount(){
    axios.get('/rest/settings')
      .then((response) => {
         this.setState(response.data) //Change
      }).catch((err) => {
         // cant set anything
      });
  }

  submitNewSettings(event){
    axios.post('/rest/settings', this.state)
    event.preventDefault();
  }

  render() {
    return(
      <form onSubmit={this.submitNewSettings}>
        <div className="form-row">
          <div className="form-group col-md-6">
             <label for="inputssid">SSID</label>
             <input type="text" className="form-control" id="inputssid" placeholder="SSID" defaultValue={this.state.wlan.ssid}
              onChange={event => this.state.wlan.ssid = event.target.value} />
           </div>
           <div className="form-group col-md-6">
             <label for="inputPassword">Password</label>
             <input type="password" className="form-control" id="inputPassword" placeholder="Password" defaultValue={ this.state.wlan.password }
              onChange={event => this.state.wlan.password = event.target.value} />
           </div>
        </div>
       <div className="form-group">
         <label for="inputRequestUrl">Requesturl (address to send current data on every wakeup)</label>
         <input type="text" className="form-control" id="inputRequestUrl" placeholder="" defaultValue={ this.state.request_url }
          onChange={event => this.state.request_url = event.target.value} />
       </div>
       <div className="form-group">
         <label for="inputConfigTime">Time in seconds for the html interface to be only if Requesturl is not set or reachable</label>
         <input type="text" className="form-control" id="inputConfigTime" placeholder="" defaultValue={ this.state.awake_time_for_config }
          onChange={event => this.state.awake_time_for_config = event.target.value} />
       </div>
       <div className="form-group">
         <label for="inputDeepsleep">Time in seconds this plantmonitor will be in deepsleep</label>
         <input type="text" className="form-control" id="inputDeepsleep" placeholder="" defaultValue={ this.state.deepsleep_s }
          onChange={event => this.state.deepsleep_s = event.target.value} />
       </div>
       <div className="form-row">
         <div className="form-group col-md-6">
            <label for="inputAwakeTime">max awake time in seconds</label>
            <input type="text" className="form-control" id="inputAwakeTime" placeholder="" defaultValue={ this.state.max_awake_time_s }
             onChange={event => this.state.max_awake_time_s = event.target.value} />
          </div>
          <div className="form-group col-md-6">
            <label for="inputKeepAlive">keep alive time in seconds</label>
            <input type="text" className="form-control" id="inputKeepAlive" placeholder="" defaultValue={ this.state.keep_alive_time_s }
              onChange={event => this.state.keep_alive_time_s = event.target.value} />
          </div>
       </div>
       <button type="submit" className="btn btn-primary">change</button>
      </form>
    )
  }
}

export {Home, CurrentData, Settings};
