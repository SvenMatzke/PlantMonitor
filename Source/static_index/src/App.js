import React, { Component } from 'react';
import { BrowserRouter as Router, Route, Switch, Link } from 'react-router-dom';
import { Home, CurrentData, Settings} from './Routes';
import 'bootstrap/dist/css/bootstrap.min.css';

class Navbar extends Component {
  render() {
    return(
        <nav class="navbar navbar-expand-md navbar-dark bg-dark fixed-top">
          <Link class="navbar-brand" to="/">Plantmonitor</Link>
          <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarsExampleDefault" aria-controls="navbarsExampleDefault" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
          </button>

          <div class="collapse navbar-collapse" id="navbarsExampleDefault">
            <ul class="navbar-nav mr-auto">
              <li class="nav-item">
                <Link class="nav-link" to="#">Home </Link>
              </li>
              <li class="nav-item">
                <Link class="nav-link" to="/CurrentData">Current Data</Link>
              </li>

            </ul>
          </div>
        </nav>
      )
  }
}


class App extends Component {
  render() {
    return (
      <Router>
        <div>
          <Navbar></Navbar>

          <main role="main" class="container" role="main" style={{'padding-top': 5+ 'rem'}}>
            <div>
              <Switch>
                <Route exact path="/" component={Home}/>
                <Route path="/CurrentData" component={CurrentData}/>
                <Route path="/Settings" component={Settings}/>
              </Switch>
            </div>
          </main>
        </div>
      </Router>
    );
  }
}

export default App;
