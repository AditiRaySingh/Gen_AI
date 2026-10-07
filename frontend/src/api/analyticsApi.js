import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000/api"
});

export const runQuery = async (query) => {
  const response = await API.post("/query", {
    query: query
  });

  return response.data;
};

export const sendFeedback = async (query, feedback) => {
  const response = await API.post("/feedback", {
    query: query,
    feedback: feedback
  });

  return response.data;
};