import React, { Component } from 'react';
import { BrowserRouter as Router, Route, Switch, Link } from 'react-router-dom';
import { Home, CurrentData, Settings} from './Routes';
import 'bootstrap/dist/css/bootstrap.min.css';

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
    );
  }
}

export default App;
