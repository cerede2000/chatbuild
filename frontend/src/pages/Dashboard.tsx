import React from 'react';
import { Link } from 'react-router-dom';

const Dashboard: React.FC = () => {
  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Tableau de bord</h1>
      <p>Bienvenue dans votre espace personnel.</p>
      <div className="mt-4">
        <Link to="/accounts" className="text-blue-600 underline">
          Gérer mes comptes
        </Link>
      </div>
    </div>
  );
};

export default Dashboard;