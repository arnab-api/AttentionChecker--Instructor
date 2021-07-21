// import logo from './logo.svg';
// import './App.css';

import { Switch, Route, BrowserRouter as Router } from "react-router-dom";
import { HomePage } from "./Pages/HomePage/HomePage";

function App() {
    return (
        <Router>
            <Switch>
                <Route exact path="/">
                    <HomePage />
                </Route>
            </Switch>
        </Router>
    );
}

export default App;
