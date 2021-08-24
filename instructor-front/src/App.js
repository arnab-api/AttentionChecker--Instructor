// import logo from './logo.svg';
// import './App.css';

import { Switch, Route, BrowserRouter as Router } from "react-router-dom";
import { HomePage } from "./Pages/HomePage/HomePage";
import { HomePage_sim } from "./Pages/HomePage/Homepage_sim";
import { HomePage_session } from "./Pages/HomePage/Homepage_session";


function App() {
    return (
        <Router>
            <Switch>
                <Route exact path="/">
                    <HomePage />
                </Route>
                <Route exact path="/simulation">
                    <HomePage_sim />
                </Route>
                <Route exact path="/session">
                    <HomePage_session />
                </Route>
            </Switch>
        </Router>
    );
}

export default App;
