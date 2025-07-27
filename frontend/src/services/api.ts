import axios from "axios";
const API = axios.create({
  baseURL: "/api",
});

export const getPeople = () => API.get("/people");
export const enrichPerson = (id: string) => API.post(`/enrich/${id}`);
export const getSnippets = (companyId: string) =>
  API.get(`/snippets/${companyId}`);

export default API;
