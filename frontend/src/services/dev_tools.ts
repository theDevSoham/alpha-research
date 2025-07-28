import axios from "axios";
const API = axios.create({
  baseURL: "/dev",
});

export const reseedPeople = () => API.post("/reseed");
export const unseedPeople = () => API.post("/unseed");
export const unenrichPeople = () => API.post("/unenrich");

export default API;
