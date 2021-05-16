import React, {useState} from "react";
import { render } from "react-dom"; 
import HomePage from './HomePage';

/*
export default class App extends Component {
    constructor(props) {
        super(props);
        
    }
    render() {
        return(
        <div className = "center">  
        <HomePage/>
        
        </div>
        );
    }
}


*/

 // a prop is a property or arguement we give to a component, and use that to modify behaviour of component
 // whenever we want to write javascript code in a render function we need scquiggly brackets '{}' 

 function App() {
    return(
        <div className = "center">  
        <HomePage/>
        
        </div>
        );
 }

 const appDiv = document.getElementById("app");
render(<App />, appDiv); //take this class "App" and render it on the appDiv. The app div is equal to the id "app" on index.html