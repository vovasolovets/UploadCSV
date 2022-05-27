import  React, { Component } from  'react';
import  DataSetsService  from './DataSetService';

const  datasetsService  =  new  DataSetsService();

class  DataSetsList  extends  Component {

constructor(props) {
	super(props);
	this.state  = {
		datasets: [],
		nextPageURL:  ''
	};
	this.nextPage  =  this.nextPage.bind(this);
	this.handleDelete  =  this.handleDelete.bind(this);
}

componentDidMount() {
	var  self  =  this;
	datasetsService.getDataSets().then(function (result) {
		self.setState({ datasets:  result, nextPageURL:  result.nextlink});
	});
}
handleDelete(e,id){
	var  self  =  this;
	datasetsService.deleteDataSet({id :  id}).then(()=>{
		var  newArr  =  self.state.datasets.filter(function(obj) {
			return  obj.id  !==  id;
		});
		self.setState({datasets:  newArr})
	});
}

nextPage(){
	var  self  =  this;
	datasetsService.getDataSetsByURL(this.state.nextPageURL).then((result) => {
		self.setState({ datasets:  result, nextPageURL:  result.nextlink});
		console.log(this.state);
	});
}
render() {
	console.log(this.state.datasets);
	return (
		<div  className="datasets--list">
			<table  className="table">
			<thead  key="thead">
			<tr>
				<th>#</th>
				<th>Name</th>
				<th>Files</th>
			</tr>
			</thead>
			<tbody>
			{this.state.datasets.map( c  =>
				<tr  key={c.id}>
				<td>{c.id}  </td>
				<td>{c.name}</td>
				<td>{c.datasetexample_set.map( (example) =>
				{
					console.log(example.link);
					console.log(example.file_name);
					return <a href={`localhost:8000${example.link}`} download='{example.file_name}'> {example.file_name}</a>
				})}</td>
				<td>
				<button  onClick={(e)=>  this.handleDelete(e,c.id) }> Delete</button>
				<a  href={`/dataset/${c.id}`}>Update</a>
				<a  href={`/dataset/${c.id}/generate-file`}>Generate File</a>
				</td>
			</tr>
            )}
			</tbody>
			</table>
			<button  className="btn btn-primary"  onClick=  {  this.nextPage  }>Next</button>
		</div>
		);
  }
}
export  default  DataSetsList;