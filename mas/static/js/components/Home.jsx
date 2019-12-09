import React, { Component } from 'react';
import axios from 'axios';

export default class Home extends Component {

   constructor(props) {
      super(props);
      this.state = { keywords: "" };

      this.handleChange = this.handleChange.bind(this);
      this.handleSubmit = this.handleSubmit.bind(this);
   }

   handleChange(event) {
      this.setState({
         keywords: event.target.value
      })
   }
   
   handleSubmit(event) {
      axios.post('/agent/search')
         .then(response => {
            alert(response.data);
         })

      event.preventDefault();
   }
   
    render() {
       return ( 
         <div class="container">
            <div class="py-5 text-center">
               <img class="d-block mx-auto mb-4" src="public/images/robot.jpg" alt="" width="144" height="144" />
               <h2>Multi-Agent System</h2>
               <p class="lead">Hello, World</p>
            </div>

            <div class="row">
            <div class="col-md-8 mx-auto">
                  <h4 class="mb-3 text-center">Send request to the Agent</h4>
                  <form class="needs-validation" novalidate="" onSubmit={this.handleSubmit}>
                     <div class="mb-3">
                        <label for="keywords">Keyworkd</label>
                        <div class="input-group">
                           <input type="text" class="form-control" id="keywords" placeholder="Keywords" required="" value={this.state.keywords} onChange={this.handleChange}/>
                           <div class="invalid-feedback">
                           Request keywords are required.
                           </div>
                        </div>
                     </div>

                     <hr class="mb-4"/>
                     <button class="btn btn-primary btn-lg btn-block" type="submit" >Send</button>
                  </form>
               </div>
            </div>
         </div>
       )
    }
}
