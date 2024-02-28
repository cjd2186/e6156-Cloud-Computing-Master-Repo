import React from 'react';
import logo from './logo.svg';
import './App.css';
import {GoogleLogin} from '@react-oauth/google';

function App() {
    const responseMessage = (response: any) => {
        console.log(response);
        window.location.href = 'http://ec2-13-59-154-80.us-east-2.compute.amazonaws.com:8000/docs';
    };
    const errorMessage = () => {
        console.log('error')
    };

    return (
        <div>
            <h2>React Google Login</h2>
            <br/>
            <br/>
            <GoogleLogin onSuccess={responseMessage} onError={errorMessage}/>
        </div>
    )
}

export default App;
