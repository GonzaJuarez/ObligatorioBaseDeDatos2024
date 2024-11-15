import { useState } from 'react'
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom'
import Home from './components/Home.jsx'
import Login from './components/Login.jsx'
import Alumnos from './components/Alumnos.jsx'
import Profesores from './components/Profesores.jsx'
import Admin from './components/Admin.jsx'
import './App.css'

function App() {

  return (
    <div>
      <Router>
        <Switch>
          <Route path="/" exact component={Home} />
          <Route path="/login" component={Login} />
          <Route path="/alumnos" component={Alumnos} />
          <Route path="/profesores" component={Profesores} />
          <Route path="/admin" component={Admin} />
        </Switch>
      </Router>
    </div>
  )
    
}

export default App
