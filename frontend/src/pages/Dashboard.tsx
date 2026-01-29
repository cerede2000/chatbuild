import React, { useContext } from 'react';
import { Link } from 'react-router-dom';
import { AuthContext } from '../providers/AuthProvider';

const Dashboard: React.FC = () => {
  const { isAdmin } = useContext(AuthContext);
  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Tableau de bord</h1>
      <p>Bienvenue dans votre espace personnel.</p>
      <div className="mt-4">
        <Link to="/accounts" className="text-blue-600 underline">
          Gérer mes comptes
        </Link>
        {isAdmin && (
          <div className="mt-2">
            <Link to="/admin/users" className="text-blue-600 underline">
              Gérer les utilisateurs
            </Link>
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;