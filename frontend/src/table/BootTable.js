
import React , {Component, useEffect, useState}from 'react'
import axios from 'axios'
import * as ReactBootStrap from 'react-bootstrap'
import Button from 'react-bootstrap/Button';

class BootTable extends Component{

    // constructor 
    constructor(pros){ 
        super(pros)

        this.state = {
            posts: []
        }
    }
    // load all data 
    fetchAllData(){
        axios.get("http://localhost:8000/data") // use axios GET request
        .then(response => {
            this.setState({
                posts: response.data // save the data
            })
            // console.log(response.data) // Output the data to the console
        })
    }

    timeDescData(){
        axios.get("http://localhost:8000/data/tm_asce") // use axios GET request
        .then(response => {
            this.setState({
                posts: response.data // save the data
            })
            // console.log(response.data) // Output the data to the console
        })
    }

    idDescData(){
        axios.get("http://localhost:8000/data/cm_desc") // use axios GET request
        .then(response => {
            this.setState({
                posts: response.data // save the data
            })
            // console.log(response.data) // Output the data to the console
        })
    }

    // delete one entry from the database
    deleteEntry = async (entry_id) => {
        axios.delete(`http://localhost:8000/data/${entry_id}`) // use axios GET request
        .then(() => this.setState({}))
        this.fetchAllData(); // recall the GET function 
      }

    render() { 

        const {posts} = this.state

        return ( // return a table with data
            <div>
                <h1>Camera Logs</h1>

                <form className='row g- ms-auto'>
                    <div className='col-auto'>
                        <input
                            type="text" 
                            className='form-control ms-auto' 
                            placeholder='search data'/>
                    </div>
                </form>
                <button onClick={this.fetchAllData()}>Refresh component</button>
                <ReactBootStrap.Table>
                <thead>
                    <tr>
                    <th>#ID<button onClick={() => this.idDescData()}>↓</button></th>
                    <th>Camera Number</th>
                    <th>Person Entered</th>
                    <th>Time Entered <button onClick={() => this.timeDescData()}>↓</button></th>
                    <th>Delete</th>
                    </tr>
                </thead>
                <tbody>
                    {
                        posts.map((item) =>(
                            <tr key={item.entry_id}>
                                <td>{item.entry_id}</td>
                                <td>{item.camera_id}</td>
                                <td>{item.person_name}</td>
                                <td>{item.time_recognised}</td>
                                <td><Button variant="danger" onClick={() =>
                                    this.deleteEntry(item.entry_id)}>X</Button>
                                </td>
                            </tr>
                        ))
                    }
                </tbody>
                </ReactBootStrap.Table>
            </div>
        )
    }

}

export default BootTable
