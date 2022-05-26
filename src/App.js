
import  React, { Component } from  'react';
import { BrowserRouter } from  'react-router-dom'
import { Route, Routes, Link } from  'react-router-dom'
import './App.css';
import DataSetsList from "./DataSetsList";
import DataSetCreateUpdate from "./DataSetCreateUpdate";
import DataSetGenerateFile from './DataSetGenerateFile';


const BaseLayout = () => (
  <div className="container-fluid">
<nav className="navbar navbar-expand-lg navbar-light bg-light">
  <a className="navbar-brand" href="#">Django React Demo</a>
  <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
    <span className="navbar-toggler-icon"></span>
  </button>
  <div className="collapse navbar-collapse" id="navbarNavAltMarkup">
    <div className="navbar-nav">
      <a className="nav-item nav-link" href="/">DATASET</a>
      <a className="nav-item nav-link" href="/dataset">CREATE DATASET</a>

    </div>
  </div>
</nav>

    <div className="content">
      <Routes>
      <Route exact path="/" element={<DataSetsList/>} />
      <Route path="/dataset/:id"  element={<DataSetCreateUpdate/>} />
      <Route path="/dataset/:id/generate-file"  element={<DataSetGenerateFile/>} />
      <Route exact path="/dataset" element={<DataSetCreateUpdate/>} />
      </Routes>
    </div>

  </div>
)

class App extends Component {
  render() {
    return (
      <BrowserRouter>

        <BaseLayout/>
      </BrowserRouter>
    );
  }
}

export default App;