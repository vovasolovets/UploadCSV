import React, { Component } from 'react';
import Form from "@rjsf/core";
import DataSetsService from './DataSetService';

const dataSetsService = new DataSetsService();

const schema = {
  "type": "object",
  "required": ["row_number"],
  "properties": {
        "row_number": {
          "type": "integer"
        }
  }
};

class DataSetGenerateFile extends Component {
    constructor(props) {
        super(props);
      }

      componentDidMount(){
        const params = this.props;
        if(params && params.id)
        {

        }
      }

      handleUpdate(id, formData){
        dataSetsService.uploadRowNumbers(id, formData
        ).then((result)=>{
          alert("DataSet updated!");
        }).catch(()=>{
          alert('There was an error! Please re-check your form.');
        });
      }
      handleSubmitData(formData) {
        const params = this.props;
        console.log(params);

        if(params && params.id){
          this.handleUpdate(params.id, formData);
        }
      }

      render(){
        return (<Form schema={schema}
                onSubmit={({formData}) => {
                this.handleSubmitData(formData)}
                }/>)
      }
}

export default DataSetGenerateFile;