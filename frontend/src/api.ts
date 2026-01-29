import axios from 'axios';

// Configure axios instance
const api = axios.create({
  baseURL: '/api',
  withCredentials: true,
});

export interface LoginRequest {
  username: string;
  password: string;
}

export const login = async (data: LoginRequest) => {
  const res = await api.post('/login', data);
  return res.data;
};

export interface Account {
  id: number;
  name: string;
  bank?: string | null;
  account_number?: string | null;
  initial_balance: number;
  owner_id: number;
  type: string;
}

export const fetchAccounts = async (): Promise<Account[]> => {
  const res = await api.get('/accounts');
  return res.data;
};

export interface CreateAccountRequest {
  name: string;
  bank?: string;
  account_number?: string;
  initial_balance: number;
  type: string;
}

export const createAccount = async (data: CreateAccountRequest) => {
  const res = await api.post('/accounts', data);
  return res.data;
};

export default api;