import React, { Component } from 'react';
import { BrowserRouter as Router, Route, Switch, Link } from 'react-router-dom';

import { Provider } from 'react-redux';

import {MuiThemeProvider, createMuiTheme } from 'material-ui/styles';
import green from 'material-ui/colors/green';
import List, { ListItem, ListItemIcon, ListItemText, ListSubheader } from 'material-ui/List';
import PropTypes from 'prop-types';
import { withStyles } from 'material-ui/styles';
import Drawer from 'material-ui/Drawer';
import AppBar from 'material-ui/AppBar';
import Toolbar from 'material-ui/Toolbar';
import Typography from 'material-ui/Typography';
import Divider from 'material-ui/Divider';
import TimelineIcon from 'material-ui-icons/Timeline';
import SettingsIcon from 'material-ui-icons/Settings';
import LightIcon from 'material-ui-icons/WbSunny';
import TemperatureIcon from 'material-ui-icons/Whatshot';
import PlantIcon from 'material-ui-icons/LocalFlorist';
import HumidityIcon from 'material-ui-icons/Opacity';
import DeepsleepIcon from 'material-ui-icons/Snooze';

import {store} from './reducer.js';
import {Home, Settings} from './Routes';
import {get_sensor_history, get_sensor_data, get_settings, send_deep_sleep} from './rest_request.js';

const drawerWidth = 240;

const rootStyles = theme => ({
  root: {
      flexGrow: 1,
      zIndex: 1,
      overflow: 'hidden',
      position: 'relative',
      display: 'flex',
    },
    appBar: {
      zIndex: theme.zIndex.drawer + 1,
    },
    drawerPaper: {
      position: 'relative',
      width: drawerWidth,
    },
    content: {
      flexGrow: 1,
      backgroundColor: theme.palette.background.default,
      padding: theme.spacing.unit * 3,
      minWidth: 0, // So the Typography noWrap works
    },
    toolbar: theme.mixins.toolbar,
});

const theme = createMuiTheme({
  palette: {
    primary: green,
  },
});

function Menue(props) {
    const { classes, store, set_deep_sleep } = props;
    const sensor_data = store.getState().data;
    return (
      <MuiThemeProvider theme={theme}>
        <Provider store={store}>
          <Router>
            <div className={classes.root}>
              <AppBar
                position="absolute"
                className={classes.appBar}
                title="Plantmonitor"
              >
                <Toolbar>
                  <Typography variant="title" color="inherit" noWrap>
                    Plantmonitor
                  </Typography>
                </Toolbar>
              </AppBar>
              <Drawer
                variant="permanent"
                classes={{
                    paper: classes.drawerPaper,
                }}
                >
                <div className={classes.toolbar} />
                <Link to="/">
                  <List>
                    <ListItem button>
                    <ListItemIcon>
                       <TimelineIcon />
                    </ListItemIcon>
                        <ListItemText primary="Monitor" />
                    </ListItem>
                  </List>
                </Link>
                <Divider inset={true} />
                <List>
                  <ListSubheader>Sensordata:</ListSubheader>
                  <ListItem>
                    <ListItemIcon>
                       <LightIcon />
                    </ListItemIcon>
                    <ListItemText  inset primary="light" />
                    { sensor_data["light"] }
                  </ListItem>
                  <ListItem>
                    <ListItemIcon>
                       <TemperatureIcon />
                    </ListItemIcon>
                    <ListItemText  inset primary="temperature" />
                    { sensor_data["temperature"] }
                  </ListItem>
                  <ListItem>
                    <ListItemIcon>
                       <HumidityIcon />
                    </ListItemIcon>
                    <ListItemText  inset primary="humidiy" />
                    { sensor_data["humidiy"] }
                  </ListItem>
                  <ListItem>
                    <ListItemIcon>
                       <PlantIcon />
                    </ListItemIcon>
                    <ListItemText  inset primary="soil moisture" />
                    { sensor_data["soil moisture"] }
                    </ListItem>
                </List>
                <Divider inset={true} />
                <Link to="/Settings">
                  <List>
                    <ListItem button>
                      <ListItemIcon>
                         <SettingsIcon />
                      </ListItemIcon>
                      <ListItemText primary="Settings" />
                    </ListItem>
                  </List>
                </Link>
                <List>
                  <ListItem button onClick={set_deep_sleep}>
                    <ListItemIcon>
                       <DeepsleepIcon />
                    </ListItemIcon>
                    <ListItemText primary="deepsleep" />
                  </ListItem>
                </List>
              </Drawer>
              <main role="main" className={classes.content}>
                <div className={classes.toolbar} />
                 <div>
                   <Switch>
                     <Route exact path="/" component={Home}/>
                     <Route path="/Settings" component={Settings}/>
                   </Switch>
                 </div>
              </main>
            </div>
          </Router>
        </Provider>
      </MuiThemeProvider>);
}


Menue.propTypes = {
  classes: PropTypes.object.isRequired,
  store: PropTypes.object.isRequired,
  set_deep_sleep: PropTypes.func.isRequired
};
Menue = withStyles(rootStyles)(Menue);

class App extends Component {
    componentWillMount() {
      get_settings();
      get_sensor_data();
      get_sensor_history();
    }

    set_deep_sleep(){
      alert("Sending Plantmonitor to deepsleep after this.")
      send_deep_sleep()
    }

    render(){
      return <Menue set_deep_sleep={this.set_deep_sleep} store={store}/>
    }
}

export default App;
