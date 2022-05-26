import React, { Component } from 'react';
import Form from "@rjsf/core";
import DataSetsService from './DataSetService';
import {useParams} from "react-router-dom";

const dataSetsService = new DataSetsService();

const schema = {
  "type": "object",
  "required": ["name", "json_schema"],
  "properties": {
        "name": {
          "type": "string"
        },
        "json_schema": {
          "type": "array",
          "items": {
            "type": "object",
            "required":["name", "data_type", "order"],
            "properties": {
              "name": {
                "type": "string",
              },
              "data_type": {
                "type": "string",
                "enum": ["full_name", "email", "domain_name", "phone_number",
                  "company_name", "address", "date"],
              },
              "order": {
                "type": "integer",
              }
            }
          }
        }
  }
};

const handleCreate = (formData) =>{
        dataSetsService.createDataSet(formData
        ).then((result)=>{
          console.log(result);
          alert("DataSet created!");
        }).catch(()=>{
          alert('There was an error! Please re-check your form.');
        });
      };

const handleUpdate = (id, formData)=> {
        dataSetsService.updateDataSet(id, formData
        ).then((result)=>{
          alert("DataSet updated!");
        }).catch(()=>{
          alert('There was an error! Please re-check your form.');
        });
      };

const handleSubmitData = (id, formData) => {

        if(!!id){
          handleUpdate(id, formData);
        }
        else
        {
          handleCreate(formData);
        }

      };

const DataSetCreateUpdate = () => {
      let {id} = useParams();
      return (<Form schema={schema}
                onSubmit={({formData}) => {
                handleSubmitData(id, formData)}
                }/>)
};

export default DataSetCreateUpdate;