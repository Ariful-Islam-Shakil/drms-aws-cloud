import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'
import './App.css'
import AddEmployee from './components/AddEmployee'
import AdminPanel from './components/AdminPanel'
import ViewEmployees from './components/ViewEmployees'
import Queries from './components/Queries'
import EditEmployee from './components/EditEmployee'

function App() { 

  return (
    <Router>
      <Routes>
        <Route path='/' element = {<AdminPanel/>} />
        <Route path = "/add-employee" element = {<AddEmployee/>} />
        <Route path='/view-employees' element = {<ViewEmployees/>} />
        <Route path='/queries' element = {<Queries/>} />
        <Route path="/editEmployee" element={<EditEmployee />} />
      </Routes>
    </Router>
  )
}

export default App
