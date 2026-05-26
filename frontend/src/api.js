/**
 * API client for FairLend-Africa backend.
 * All communication with FastAPI goes through this module.
 */

import axios from "axios"

const BASE = "http://localhost:8001/api/v1"

export async function getPrediction(borrowerData) {
  const res = await axios.post(`${BASE}/predict`, borrowerData)
  return res.data
}

export async function getExplanation(borrowerData) {
  const res = await axios.post(`${BASE}/explain`, borrowerData)
  return res.data
}

export async function getEvaluation() {
  const res = await axios.get(`${BASE}/evaluate`)
  return res.data
}