import React, { Component } from 'react';
import Form from "@rjsf/core";
import DataSetsService from './DataSetService';
import {useParams } from 'react-router-dom';

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

const handleUpdate = (id, formData) =>{
        dataSetsService.uploadRowNumbers(id, formData
        ).then((result)=>{
          alert("DataSet updated!");
        }).catch(()=>{
          alert('There was an error! Please re-check your form.');
        });
      };
const handleSubmitData = (id, formData) => {
        console.log(formData);
        console.log(id);
        if(id){
          handleUpdate(id, formData);
        }
      };

const DataSetGenerateFile = () => {
        let { id } = useParams();
        return (<Form schema={schema}
                onSubmit={({formData}) => {
                handleSubmitData(id, formData)}
                }/>)
};

export default DataSetGenerateFile;