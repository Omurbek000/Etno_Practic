import { Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { Loader } from "./States";

export default function ProtectedRoute({ children }) {
  const { user, loading } = useAuth();

  if (loading) return <Loader label="Проверка входа" />;
  if (!user) return <Navigate to="/login" replace />;
  return children;
}
