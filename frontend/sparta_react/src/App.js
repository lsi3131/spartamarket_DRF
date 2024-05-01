import logo from './logo.svg';
// import './App.css';
import {BrowserRouter, Link, Route, Switch} from "react-router-dom";
import Header from "./component/Header";
import EmptyPage from "./component/EmptyPage";
import ItemList from "./component/ItemList";
// import {Container, Row, Col} from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';

import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import {Badge, Button, Stack} from "react-bootstrap";

function App() {
    return (
        <BrowserRouter>
            <Header/>
            <Switch>
                <Route path="/" exact>
                    <ItemList/>
                </Route>
                <Route>
                    <EmptyPage/>
                </Route>
            </Switch>
        </BrowserRouter>
    );
}

export default App;
