import React, { Component } from 'react';
import axios from 'axios'

class Home extends Component {
  constructor(props) {
    super(props);
    this.state = {

    }
    // axios.get('/data')
  }
  render() {
    return(
      <div>Data to view</div>
    )
  }
}


class CurrentData extends Component {
  constructor(props) {
    super(props);
    this.state = {
      'loading': 0,
    }
    this.state = axios.get('/data') // das wird so nicht gerendert
      .then((response) => {
         this.state = response.data //Change
      }).catch((err) => {
         this.state = {"error": 1}
      });
  }
  add_list_element(key, value){
    return(
      <li class="list-group-item d-flex justify-content-between align-items-center">
        {key}
        <span class="badge badge-primary badge-pill">{value}</span>
      </li>
    )
  }
  render() {
    const elements = Object.keys(this.state).map(
      (element) => this.add_list_element(element, this.state[element])
    )
    return(
      <div>
      <ul class="list-group">
        {elements}
      </ul>
      </div>
    )
  }
}


const Settings = () => <div>Settings</div>;

export {Home, CurrentData, Settings};
