import React, { createContext, useState } from 'react';

/**
 * Contexte d’authentification.
 *
 * Il expose l’état de connexion (`isAuthenticated`), le nom de l’utilisateur
 * connecté et le statut administrateur. La fonction `setAuthenticated` permet
 * de mettre à jour ces valeurs et accepte facultativement le nom
 * d’utilisateur lorsqu’on passe en mode connecté.
 */
interface AuthContextType {
  isAuthenticated: boolean;
  username: string | null;
  isAdmin: boolean;
  /**
   * Met à jour l’état d’authentification. Si `auth` vaut `true`, vous pouvez
   * fournir `username` pour mettre à jour le nom d’utilisateur stocké. Si
   * `auth` vaut `false`, le nom d’utilisateur est réinitialisé.
   */
  setAuthenticated: (auth: boolean, username?: string | null) => void;
}

export const AuthContext = createContext<AuthContextType>({
  isAuthenticated: false,
  username: null,
  isAdmin: false,
  setAuthenticated: () => {},
});

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [username, setUsername] = useState<string | null>(null);

  const setAuthenticated = (auth: boolean, usernameParam?: string | null) => {
    setIsAuthenticated(auth);
    if (auth) {
      setUsername(usernameParam || null);
    } else {
      setUsername(null);
    }
  };

  const isAdmin = username === 'admin';

  return (
    <AuthContext.Provider value={{ isAuthenticated, username, isAdmin, setAuthenticated }}>
      {children}
    </AuthContext.Provider>
  );
};