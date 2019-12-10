import React, { Component } from "react";

import Splash from './Splash'
import Agent from './Agent'

export default class Home extends Component {
  render() {
    return (
      <div id = "root">
         <Splash />

         <Agent />
      </div>
    );
  }
}
