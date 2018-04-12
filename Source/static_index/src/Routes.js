import React, { Component } from 'react';
import {store} from './reducer.js';
import {post_settings} from './rest_request.js';
import TextField from 'material-ui/TextField';
import Button from 'material-ui/Button';
import PropTypes from 'prop-types';
import { withStyles } from 'material-ui/styles';
import {LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend} from 'recharts';
import {get_settings, get_sensor_history} from './rest_request.js';


const styles = theme => ({
  container: {
    display: 'flex',
    flexWrap: 'wrap',
  },
  textField: {
    marginLeft: theme.spacing.unit,
    marginRight: theme.spacing.unit,
    width: 200,
  },
  menu: {
    width: 200,
  },
});

class Home extends Component {
  componentDidMount() {
    get_sensor_history()
  }

  render() {
    store.subscribe(
        () => {
          this.setState(store.getState().sensor_history);
        }
    )

    return(
      <LineChart width={700} height={450} data={store.getState().sensor_history}
            margin={{top: 50, right: 30, left: 20, bottom: 5}}>
       <XAxis dataKey="time"/>
       <YAxis/>
       <CartesianGrid strokeDasharray="3 3"/>
       <Tooltip/>
       <Legend />
       <Line type="monotone" dataKey="temperature" stroke="#8b3333" activeDot={{r: 2}}/>
       <Line type="monotone" dataKey="light" stroke="#a1a100" />
       <Line type="monotone" dataKey="humidity" stroke="#00539c" />
       <Line type="monotone" dataKey="soil moisture" stroke="#4b4833" />
      </LineChart>
    )
  }
}

class SettingsComp extends Component {

  componentDidMount() {
    get_settings()
  }

  render() {
    const { classes } = this.props;
    const settings = this.state;
    store.subscribe(
        () => {
          this.setState(store.getState().settings);
        }
    )

    if(!this.state){
      return "loading"
    }
    return(
      <form className={classes.container} noValidate autoComplete="off"
            onSubmit={event => {post_settings(settings);event.preventDefault();}} >
        <TextField
           id="ssid"
           label="ssid"
           className={classes.textField}
           defaultValue={settings.wlan.ssid}
           onChange={event => settings.wlan.ssid = event.target.value}
           margin="normal"
        />
        <TextField
           id="password"
           label="password"
           type="password"
           className={classes.textField}
           defaultValue={settings.wlan.password}
           onChange={event => settings.wlan.password = event.target.value}
           margin="normal"
        />
        <TextField
           id="request_url"
           label="request url"
           className={classes.textField}
           defaultValue={settings.request_url}
           onChange={event => settings.request_url = event.target.value}
           margin="normal"
        />
        <TextField
           id="reads_without_send"
           label="reads without send"
           className={classes.textField}
           defaultValue={settings.reads_without_send}
           onChange={event => settings.reads_without_send = event.target.value}
           margin="normal"
        />
        <TextField
           id="inputConfigTime"
           label="configuration time"
           className={classes.textField}
           defaultValue={settings.awake_time_for_config}
           onChange={event => settings.awake_time_for_config = event.target.value}
           margin="normal"
        />
        <TextField
           id="inputDeepsleep"
           label="deepsleep time in s"
           className={classes.textField}
           defaultValue={settings.deepsleep_s}
           onChange={event => settings.deepsleep_s = event.target.value}
           margin="normal"
        />
        <TextField
           id="inputAwakeTime"
           label="max awake time in s"
           className={classes.textField}
           defaultValue={settings.max_awake_time_s}
           onChange={event => settings.max_awake_time_s = event.target.value}
           margin="normal"
        />
        <TextField
           id="inputKeepAlive"
           label="keep alive time in s"
           className={classes.textField}
           defaultValue={settings.keep_alive_time_s}
           onChange={event => settings.keep_alive_time_s = event.target.value}
           margin="normal"
        />
        <Button variant="raised" type="submit">
          change
        </Button>
      </form>
    )
  }
}
SettingsComp.propTypes = {
  classes: PropTypes.object.isRequired,
};
const Settings = withStyles(styles)(SettingsComp)
export {Home, Settings};
