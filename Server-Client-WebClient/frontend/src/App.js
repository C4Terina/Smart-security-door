import React, { Component} from 'react';
import './App.css';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css'; 
import BootTable from './table/BootTable';

const api = axios.create({
  baseURL: 'http://localhost:8000/data'
})

const DataColumns = [
  {title: "Camera Number", filed: "camera_id"},
  {title: "Person enterded", filed: "person_name"},
  {title: "At Time", filed: "time_recognised"},
]


class App extends Component{

  render() {

    return(
      <div className='App'>
        <BootTable></BootTable>
      </div>
    );


  }
  
}

export default App;
