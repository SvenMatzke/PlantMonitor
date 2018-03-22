import React, { Component } from 'react';
import { BrowserRouter as Router, Route, Switch, Link } from 'react-router-dom';
import { Home, CurrentData, Settings} from './Routes';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
// import 'bootstrap/dist/css/bootstrap.min.css';
import { createStore, bindActionCreators, combineReducers } from 'redux';

import Paper from 'material-ui/Paper';
import Menu from 'material-ui/Menu';
import MenuItem from 'material-ui/MenuItem';
import RemoveRedEye from 'material-ui/svg-icons/image/remove-red-eye';
import PersonAdd from 'material-ui/svg-icons/social/person-add';
import ContentLink from 'material-ui/svg-icons/content/link';
import Divider from 'material-ui/Divider';
import ContentCopy from 'material-ui/svg-icons/content/content-copy';
import Download from 'material-ui/svg-icons/file/file-download';
import Delete from 'material-ui/svg-icons/action/delete';
import FontIcon from 'material-ui/FontIcon';
import Drawer from 'material-ui/Drawer';
import Subheader from 'material-ui/Subheader';
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
      <MuiThemeProvider>
        <Provider store={store}>

          <Router>
            <div>

        <AppBar
          position="absolute"
          className={classNames(classes.appBar, this.state.open && classes.appBarShift)}
        >
          <Toolbar disableGutters={!this.state.open}>
            <IconButton
              color="inherit"
              aria-label="open drawer"
              onClick={this.handleDrawerOpen}
              className={classNames(classes.menuButton, this.state.open && classes.hide)}
            >
              <MenuIcon />
            </IconButton>
            <Typography variant="title" color="inherit" noWrap>
              Mini variant drawer
            </Typography>
          </Toolbar>
        </AppBar>
        <Drawer
          variant="permanent"
          classes={{
            paper: classNames(classes.drawerPaper, !this.state.open && classes.drawerPaperClose),
          }}
          open={this.state.open}
        >
          <div className={classes.toolbar}>
            <IconButton onClick={this.handleDrawerClose}>
              {theme.direction === 'rtl' ? <ChevronRightIcon /> : <ChevronLeftIcon />}
            </IconButton>
          </div>
          <Divider />
          <List>{mailFolderListItems}</List>
          <Divider />
          <List>{otherMailFolderListItems}</List>
        </Drawer>
        <main className={classes.content}>
          <div className={classes.toolbar} />
          <Typography noWrap>{'You think water moves fast? You should see ice.'}</Typography>
        </main>


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
      </MuiThemeProvider>
    );
  }
}

export default App;
