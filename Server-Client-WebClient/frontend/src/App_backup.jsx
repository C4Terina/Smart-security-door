
import React, { Component} from 'react';
import './App.css';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css'; 


const api = axios.create({
  baseURL: 'http://localhost:8000/data'
})

const DataColumns = [
  {title: "Camera Number", filed: "camera_id"},
  {title: "Person enterded", filed: "person_name"},
  {title: "At Time", filed: "time_recognised"},
]


class App extends Component{

  

  state = {
    camData: []
  }

  constructor() {
    super();
    this.getCamData();
  }

  getCamData = async () => {
    let data = await api.get("/").then(({data}) => data);
    this.setState({camData: data})
  }
  
  deleteEntry = async (entry_id) => {
    let data = await api.delete(`/${entry_id}`)
    this.getCamData();
  }


  render() {

    return(

      <div className="App list-group-item  justify-content-center align-items-center mx-auto" style={{"backgroundColor":"white", "marginTop":"15px"}} >
       <h1 className="card text-white bg-primary mb-1" styleName="max-width: 20rem;">Task Manager</h1>
       <h6 className="card text-white bg-primary mb-3">FASTAPI - React - MongoDB</h6>
      <div className="card-body">
       <h5 className="card text-white bg-dark mb-3">Your Tasks</h5>
       <div >

        {this.state.camData.map(cdata => <h2 key={cdata.entry_id}>/ {cdata.entry_id} \ {cdata.camera_id} - 
                                                                  {cdata.person_name} - 
                                                                  {cdata.time_recognised}<button onClick={() =>
                                                                   this.deleteEntry(cdata.entry_id)}>X</button></h2>)}
       </div>
       </div>
     </div>

    );


  }
  
}

export default App;