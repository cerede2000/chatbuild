import React, { useEffect, useState } from 'react';
import { fetchAccounts, Account, createAccount, CreateAccountRequest } from '../api';

const Accounts: React.FC = () => {
  const [accounts, setAccounts] = useState<Account[]>([]);
  const [loading, setLoading] = useState(true);
  const [form, setForm] = useState<CreateAccountRequest>({
    name: '',
    bank: '',
    account_number: '',
    initial_balance: 0,
    type: 'PERSONAL',
  });
  const [error, setError] = useState<string | null>(null);

  const loadAccounts = async () => {
    setLoading(true);
    try {
      const data = await fetchAccounts();
      setAccounts(data);
    } catch (err) {
      setError('Impossible de charger les comptes');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAccounts();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await createAccount(form);
      setForm({ name: '', bank: '', account_number: '', initial_balance: 0, type: 'PERSONAL' });
      loadAccounts();
    } catch (err) {
      setError('Erreur lors de la création du compte');
    }
  };

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Mes comptes</h1>
      {error && <p className="text-red-600">{error}</p>}
      <form onSubmit={handleSubmit} className="mb-6 bg-white shadow rounded p-4 max-w-md">
        <h2 className="text-lg font-bold mb-2">Créer un compte</h2>
        <div className="mb-2">
          <label className="block text-sm mb-1" htmlFor="name">Nom</label>
          <input
            id="name"
            type="text"
            value={form.name}
            onChange={(e) => setForm({ ...form, name: e.target.value })}
            className="w-full border px-2 py-1"
          />
        </div>
        <div className="mb-2">
          <label className="block text-sm mb-1" htmlFor="bank">Banque</label>
          <input
            id="bank"
            type="text"
            value={form.bank}
            onChange={(e) => setForm({ ...form, bank: e.target.value })}
            className="w-full border px-2 py-1"
          />
        </div>
        <div className="mb-2">
          <label className="block text-sm mb-1" htmlFor="account_number">Numéro de compte</label>
          <input
            id="account_number"
            type="text"
            value={form.account_number}
            onChange={(e) => setForm({ ...form, account_number: e.target.value })}
            className="w-full border px-2 py-1"
          />
        </div>
        <div className="mb-2">
          <label className="block text-sm mb-1" htmlFor="initial_balance">Solde initial</label>
          <input
            id="initial_balance"
            type="number"
            step="0.01"
            value={form.initial_balance}
            onChange={(e) => setForm({ ...form, initial_balance: parseFloat(e.target.value) || 0 })}
            className="w-full border px-2 py-1"
          />
        </div>
        <div className="mb-2">
          <label className="block text-sm mb-1" htmlFor="type">Type</label>
          <select
            id="type"
            value={form.type}
            onChange={(e) => setForm({ ...form, type: e.target.value })}
            className="w-full border px-2 py-1"
          >
            <option value="PERSONAL">Personnel</option>
            <option value="JOINT">Joint</option>
          </select>
        </div>
        <button
          type="submit"
          className="bg-blue-500 text-white py-1 px-4 rounded mt-2"
        >
          Ajouter
        </button>
      </form>
      <h2 className="text-lg font-bold mb-2">Liste des comptes</h2>
      {loading ? (
        <p>Chargement…</p>
      ) : (
        <ul className="space-y-2">
          {accounts.map((acc) => (
            <li key={acc.id} className="p-2 bg-white shadow rounded">
              <span className="font-semibold">{acc.name}</span> — {acc.type}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default Accounts;