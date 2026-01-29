import React, { useContext, useEffect, useState } from 'react';
import { Navigate } from 'react-router-dom';
import { AuthContext } from '../providers/AuthProvider';
import { fetchUsers, createUser, User } from '../api';

/**
 * Page de gestion des utilisateurs pour l’administrateur.
 *
 * Permet de lister les utilisateurs existants et d’en créer de nouveaux. Elle
 * redirige vers la page d’accueil si l’utilisateur courant n’est pas admin.
 */
const AdminUsers: React.FC = () => {
  const { isAdmin } = useContext(AuthContext);
  const [users, setUsers] = useState<User[]>([]);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [isAdminFlag, setIsAdminFlag] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (isAdmin) {
      fetchUsers()
        .then(setUsers)
        .catch(() => setUsers([]));
    }
  }, [isAdmin]);

  if (!isAdmin) {
    return <Navigate to="/" replace />;
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    try {
      const newUser = await createUser({ username, password, is_admin: isAdminFlag });
      setUsers([...users, newUser]);
      setUsername('');
      setPassword('');
      setIsAdminFlag(false);
    } catch {
      setError("Erreur lors de la création de l’utilisateur");
    }
  };

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-4">Gestion des utilisateurs</h2>
      {error && <p className="text-red-600 mb-2">{error}</p>}
      <form onSubmit={handleSubmit} className="mb-4 flex flex-wrap items-center">
        <input
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="Nom d’utilisateur"
          className="border p-2 mr-2 mb-2"
        />
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Mot de passe"
          className="border p-2 mr-2 mb-2"
        />
        <label className="flex items-center mr-2 mb-2">
          <input
            type="checkbox"
            checked={isAdminFlag}
            onChange={(e) => setIsAdminFlag(e.target.checked)}
            className="mr-1"
          />
          Admin
        </label>
        <button
          type="submit"
          className="bg-blue-500 text-white p-2 rounded mb-2"
        >
          Créer
        </button>
      </form>
      <table className="min-w-full bg-white">
        <thead>
          <tr>
            <th className="border px-4 py-2">ID</th>
            <th className="border px-4 py-2">Nom</th>
            <th className="border px-4 py-2">Admin</th>
            <th className="border px-4 py-2">Actif</th>
          </tr>
        </thead>
        <tbody>
          {users.map((u) => (
            <tr key={u.id}>
              <td className="border px-4 py-2 text-center">{u.id}</td>
              <td className="border px-4 py-2">{u.username}</td>
              <td className="border px-4 py-2 text-center">{u.is_admin ? 'Oui' : 'Non'}</td>
              <td className="border px-4 py-2 text-center">{u.disabled ? 'Non' : 'Oui'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default AdminUsers;