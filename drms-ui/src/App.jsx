import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'
import './App.css'
import AddEmployee from './components/AddEmployee' 
import ViewEmployees from './components/ViewEmployees'
import EditEmployee from './components/EditEmployee'
import UploadImage from './components/UploadImage'
import QueriyImages from './components/QueriyImages'
import NavBar from './components/NavBar'
import Home from './components/Home'

function App() { 

  return (
    <Router>
      <NavBar/>
      <Routes>
        <Route path ='/' element = {<Home/>} />
        <Route path = "/add-employee" element = {<AddEmployee/>} />
        <Route path ='/view-employees' element = {<ViewEmployees/>} />
        <Route path ='/queryImages' element = {<QueriyImages/>} />
        <Route path ="/editEmployee" element ={<EditEmployee />} />
        <Route path ='/uploadImage' element = {<UploadImage />} />
      </Routes>
    </Router>
  )
}

export default App
