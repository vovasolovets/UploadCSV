import axios from 'axios';
import Cookies from 'js-cookie'
import qs from 'qs'
const API_URL = 'http://localhost:8000';

export const getCookieCsrf = () => {
  return Cookies.get('csrftoken') || ''
}

const axiosInstance = axios.create({
  baseURL: API_URL,
  withCredentials: true,
  paramsSerializer: function (params) {
    return qs.stringify(params, { arrayFormat: 'repeat' })
  },
  headers: {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': 'http://localhost:8000',
    'Access-Control-Allow-Credentials':true,
    'X-CSRFTOKEN': getCookieCsrf(),
  },
})

export default class DataSetsService{

	constructor(){}


	getDataSets() {
		const url = `/upload/datasets`;
		return axiosInstance.get(url).then(response => response.data);
	}
	getDataSetsByURL(link){
		const url = `${link}`;
		return axiosInstance.get(url).then(response => response.data);
	}
	getDataSet(id) {
		const url = `/upload/datasets/${id}`;
		return axiosInstance.get(url).then(response => response.data);
	}
	deleteDataSet(dataset){
		const url = `/upload/datasets/${dataset.id}`;
		return axiosInstance.delete(url);
	}
	createDataSet(dataset){
		const url = `/upload/datasets`;
		return axiosInstance.post(url, JSON.stringify(dataset));
	}
	updateDataSet(id, dataset){
		const url = `/upload/datasets/${id}`;
		return axiosInstance.put(url, JSON.stringify(dataset));
	}
	uploadRowNumbers(id, dataset){
		const url = `/upload/datasets/${id}/generate-file`;
		return axiosInstance.post(url, JSON.stringify(dataset))
	}
}