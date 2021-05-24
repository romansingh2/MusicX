import React, { useState, useEffect } from "react";
import RoomJoinPage from "./RoomJoinPage";
import CreateRoomPage from "./CreateRoomPage";
import Room from "./Room";
import { Grid, Button, ButtonGroup, Typography } from "@material-ui/core";
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link,
  Redirect,
} from "react-router-dom";
import Info from "./info";
import MusicPlayer from "./MusicPlayer";



/*
export default class HomePage extends Component {
  constructor(props) {
    super(props);
    this.state = {
      roomCode: null,
    };
    this.clearRoomCode = this.clearRoomCode.bind(this)
  }

async componentDidMount() {
  fetch('/api/user-in-room') //call api/user-in-room, this will return to us whether or not we are in a room, if we are in a room we are going to get that room code coming in through the  field called code
  .then((response) => response.json()). //return response.json from our response, that will go to .then which is data, which is a json object
  then((data) => {
    this.setState({ 
      roomCode: data.code,
    });
  }); //parse and look through the json object to get the room code
}

renderHomePage() {
  return (
    <Grid container spacing={3}>
      <Grid item xs = {12} align="center">  
      <Typography variant = "h3" compact="h3">
          House Party
      </Typography>    
      </Grid>
      <Grid item xs = {12} align="center">
        <ButtonGroup disableElevation variant="contained" color="primary">
          <Button color="primary" to="/join" component ={Link}>
            Join a Room
          </Button>
          <Button color="default" to="/info" component ={Link}>
            Info
          </Button>         
          <Button color="secondary" to="/create" component ={Link}>
            Create a Room pretty please
          </Button>
        </ButtonGroup>
      </Grid>
    </Grid>
  );
}


clearRoomCode (){ //set the state so that our room code is null
  this.setState({
    roomCode: null, 
  });
}

render() {
  return (
    <Router>
      <Switch>
        <Route
          exact
          path="/"
          render={() => {
            return this.state.roomCode ? (
              <Redirect to={`/room/${this.state.roomCode}`} />
            ) : (
              this.renderHomePage()
            );
          }}
        />
        <Route path="/join" component={RoomJoinPage} />
        <Route path="/info" component = {Info} />
        <Route path="/create" component={CreateRoomPage} />
        <Route
          path="/room/:roomCode"
          render={(props) => {
            return <Room {...props} leaveRoomCallback={this.clearRoomCode} />;
          }}
        />
      </Switch>
    </Router>
  );
}
}
*/

export default function HomePage(props) {

const [roomCode, setRoomCode] = useState(null);


useEffect = () => {
  fetch('/api/user-in-room') //call api/user-in-room, this will return to us whether or not we are in a room, if we are in a room we are going to get that room code coming in through the  field called code
  .then((response) => response.json()). //return response.json from our response, that will go to .then which is data, which is a json object
  then((data) => {
      setRoomCode(data.code)   
  }); //parse and look through the json object to get the room code
}

function renderHomePage() {
  return (
    <Grid container spacing={3}>
      <Grid item xs = {12} align="center">  
      <Typography variant = "h3" compact="h3">
          MusicX
      </Typography>    
      </Grid>
      <Grid item xs = {12} align="center">
        <ButtonGroup disableElevation variant="contained" color="primary">
          <Button color="primary" to="/join" component ={Link}>
            Join a Room
          </Button>
          <Button color="default" to="/info" component ={Link}>
            Info
          </Button>         
          <Button color="secondary" to="/create" component ={Link}>
            Create a Room
          </Button>
        </ButtonGroup>
      </Grid>
    </Grid>
  );
}


const clearRoomCode = () => { //set the state so that our room code is null
    setRoomCode(null) 
};


  return (
    <Router>
      <Switch>
        <Route
          exact
          path="/"
          render={() => {
            return roomCode ? (
              <Redirect to={`/room/${roomCode}`} />
            ) : (
              renderHomePage()
            );
          }}
        />
        <Route path="/join" component={RoomJoinPage} />
        <Route path="/info" component = {Info} />
        <Route path="/create" component={CreateRoomPage} />
        <Route
          path="/room/:roomCode"
          render={(props) => {
            return <Room {...props} leaveRoomCallback={clearRoomCode} />;
          }}
        />
      </Switch>
    </Router>
  );
}







