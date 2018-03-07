import React, { Component } from 'react';
import { BrowserRouter as Router, Route, Switch, Link } from 'react-router-dom';
import { Home, CurrentData, Settings} from './Routes';
import 'bootstrap/dist/css/bootstrap.min.css';
import { createStore, bindActionCreators, combineReducers } from 'redux';
import { Provider } from 'react-redux';
var Immutable = require('immutable');

const initialState = {
    sensor: {
      data : []
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
    }
}

const sensorReducer = (state = initialState.sensor, action) => {
    switch(action.type){
        case 'SENSOR_DATA_HISTORY':
            return Object.assign({}, state, { data: action.sensor_list }); // TODO
        case 'ADD_SENSOR_DATA':
            return Object.assign({}, state, { data: action.data }); // TODO
        default:
            return state;
    }
};
const settingsReducer = (state = initialState.settings, action) => {
    switch(action.type){
        case 'UPDATE_SETTINGS':
            return action.data;
        default:
            return state;
    }
};

const reducers = combineReducers({
    sensor: sensorReducer,
    settings: settingsReducer
})


const store = createStore( reducers );

class Navbar extends Component {
  render() {
    return(
        <nav className="navbar navbar-expand-md navbar-dark bg-dark fixed-top">
          <Link className="navbar-brand" to="/">Plantmonitor</Link>
          <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#Plantnavbar" aria-controls="navbarsExampleDefault" aria-expanded="false" aria-label="Toggle navigation">
            <span className="navbar-toggler-icon"></span>
          </button>

          <div className="collapse navbar-collapse" id="Plantnavbar">
            <ul className="navbar-nav mr-auto">
              <li className="nav-item">
                <Link className="nav-link" to="/">Home </Link>
              </li>
              <li className="nav-item">
                <Link className="nav-link" to="/CurrentData">Current Data</Link>
              </li>
            </ul>
            <span className="navbar-text">
              <Link className="navbar-brand" to="/Settings">Settings</Link>
            </span>
          </div>
        </nav>
      )
  }
}


class App extends Component {
  render() {
    return (
      <Provider store={store}>
        <Router>
          <div>
            <Navbar></Navbar>

            <main role="main" className="container" role="main" style={{'paddingTop': 5+ 'rem'}}>
              <div>
                <Switch>
                  <Route exact path="/" component={CurrentData}/>
                  <Route path="/CurrentData" component={CurrentData}/>
                  <Route path="/Settings" component={Settings}/>
                </Switch>
              </div>
            </main>
          </div>
        </Router>
      </Provider>
    );
  }
}

export default App;
