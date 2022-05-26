import React, { Component } from 'react';
import Form from "@rjsf/core";
import DataSetsService from './DataSetService';

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

class DataSetCreateUpdate extends Component {
    constructor(props) {
        super(props);
      }

      componentDidMount(){
        const params = this.props;
        if(params && params.id)
        {
          dataSetsService.getDataSet(params.id).then((c)=>{
            this.refs.name.value = c.name;
            this.refs.json_schema.value = c.json_schema;
          })
        }
      }

      handleCreate(formData){
        dataSetsService.createDataSet(formData
        ).then((result)=>{
          console.log(result);
          alert("DataSet created!");
        }).catch(()=>{
          alert('There was an error! Please re-check your form.');
        });
      }
      handleUpdate(id, formData){
        dataSetsService.updateDataSet(id, formData
        ).then((result)=>{
          alert("DataSet updated!");
        }).catch(()=>{
          alert('There was an error! Please re-check your form.');
        });
      }
      handleSubmitData(formData) {
        const params = this.props;

        if(params && params.id){
          this.handleUpdate(params.id, formData);
        }
        else
        {
          this.handleCreate(formData);
        }

      }

      render(){
        return (<Form schema={schema}
                onSubmit={({formData}) => {
                this.handleSubmitData(formData)}
                }/>)
      }
}

export default DataSetCreateUpdate;