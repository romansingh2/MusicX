import React, { Component } from "react";
import Button from "@material-ui/core/Button";
import Grid from "@material-ui/core/Grid";
import Typography from "@material-ui/core/Typography";
import TextField from "@material-ui/core/TextField";
import FormHelperText from "@material-ui/core/FormHelperText";
import FormControl from "@material-ui/core/FormControl";
import { Link } from "react-router-dom";
import Radio from "@material-ui/core/Radio";
import RadioGroup from "@material-ui/core/RadioGroup";
import FormControlLabel from "@material-ui/core/FormControlLabel";
import { Collapse } from "@material-ui/core";
import Alert from "@material-ui/lab/Alert";



export default class CreateRoomPage extends Component {
  static defaultProps = { // if no values are passed to these variables, they will have these default values
    votesToSkip: 2,
    guestCanPause: true,
    update: false,
    roomCode: null, 
    updateCallback: () => { },
  };
   
constructor(props) {
  super(props);
  this.state = {
    guestCanPause: this.props.guestCanPause,
    votesToSkip: this.props.votesToSkip,
    errorMsg: "",
    successMsg: "",
  };

  this.handleRoomButtonPressed = this.handleRoomButtonPressed.bind(this); //binding this method to the class so inside of handleRoomButtonPressed we can use this method
  this.handleVotesChange = this.handleVotesChange.bind(this);
  this.handleGuestCanPauseChange = this.handleGuestCanPauseChange.bind(this);
  this.handleUpdateButtonPressed = this.handleUpdateButtonPressed.bind(this);
  }
    
handleVotesChange(e) { //e means object that called this function
  this.setState({
    votesToSkip : e.target.value, //get the object that called this function, in this case the textfield, it will then get the value from the textfield and put it here for votesToSkip  
  });
}

handleGuestCanPauseChange(e) {
  this.setState({
    guestCanPause: e.target.value === 'true' ? true : false, //if this value is equal to the string "true", then make what is here true, otherwise make it false
  })
}

  handleRoomButtonPressed() {
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" }, //HTTP headers let the client and the server pass additional information with an HTTP request or response. Content-Type is an HTTP header which is used to indicate the media type of the resource and in case of responses it tells the browser about what actually content type of the returned content is. In case of any POST or PUT requests, the client tells the server about the kind of data sent. The header is there so your app can detect what data was returned and how it should handle it. The content header is just information about the type of returned data, ex::JSON,image(png,jpg,etc..),html
      body: JSON.stringify({ //The JSON.stringify() method converts a JavaScript object or value to a JSON string, 
        votes_to_skip: this.state.votesToSkip,
        guest_can_pause: this.state.guestCanPause,
      }),
    };
    fetch("/api/create-room", requestOptions) //fetch api fetches resources
      .then((response) => response.json())  //Here we are fetching a JSON file across the network and printing it to the console. The simplest use of fetch() takes one argument — the path to the resource you want to fetch — and returns a promise containing the response (a Response object). This is just an HTTP response, not the actual JSON. To extract the JSON body content from the response, we use the json() method (defined on the Body mixin, which is implemented by both the Request and Response objects.)
      .then((data) => this.props.history.push('/room/' + data.code));
    }
  
    handleUpdateButtonPressed() {
      const requestOptions = {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          votes_to_skip: this.state.votesToSkip,
          guest_can_pause: this.state.guestCanPause,
          code: this.props.roomCode,
        }),
      };
      fetch("/api/update-room", requestOptions).then((response) => {
        if (response.ok) {
          this.setState({
            successMsg: "Room updated successfully!",
          });
        } else {
          this.setState({
            errorMsg: "Error updating room...",
          });
        }
        this.props.updateCallback();
      });
    }
  


  renderCreateButtons() { 
    return (
  <Grid container spacing = {1}>
    <Grid item xs = {12} align="center">
      <Button color="primary" variant = "contained" onClick={this.handleRoomButtonPressed} >
      Create A Room
      </Button>
    </Grid>
    <Grid item xs = {12} align="center">
      <Button color="secondary" variant = "contained" to="/"  component={Link}>
        Back 
      </Button>
    </Grid>
  </Grid>
    );
  }

  renderUpdateButtons () {
    return (
      <Grid item xs = {12} align="center">
        <Button color="primary" 
        variant = "contained" 
        onClick={this.handleUpdateButtonPressed} 
        >
          Update Room
        </Button>
      </Grid>
    );
  }




  render() {
    const title = this.props.update ? "Update Room" : "Create a Room"; //if this.props.update is true, {title} will be "update room", otherwise its "create a room"
    
    return (
            <Grid container spacing={1}> 
              <Grid item xs = {12} align="center">
                 <Collapse 
                 in={ this.state.errorMsg != "" || "" || this.state.successMsg != ""}
                 > 
                  {this.state.successMsg != "" ? 
                  (<Alert severity = "success" 
                  onClose={() => 
                    {this.setState({successMsg : ""});
                }} >
                  {this.state.successMsg}
                  </Alert>) 
                  : (<Alert severity = "error" onClose={() => 
                    {this.setState({errorMsg : ""});
                }}>
                    {this.state.errorMsg}
                    </Alert>)}
                 </Collapse>
              </Grid>
              <Grid item xs = {12} align="center">
                  <Typography component='h4' variant="h4">
                  {title}
                  </Typography>
              </Grid>
              <Grid item xs = {12} align="center">
                <FormControl component="fieldset">
                   <FormHelperText>
                     <div align='center'> Guest Control of Playback State </div>                    
                        </FormHelperText>
                        <RadioGroup 
                        row 
                        defaultValue='true' 
                        onChange={this.handleGuestCanPauseChange}
                        >
                            <FormControlLabel
                            value= {this.props.guestCanPause.toString()}
                            control = {<Radio color="primary" /> }
                            label = "Play/Pause"
                            labelPlacement = "bottom"
                          />
                        
                            <FormControlLabel 
                            value="false" 
                            control = {<Radio color="secondary" /> }
                            label = "No Control"
                            labelPlacement = "bottom"
                          />
                    </RadioGroup>
                </FormControl>
              </Grid>
                <Grid item xs = {12} align="center">
                  <FormControl>
                    <TextField 
                    required = {true} 
                    type = "number" 
                    onChange={this.handleVotesChange}
                    defaultValue = {this.state.votesToSkip}
                    inputProps = {{
                    min: 1,
                    style: { textAlign: "center"}
                    }}
                          />
                    <FormHelperText>
                      <div align="center">
                        Votes Required to Skip Song
                      </div>
                    </FormHelperText>
                  </FormControl>
                </Grid> 
                {this.props.update 
                ? this.renderUpdateButtons() 
                : this.renderCreateButtons()}  
            </Grid>
    );
    
    
    //Grid is a standard thing used in material UI to align items vertically or horizontally, 
    //by default when we define grid like this it is a container and it will hold and align things vertically in a column structure
    // The spacing is how much space we should put between the items in the grid, 1 means eight pixels    
    //grid item xs = {12} tells us what the width of the grid item should be when the screen size is extra small, ie when you shrink browser, 12 is the most wide it can be
    // Typography is a nicely styled header from material UI
    // FormControl Provides context such as filled/focused/error/required for form inputs.
    //FormHelperText helps us create labels
    //A radio button or option button is a graphical control element that allows the user to choose only one of a predefined set of mutually exclusive options. 
    //by default guests will have control of playback
    //Textfield required = {true} means it is required to type something in here, minimum value for the textfield is 1
    // inputProps is Attributes applied to the input element.
    //the reason we put two squiggly brackets is because it accepts an object and we need to pass a javascript object
    //<Button color="primary" variant = "contained" to="/"  component={Link}> means this button will act as a link, hence why we imported link and will redirect to "/"
    //use react state to keep track of what is in our form
    //if we are updating then return this.renderUpdateButtons, otherwise return this.renderCreateButtons
    // "in" is a boolean value that tells whether something should be shown or not, if the condition we put in the sqiuggly brackets is true, show whatever is inside the collapse tag, otherwise don't show it
  }
}