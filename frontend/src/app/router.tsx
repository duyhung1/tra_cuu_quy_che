import { createBrowserRouter, Navigate } from 'react-router-dom';
import { AskPage } from '../features/ask/AskPage';
import { DocumentsPage } from '../features/documents/DocumentsPage';
import { AppShell } from './AppShell';

export const router = createBrowserRouter([
  {
    element: <AppShell />,
    children: [
      { path: '/', element: <Navigate to="/ask" replace /> },
      { path: '/ask', element: <AskPage /> },
      { path: '/documents', element: <DocumentsPage /> },
      { path: '*', element: <Navigate to="/ask" replace /> },
    ],
  },
]);
